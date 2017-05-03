from manager import ContainerManager


if __name__ == "__main__":

    cm = ContainerManager(
        "tcp://192.168.99.101:2376",
        "/home/michalj/.docker/machine/machines/example-votin-app-microservices"
    )
    container = cm.get_container('db')
    container.start()
