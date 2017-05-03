

class ContainerManagerError(Exception):
    """
    Base exception
    """

class ContainerNotFoundError(ContainerManagerError):
    """
    Raises when requested container wasn't found
    """

class ContainerStatusError(ContainerManagerError):
    """
    Raises when requested container's action is impossible because of
    the container status
    """

class ContainerExecError(ContainerManagerError):
    """
    Raises on container's execution exception
    """

class DockerHostError(ContainerManagerError):
    """
    Raises when connection error occurs
    """
