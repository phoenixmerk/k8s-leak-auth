import subprocess
import json
import base64

RED_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'

def get_secrets(secret_type):
    result = subprocess.run(['kubectl', 'get', 'secrets', '--output=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return []

    secrets = json.loads(result.stdout)
    return [secret['metadata']['name'] for secret in secrets.get('items', []) if secret.get('type', '') == secret_type]

def get_secret_content(secret_name, field):
    result = subprocess.run(['kubectl', 'get', 'secret', secret_name, '--output=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    secret_info = json.loads(result.stdout)
    secret_data = secret_info.get('data', {}).get(field, '')
    return base64.b64decode(secret_data).decode('utf-8') if secret_data else None

def main():
    secret_types = ['kubernetes.io/dockerconfigjson', 'kubernetes.io/dockercfg']

    for secret_type in secret_types:
        secrets = get_secrets(secret_type)

        if not secrets:
            print(f"No secrets of type {secret_type} found.")
            continue

        for secret_name in secrets:
            print(f"Processing {secret_type} secret: {secret_name}")
            print("\n" + "=" * 50 + "\n")

            field = '.dockerconfigjson' if secret_type == 'kubernetes.io/dockerconfigjson' else '.dockercfg'
            content = get_secret_content(secret_name, field)

            if content is not None:
                print(f"Decoded {field} for {secret_name}:\n{RED_COLOR}{content}{RESET_COLOR}")
            else:
                print(f"No {field} field found in {secret_name}")

            print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()

