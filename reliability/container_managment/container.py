import docker

from .errors import ContainerExecError, ContainerStatusError


class ContainerStatus(object):

    RUNNING = 'running'
    EXITED = 'exited'


class Container(object):

    def __init__(self, container):
        self._container = container

    @property
    def status(self):
        return self._container.status

    def start(self):
        if self.status == ContainerStatus.RUNNING:
            raise ContainerStatusError('Container already running')
        try:
            self._container.start()
        except docker.errors.ContainerError:
            raise ContainerExecError
        except docker.errors.APIError:
            raise DockerHostError

    def stop(self):
        if self.status == ContainerStatus.EXITED:
            raise ContainerStatusError('Container already exited')
        try:
            self._container.stop()
        except docker.errors.APIError:
            raise DockerHostError
