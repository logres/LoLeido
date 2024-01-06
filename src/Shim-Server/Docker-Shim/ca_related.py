from fastapi import APIRouter
from fastapi import  status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from resource import get_docker_client
from config import FAIL_CODE, PASS_CODE, STORAGE_PATH, TEMPLATE_PATH
import os
import shutil
import yaml

router = APIRouter()

client = get_docker_client()

class CACreateRequest(BaseModel):
    ca_type: str
    name: str
    CSR_CN: str
    CSR_HOSTS: str

@router.post('/api/v1/ca')
def create_ca(request: CACreateRequest):
    if request.ca_type != 'fabric-ca':
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'type error'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    
    # Prepare the fabric-ca-server home directory
    ca_server_home = f'{STORAGE_PATH}/fabric-ca-servers/{request.name}'
    if os.path.exists(ca_server_home):
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'name repeat'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    print(ca_server_home)
    os.mkdir(ca_server_home)

    # Start a Fabric CA container with default fabric-ca-server config

    # 1. Prepare the fabric-ca-server config file
    with open (f'{TEMPLATE_PATH}/fabric-ca-server-config.yaml', 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        config['affiliations'][request.name] = {
            'name': request.name,
            'department': request.name,
            'displayName': request.name,
            'caname': request.name
        }
        config['csr']['cn'] = request.CSR_CN
        config['csr']['hosts'] = request.CSR_HOSTS.split(',')

    # 2. Write the config file to the ca_server_home
    with open(f'{ca_server_home}/fabric-ca-server-config.yaml', 'w') as f:
        yaml.dump(config, f)

    # 2. Start the fabric-ca-server container
    try:
        container = client.containers.create(
            image='hyperledger/fabric-ca',
            command='fabric-ca-server start -b admin:adminpw -d',
            name= f'{request.name}-fabric-ca-server',
            ports={'7054/tcp': 7054},
            environment={
                'FABRIC_CA_SERVER_HOME': '/etc/hyperledger/fabric-ca-server',
                'FABRIC_CA_SERVER_TLS_ENABLED': 'true',
                'FABRIC_CA_SERVER_CSR_CN': request.CSR_CN,
                'FABRIC_CA_SERVER_CSR_HOSTS': request.CSR_HOSTS,
                'FABRIC_CA_SERVER_DEBUG': 'true'
            },
            volumes={
                os.path.abspath(ca_server_home): {
                    'bind': '/etc/hyperledger/fabric-ca-server',
                    'mode': 'rw'
                }
            }
        )
    except Exception as e:
        print(e)
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'create ca failed'}
        # delete the ca_server_home
        shutil.rmtree(ca_server_home)
        return JSONResponse(content={'res': res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CAOperationRequest(BaseModel):
    command : str

@router.put('/api/v1/ca/{id}')
def update_ca(command: str):

    ca_server_home = f'{STORAGE_PATH}/fabric-ca-servers/{command}'
    if not os.path.exists(ca_server_home):
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'name not exist'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    res = {'code': PASS_CODE, 'data': {}, 'msg': 'update ca success'}
    return JSONResponse(content={'res': res}, status_code=status.HTTP_200_OK)

@router.delete('/api/v1/ca')
def delete_ca(name: str):
    ca_server_home = f'{STORAGE_PATH}/fabric-ca-servers/{name}'
    if not os.path.exists(ca_server_home):
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'name not exist'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    shutil.rmtree(ca_server_home)
    res = {'code': PASS_CODE, 'data': {}, 'msg': 'delete ca success'}
    return JSONResponse(content={'res': res}, status_code=status.HTTP_200_OK)

@router.get('/api/v1/ca')
def get_ca(name: str):
    ca_server_home = f'{STORAGE_PATH}/fabric-ca-servers/{name}'
    if not os.path.exists(ca_server_home):
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'name not exist'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    res = {'code': PASS_CODE, 'data': {}, 'msg': 'get ca success'}
    return JSONResponse(content={'res': res}, status_code=status.HTTP_200_OK)

@router.get('/api/v1/ca/list')
def list_ca():
    ca_server_home = f'{STORAGE_PATH}/fabric-ca-servers'
    if not os.path.exists(ca_server_home):
        res = {'code': FAIL_CODE, 'data': {}, 'msg': 'name not exist'}
        return JSONResponse(content={'res': res}, status_code=status.HTTP_400_BAD_REQUEST)
    res = {'code': PASS_CODE, 'data': {}, 'msg': 'get ca success'}
    return JSONResponse(content={'res': res}, status_code=status.HTTP_200_OK)