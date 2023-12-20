from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import docker
import sys
import logging
import os
import ast

app = FastAPI()
PASS_CODE = 'OK'
FAIL_CODE = 'Fail'

docker_url = os.getenv("DOCKER_URL")
storage_path = os.getenv("STORAGE_PATH")

client = docker.DockerClient(docker_url)
res = {'code': '', 'data': {}, 'msg': ''}

class NodeCreateRequest(BaseModel):
    name: str
    msp: str
    tls: str
    bootstrap_block: str
    peer_config_file: str
    orderer_config_file: str
    type: str
    port_map: dict

class NodeOperateRequest(BaseModel):
    action: str
    form: dict

@app.get('/api/v1/networks')
def get_network():
    container_list = client.containers.list()
    containers = {}
    for container in container_list:
        containers[container.id] = {
            "id": container.id,
            "short_id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": str(container.image),
            "attrs": container.attrs
        }
    res = {'code': PASS_CODE, 'data': containers, 'msg': ''}
    return JSONResponse(content={'res': res})

@app.post('/api/v1/nodes')
def create_node(request: NodeCreateRequest):
    node_name = request.name
    env = {
        'HLF_NODE_MSP': request.msp,
        'HLF_NODE_TLS': request.tls,
        'HLF_NODE_BOOTSTRAP_BLOCK': request.bootstrap_block,
        'HLF_NODE_PEER_CONFIG': request.peer_config_file,
        'HLF_NODE_ORDERER_CONFIG': request.orderer_config_file,
        'platform': 'linux/amd64',
    }
    port_map = request.port_map
    volumes = [
        f'{storage_path}/fabric/{node_name}:/etc/hyperledger/fabric',
        f'{storage_path}/production/{node_name}:/var/hyperledger/production'
    ]
    if request.type == "peer":
        peer_envs = {
            'CORE_VM_ENDPOINT': 'unix:///host/var/run/docker.sock',
            'CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE': 'cello-net',
            'FABRIC_LOGGING_SPEC': 'INFO',
            'CORE_PEER_TLS_ENABLED': 'true',
            'CORE_PEER_PROFILE_ENABLED': 'true',
            'CORE_PEER_TLS_CERT_FILE': '/etc/hyperledger/fabric/tls/server.crt',
            'CORE_PEER_TLS_KEY_FILE': '/etc/hyperledger/fabric/tls/server.key',
            'CORE_PEER_TLS_ROOTCERT_FILE': '/etc/hyperledger/fabric/tls/ca.crt',
            'CORE_PEER_ID': node_name,
            'CORE_PEER_ADDRESS': f'{node_name}:7051',
            'CORE_PEER_LISTENADDRESS': '0.0.0.0:7051',
            'CORE_PEER_CHAINCODEADDRESS': f'{node_name}:7052',
            'CORE_PEER_CHAINCODELISTENADDRESS': '0.0.0.0:7052',
            'CORE_PEER_GOSSIP_BOOTSTRAP': f'{node_name}:7051',
            'CORE_PEER_GOSSIP_EXTERNALENDPOINT': f'{node_name}:7051',
            'CORE_OPERATIONS_LISTENADDRESS': '0.0.0.0:17051'
        }
        env.update(peer_envs)
    else:
        order_envs = {
            'FABRIC_LOGGING_SPEC': 'DEBUG',
            'ORDERER_GENERAL_LISTENADDRESS': '0.0.0.0',
            'ORDERER_GENERAL_LISTENPORT': '7050',
            'ORDERER_GENERAL_GENESISMETHOD': 'file',
            'ORDERER_GENERAL_LOCALMSPDIR': '/etc/hyperledger/fabric/msp',
            'ORDERER_GENERAL_GENESISFILE': '/etc/hyperledger/fabric/genesis.block',
            'ORDERER_GENERAL_TLS_ENABLED': 'true',
            'ORDERER_GENERAL_TLS_PRIVATEKEY': '/etc/hyperledger/fabric/tls/server.key',
            'ORDERER_GENERAL_TLS_CERTIFICATE': '/etc/hyperledger/fabric/tls/server.crt',
            'ORDERER_GENERAL_TLS_ROOTCAS': '[/etc/hyperledger/fabric/tls/ca.crt]',
            'ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE': '/etc/hyperledger/fabric/tls/server.crt',
            'ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY': '/etc/hyperledger/fabric/tls/server.key',
            'ORDERER_GENERAL_CLUSTER_ROOTCAS': '[/etc/hyperledger/fabric/tls/ca.crt]',
        }
        env.update(order_envs)
    try:
        container = client.containers.run(
            request.img,
            request.cmd,
            detach=True,
            tty=True,
            stdin_open=True,
            network="cello-net",
            name=request.name,
            dns_search=["."],
            volumes=volumes,
            environment=env,
            ports=port_map
        )
    except:
        res['code'] = FAIL_CODE
        res['data'] = sys.exc_info()[0]
        res['msg'] = 'creation failed'
        logging.debug(res)
        raise

    res['code'] = PASS_CODE
    res['data']['status'] = 'created'
    res['data']['id'] = container.id
    res['data']['public-grpc'] = '127.0.0.1:7050'  # TODO: read the info from config file
    res['data']['public-raft'] = '127.0.0.1:7052'
    res['msg'] = 'node created'
    return JSONResponse(content=res)

@app.get('/api/v1/nodes/{id}')
async def get_node(id: str):
    container = client.containers.get(id)
    return {'status': container.status}

@app.post('/api/v1/nodes/{id}')
async def operate_node(id: str, request: NodeOperateRequest):
    container = client.containers.get(id)
    res = {'code': PASS_CODE}

    act = request.action

    try:
        if act == 'start':
            container.start()
            res['msg'] = 'node started'
        elif act == 'restart':
            container.restart()
            res['msg'] = 'node restarted'
        elif act == 'stop':
            container.stop()
            res['msg'] = 'node stopped'
        elif act == 'delete':
            container.remove()
            res['msg'] = 'node deleted'
        elif act == 'update':
            env = {}

            if 'msp' in request.form:
                env['HLF_NODE_MSP'] = request.form.get('msp')

            if 'tls' in request.form:
                env['HLF_NODE_TLS'] = request.form.get('tls')

            if 'bootstrap_block' in request.form:
                env['HLF_NODE_BOOTSTRAP_BLOCK'] = request.form.get('bootstrap_block')

            if 'peer_config_file' in request.form:
                env['HLF_NODE_PEER_CONFIG'] = request.form.get('peer_config_file')

            if 'orderer_config_file' in request.form:
                env['HLF_NODE_ORDERER_CONFIG'] = request.form.get('orderer_config_file')

            container.exec_run(request.form.get('cmd'), detach=True, tty=True, stdin=True, environment=env)
            container.restart()
            res['msg'] = 'node updated'
        else:
            res['msg'] = 'undefined action'
    except:
        res['code'] = FAIL_CODE
        res['data'] = str(sys.exc_info()[0])
        res['msg'] = act + ' failed'
        logging.debug(res)
        raise

    return res