import docker
client = docker.from_env()
container = client.containers.get("container_name_or_id")
output = container.exec_run("command")
print(output.output.decode("utf-8"))




