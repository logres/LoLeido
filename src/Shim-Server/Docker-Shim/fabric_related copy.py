from fastapi.responses import JSONResponse
from pydantic import BaseModel
from resource import get_docker_client
import sys
import logging
from fastapi import APIRouter, status
from config import STORAGE_PATH, PASS_CODE, FAIL_CODE

router = APIRouter()

client = get_docker_client()


class NodeCreateRequest(BaseModel):
    name: str
    msp: str
    tls: str
    bootstrap_block: str
    peer_config_file: str
    orderer_config_file: str
    type: str
    port_map: dict


@router.get("/api/v1/nodes")
def get_nodes(node_type: str = None):
    containers = client.containers.list()
    res = [
        container
        for container in containers
        if container.name.endswith("-fabric-node")
        and container.name.split("-")[1] == node_type
    ]
    res = [
        {"id": container.id, "name": container.name, "status": container.status}
        for container in res
    ]
    return JSONResponse(
        content={"res": {"code": PASS_CODE, "data": res, "msg": "success"}},
        status_code=status.HTTP_200_OK,
    )


@router.post("/api/v1/nodes")
def create_node(request: NodeCreateRequest):
    node_name = f"{request.name}-{request.type}-fabric-node"
    if request.type == "peer":
        try:
            container = client.containers.create(
                image="hyperledger/fabric-peer:2.5.0",
                command="peer node start",
                name=node_name,
                ports={},
                volumes={
                    f"{STORAGE_PATH}/fabric-nodes/{node_name}:/etc/hyperledger/fabric",
                },
                environment={
                    "FABRIC_LOGGING_SPEC": "DEBUG",
                    "FABRIC_CFG_PATH": "/etc/hyperledger/peercfg",
                    "CORE_PEER_TLS_ENABLED": "true",
                    "CORE_PEER_PROFILE_ENABLED": "true",
                    "CORE_PEER_TLS_CERT_FILE": "/etc/hyperledger/fabric/tls/server.crt",
                    "CORE_PEER_TLS_KEY_FILE": "/etc/hyperledger/fabric/tls/server.key",
                    "CORE_PEER_TLS_ROOTCERT_FILE": "/etc/hyperledger/fabric/tls/ca.crt",
                    "CORE_PEER_ID": node_name,
                    "CORE_PEER_ADDRESS": f"{node_name}:7051",
                    "CORE_PEER_LISTENADDRESS": "0.0.0.0:7051",
                    "CORE_PEER_CHAINCODEADDRESS": f"{node_name}:7052",
                    "CORE_PEER_CHAINCODELISTENADDRESS": "0.0.0.0:7052",
                    "CORE_PEER_GOSSIP_BOOTSTRAP": f"{node_name}:7051",
                    "CORE_PEER_GOSSIP_EXTERNALENDPOINT": f"{node_name}:7051",
                    "CORE_OPERATIONS_LISTENADDRESS": "0.0.0.0:17051",
                },
            )
        except Exception as e:
            return JSONResponse(
                content={"res": {"code": FAIL_CODE, "data": str(e), "msg": "failed"}},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    else:
        order_envs = {
            "FABRIC_LOGGING_SPEC": "DEBUG",
            "ORDERER_GENERAL_LISTENADDRESS": "0.0.0.0",
            "ORDERER_GENERAL_LISTENPORT": "7050",
            "ORDERER_GENERAL_GENESISMETHOD": "file",
            "ORDERER_GENERAL_LOCALMSPDIR": "/etc/hyperledger/fabric/msp",
            "ORDERER_GENERAL_GENESISFILE": "/etc/hyperledger/fabric/genesis.block",
            "ORDERER_GENERAL_TLS_ENABLED": "true",
            "ORDERER_GENERAL_TLS_PRIVATEKEY": "/etc/hyperledger/fabric/tls/server.key",
            "ORDERER_GENERAL_TLS_CERTIFICATE": "/etc/hyperledger/fabric/tls/server.crt",
            "ORDERER_GENERAL_TLS_ROOTCAS": "[/etc/hyperledger/fabric/tls/ca.crt]",
            "ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE": "/etc/hyperledger/fabric/tls/server.crt",
            "ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY": "/etc/hyperledger/fabric/tls/server.key",
            "ORDERER_GENERAL_CLUSTER_ROOTCAS": "[/etc/hyperledger/fabric/tls/ca.crt]",
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
            ports=port_map,
        )
    except:
        res["code"] = FAIL_CODE
        res["data"] = sys.exc_info()[0]
        res["msg"] = "creation failed"
        logging.debug(res)
        raise

    res["code"] = PASS_CODE
    res["data"]["status"] = "created"
    res["data"]["id"] = container.id
    res["data"][
        "public-grpc"
    ] = "127.0.0.1:7050"  # TODO: read the info from config file
    res["data"]["public-raft"] = "127.0.0.1:7052"
    res["msg"] = "node created"
    return JSONResponse(content=res)


@router.get("/api/v1/nodes/{name}")
async def get_node(name: str):
    container = client.containers.get(f"{name}-")
    return {"status": container.status}


class NodeOperateRequest(BaseModel):
    action: str
    form: dict


@router.post("/api/v1/nodes/{id}/operation")
async def operate_node(id: str, request: NodeOperateRequest):
    container = client.containers.get(id)
    res = {"code": PASS_CODE}

    act = request.action

    try:
        if act == "start":
            container.start()
            res["msg"] = "node started"
        elif act == "restart":
            container.restart()
            res["msg"] = "node restarted"
        elif act == "stop":
            container.stop()
            res["msg"] = "node stopped"
        elif act == "delete":
            container.remove()
            res["msg"] = "node deleted"
        elif act == "update":
            env = {}

            if "msp" in request.form:
                env["HLF_NODE_MSP"] = request.form.get("msp")

            if "tls" in request.form:
                env["HLF_NODE_TLS"] = request.form.get("tls")

            if "bootstrap_block" in request.form:
                env["HLF_NODE_BOOTSTRAP_BLOCK"] = request.form.get("bootstrap_block")

            if "peer_config_file" in request.form:
                env["HLF_NODE_PEER_CONFIG"] = request.form.get("peer_config_file")

            if "orderer_config_file" in request.form:
                env["HLF_NODE_ORDERER_CONFIG"] = request.form.get("orderer_config_file")

            container.exec_run(
                request.form.get("cmd"),
                detach=True,
                tty=True,
                stdin=True,
                environment=env,
            )
            container.restart()
            res["msg"] = "node updated"
        else:
            res["msg"] = "undefined action"
    except:
        res["code"] = FAIL_CODE
        res["data"] = str(sys.exc_info()[0])
        res["msg"] = act + " failed"
        logging.debug(res)
        raise

    return res
