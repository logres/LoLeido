import requests

from Orchestration.Identity.config import config
from Orchestration.Identity.models import Environment, Membership

# External API Execution

# Fabric CA

def create_ca(environment_id, membership_id, name):
    environment = Environment.objects.get(id=environment_id)
    membership = Membership.objects.get(id=membership_id)
    # Some External API
    url = "http://{}:{}/api/v1/ca".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    data = {
        "name": name,
        "environment_id": environment_id,
        "membership_id": membership_id,
    }
    response = requests.post(url, data=data)
    return response

def delete_ca(ca_id):
    url = "http://{}:{}/api/v1/ca/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], ca_id)
    response = requests.delete(url)
    return response

def get_ca(ca_id):
    url = "http://{}:{}/api/v1/ca/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], ca_id)
    response = requests.get(url)
    return response

def get_ca_list():
    url = "http://{}:{}/api/v1/ca".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    response = requests.get(url)
    return response

def register_peer():
    pass

def register_orderer():
    pass

# Fabric Node

## Peer

def create_fabric_peer(environment_id, membership_id, name):
    environment = Environment.objects.get(id=environment_id)
    membership = Membership.objects.get(id=membership_id)
    # Some External API
    url = "http://{}:{}/api/v1/peer".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    data = {
        "name": name,
        "environment_id": environment_id,
        "membership_id": membership_id,
    }
    response = requests.post(url, data=data)
    return response

def delete_fabric_peer(peer_id):
    url = "http://{}:{}/api/v1/peer/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], peer_id)
    response = requests.delete(url)
    return response

def get_fabric_peer(peer_id):
    url = "http://{}:{}/api/v1/peer/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], peer_id)
    response = requests.get(url)
    return response

def get_fabric_peer_list():
    url = "http://{}:{}/api/v1/peer".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    response = requests.get(url)
    return response

## Orderer

def create_fabric_orderer(environment_id, membership_id, name):
    environment = Environment.objects.get(id=environment_id)
    membership = Membership.objects.get(id=membership_id)
    # Some External API
    url = "http://{}:{}/api/v1/orderer".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    data = {
        "name": name,
        "environment_id": environment_id,
        "membership_id": membership_id,
    }
    response = requests.post(url, data=data)
    return response

def delete_fabric_orderer(orderer_id):
    url = "http://{}:{}/api/v1/orderer/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], orderer_id)
    response = requests.delete(url)
    return response

def get_fabric_orderer(orderer_id):
    url = "http://{}:{}/api/v1/orderer/{}".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"], orderer_id)
    response = requests.get(url)
    return response

def get_fabric_orderer_list():
    url = "http://{}:{}/api/v1/orderer".format(config["Shim-Server"]["host"], config["Shim-Server"]["port"])
    response = requests.get(url)
    return response

# Fabric Operation

def create_channel():
    pass

def join_channel():
    pass

def install_chaincode():
    pass

def instantiate_chaincode():
    pass

def invoke_chaincode():
    pass

def instantiate_chaincode():
    pass