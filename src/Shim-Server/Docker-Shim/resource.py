import docker

def get_docker_client_factory():
    client = docker.from_env()
    def get_docker_client():
        return client
    return get_docker_client

get_docker_client = get_docker_client_factory()