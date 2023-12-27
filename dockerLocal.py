import subprocess

RED_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'

def get_container_names():
    try:
        result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        container_names = result.stdout.strip().split('\n')
        return container_names
    except Exception as e:
        return []

def check_docker_directory(container_name):
    try:
        command = f'docker exec -it {container_name} /bin/bash -c "[ -d /root] && [ -d /root/.docker ] && echo success || echo fail"'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout.strip()
    except Exception as e:
        return "fail"

def check_dockercfg_directory(container_name):
    try:
        command = f'docker exec -it {container_name} /bin/bash -c "[ -d /root] && [ -d /root/.dockercfg ] && echo success || echo fail"'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout.strip()
    except Exception as e:
        return "fail"

def main():
    container_names = get_container_names()
    
    if not container_names:
        print("No running containers found.")
        return

    for container_name in container_names:
        result = check_docker_directory(container_name)
        result_dockercfg = check_dockercfg_directory(container_name)
        print(f"Container: {container_name}, Result .docker: {RED_COLOR}{result}{RESET_COLOR}, Result .dockercfg: {RED_COLOR}{result_dockercfg}{RESET_COLOR}")

if __name__ == "__main__":
    main()
