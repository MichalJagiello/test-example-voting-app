import os

import docker

from .container import Container
from .errors import ContainerNotFoundError, DockerHostError


class ContainerManager(object):

    CLIENT_CERT_FILE = 'cert.pem'
    CLIENT_KEY_FILE = 'key.pem'
    CA_CERT_FILE = 'ca.pem'

    def __init__(self, docker_host, docker_cert_path=None):
        if docker_cert_path:
            tls = self._create_tls_config(docker_cert_path)
        else:
            tls = None
        self._dc = docker.client.DockerClient(docker_host, tls=tls)

    def _create_tls_config(self, docker_cert_path):
        client_cert = (
            os.path.join(docker_cert_path, self.CLIENT_CERT_FILE),
            os.path.join(docker_cert_path, self.CLIENT_KEY_FILE)
        )
        ca_cert = os.path.join(docker_cert_path, self.CA_CERT_FILE)
        return docker.tls.TLSConfig(client_cert, ca_cert, verify=True)

    def get_container(self, name_or_id):
        try:
            container = self._dc.containers.get(name_or_id)
            return Container(container)
        except docker.errors.NotFound as e:
            raise ContainerNotFoundError(msg=e.msg)
        except docker.errors.APIError as e:
            raise DockerHostError(msg=e.msg)
