from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from resource import get_docker_client
from config import FAIL_CODE, PASS_CODE, STORAGE_PATH, TEMPLATE_PATH
import os
import shutil
import yaml
import glob

router = APIRouter()

client = get_docker_client()


class CACreateRequest(BaseModel):
    ca_type: str
    name: str
    CSR_CN: str
    CSR_HOSTS: str


@router.post("/api/v1/ca")
def create_ca(request: CACreateRequest):
    if request.ca_type != "fabric-ca":
        res = {"code": FAIL_CODE, "data": {}, "msg": "type error"}
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_400_BAD_REQUEST
        )

    # Prepare the fabric-ca-server home directory
    ca_server_home = f"{STORAGE_PATH}/fabric-ca-servers/{request.name}"
    if os.path.exists(ca_server_home):
        res = {"code": FAIL_CODE, "data": {}, "msg": "name repeat"}
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_400_BAD_REQUEST
        )
    print(ca_server_home)
    os.mkdir(ca_server_home)

    # Start a Fabric CA container with default fabric-ca-server config

    # 1. Prepare the fabric-ca-server config file
    with open(f"{TEMPLATE_PATH}/fabric-ca-server-config.yaml", "r") as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        config["affiliations"][request.name] = {
            "name": request.name,
            "department": request.name,
            "displayName": request.name,
            "caname": request.name,
        }
        # print(config.keys())
        config["csr"]["cn"] = request.CSR_CN
        config["csr"]["hosts"] = request.CSR_HOSTS.split(",") + ["localhost"]
        config["csr"]["ca"]["pathlength"] = 0
        config["registry"]["identities"][0]["name"] = "admin"
        config["registry"]["identities"][0]["pass"] = "adminpw"
        config["version"] = "1.5.7"

    # 2. Write the config file to the ca_server_home
    with open(f"{ca_server_home}/fabric-ca-server-config.yaml", "w") as f:
        yaml.dump(config, f)

    # 2. Start the fabric-ca-server container
    try:
        container = client.containers.create(
            image="hyperledger/fabric-ca",
            command="fabric-ca-server start -b admin:adminpw -d",
            name=f"{request.name}-fabric-ca-server",
            ports={"7054/tcp": 7054},
            environment={
                "FABRIC_CA_SERVER_HOME": "/etc/hyperledger/fabric-ca-server",
                "FABRIC_CA_SERVER_TLS_ENABLED": "false",
                "FABRIC_CA_SERVER_CSR_CN": request.CSR_CN,
                "FABRIC_CA_SERVER_CSR_HOSTS": request.CSR_HOSTS,
                "FABRIC_CA_SERVER_DEBUG": "true",
            },
            volumes={
                os.path.abspath(ca_server_home): {
                    "bind": "/etc/hyperledger/fabric-ca-server",
                    "mode": "rw",
                }
            },
        )
    except Exception as e:
        print(e)
        res = {"code": FAIL_CODE, "data": {}, "msg": "create ca failed"}
        # delete the ca_server_home
        shutil.rmtree(ca_server_home)
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return JSONResponse(
        content={"res": {"code": PASS_CODE, "data": {}, "msg": "create ca success"}},
        status_code=status.HTTP_200_OK,
    )


class CAOperationRequest(BaseModel):
    command: str


@router.post("/api/v1/ca/{name}/operation")
def ca_operation(name: str, request: CAOperationRequest):
    command = request.command
    if command == "start":
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            container.start()
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "start ca failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"res": {"code": PASS_CODE, "data": {}, "msg": "start ca success"}},
            status_code=status.HTTP_200_OK,
        )
    elif command == "stop":
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            container.stop()
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "stop ca failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"res": {"code": PASS_CODE, "data": {}, "msg": "stop ca success"}},
            status_code=status.HTTP_200_OK,
        )


@router.delete("/api/v1/ca/{name}")
def delete_ca(name: str):
    # stop and rm container
    try:
        container = client.containers.get(f"{name}-fabric-ca-server")
        container.stop()
        container.remove()
    except Exception as e:
        # return JSONResponse(
        #     content={"res": {"code": FAIL_CODE, "data": {}, "msg": "rm container failed"}},
        #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        # )
        pass

    ca_server_home = f"{STORAGE_PATH}/fabric-ca-servers/{name}"
    if not os.path.exists(ca_server_home):
        res = {"code": FAIL_CODE, "data": {}, "msg": "name not exist"}
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_400_BAD_REQUEST
        )
    # using root user to rm the ca_server_home
    
    shutil.rmtree(ca_server_home)

    res = {"code": PASS_CODE, "data": {}, "msg": "delete ca success"}
    return JSONResponse(content={"res": res}, status_code=status.HTTP_200_OK)


@router.get("/api/v1/ca/{name}")
def get_ca(name: str):
    ca_server_home = f"{STORAGE_PATH}/fabric-ca-servers/{name}"
    if not os.path.exists(ca_server_home):
        res = {"code": FAIL_CODE, "data": {}, "msg": "name not exist"}
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_400_BAD_REQUEST
        )
    res = {"code": PASS_CODE, "data": {}, "msg": "get ca success"}
    # check container status
    try:
        container = client.containers.get(f"{name}-fabric-ca-server")
        if container.status == "running":
            res["data"]["status"] = "running"
        else:
            res["data"]["status"] = "stopped"
    except Exception as e:
        res["data"]["status"] = "stopped"
    return JSONResponse(content={"res": res}, status_code=status.HTTP_200_OK)


@router.get("/api/v1/ca")
def list_ca():
    ca_server_home = f"{STORAGE_PATH}/fabric-ca-servers"
    # get all ca in STORAGE_PATH
    ca_list = [
        {
            "name": name,
        }
        for name in os.listdir(ca_server_home)
    ]
    for ca in ca_list[:]:
        try:
            container = client.containers.get(f"{ca['name']}-fabric-ca-server")
            if container.status == "running":
                ca["status"] = "running"
            else:
                ca["status"] = "stopped"
        except Exception as e:
            # NOT FOUND
            ca["status"] = "stopped"
    res = {
        "code": PASS_CODE,
        "data": {"ca_list": ca_list},
        "msg": "get ca list success",
    }
    return JSONResponse(content={"res": res}, status_code=status.HTTP_200_OK)


# access CA


class CAAccessRequest(BaseModel):
    name: str
    command: str
    args: str


@router.post("/api/v1/ca/access")
def access_ca(request: CAAccessRequest):
    name = request.name
    command = request.command
    args = request.args
    if command == "enroll":
        # enroll
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            # set fabric-ca-client-home
            export_command = f"export FABRIC_CA_CLIENT_HOME=/etc/hyperledger/fabric-ca-server/client/{args} ; export FABRIC_CA_CLIENT_MSPDIR=msp ; export FABRIC_CA_CLIENT_TLS_CERTFILES=/etc/hyperledger/fabric-ca-server/ca-cert.pem " 
            # enroll some identity
            exec_command = f'''bash -c '{export_command}; fabric-ca-client enroll -u http://{args}:{args}pw@localhost:7054;chmod -R 777 /etc/hyperledger/fabric-ca-server/client' '''
            exec_result = container.exec_run(exec_command, privileged=True)
            print(exec_result.output.decode())
            content = {
                "pk": "",
                "cert": "",
            }
            # set priviledge

            # get pk and cert
            folder_path = f"{STORAGE_PATH}/fabric-ca-servers/{name}/client/{args}/msp/keystore/"
            files = glob.glob(os.path.join(folder_path, "*_sk"))
            files.sort(key=os.path.getmtime)
            latest_file = files[-1]
            with open(latest_file, "r") as f:
                content["pk"] = f.read()
            with open(f"{STORAGE_PATH}/fabric-ca-servers/{name}/client/{args}/msp/signcerts/cert.pem", "r") as f:
                content["cert"] = f.read()
        except Exception as e:
            print(e)
            res = {"code": FAIL_CODE, "data": {}, "msg": "enroll failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"res": {"code": PASS_CODE, "data": {
                "pk": content["pk"],
                "cert": content["cert"],
            }, "msg": "enroll success"}},
            status_code=status.HTTP_200_OK,
        )
    elif command.startswith("register"):
        # register
        register_type = command.split("_")[1]
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            enroll_self_command="fabric-ca-client enroll -u http://admin:adminpw@localhost:7054"
            exec_command = f'''bash -c '{enroll_self_command}; fabric-ca-client register --id.name {args} --id.secret {args}pw --id.type {register_type} -u http://admin:adminpw@localhost:7054'  '''
            exec_result = container.exec_run(exec_command)
            print(exec_result.output.decode())
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "register failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"res": {"code": PASS_CODE, "data": {}, "msg": "register success"}},
            status_code=status.HTTP_200_OK,
        )
    elif command == "revoke":
        # revoke
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            exec_command = f"fabric-ca-client revoke --id.name {args} -u http://admin:adminpw@localhost:7054"
            container.exec_run(exec_command)
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "revoke failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"res": {"code": PASS_CODE, "data": {}, "msg": "revoke success"}},
            status_code=status.HTTP_200_OK,
        )
    elif command == "list":
        # list
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            exec_command = (
                f"fabric-ca-client identity list -u http://admin:adminpw@localhost:7054"
            )
            result = container.exec_run(exec_command)
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "list failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        res = {
            "code": PASS_CODE,
            "data": {"list": result.output.decode()},
            "msg": "list success",
        }
        return JSONResponse(
            content={"res": res},
            status_code=status.HTTP_200_OK,
        )
    elif command == "get":
        # get
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            exec_command = (
                f"fabric-ca-client identity list -u http://admin:adminpw@localhost:7054"
            )
            result = container.exec_run(exec_command)
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "get failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        res = {
            "code": PASS_CODE,
            "data": {"list": result.output.decode()},
            "msg": "get success",
        }
        return JSONResponse(
            content={"res": res},
            status_code=status.HTTP_200_OK,
        )
    elif command == "remove":
        # remove
        try:
            container = client.containers.get(f"{name}-fabric-ca-server")
            exec_command = (
                f"rm -rf /etc/hyperledger/fabric-ca-server/msp/keystore/{args}-sk"
            )
            result = container.exec_run(exec_command)
        except Exception as e:
            res = {"code": FAIL_CODE, "data": {}, "msg": "remove failed"}
            return JSONResponse(
                content={"res": res}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        res = {
            "code": PASS_CODE,
            "data": {"list": result.output.decode()},
            "msg": "remove success",
        }
        return JSONResponse(
            content={"res": res},
            status_code=status.HTTP_200_OK,
        )
    else:
        res = {"code": FAIL_CODE, "data": {}, "msg": "command error"}
        return JSONResponse(
            content={"res": res}, status_code=status.HTTP_400_BAD_REQUEST
        )
