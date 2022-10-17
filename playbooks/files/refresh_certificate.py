import hvac
import os
import json

def main():

    hostname = os.environ['HOSTNAME']
    ttl = os.environ['TTL']

    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN'],
        verify=os.environ['VAULT_CACERT'],
        cert=(os.environ['VAULT_CLIENTCERT'], os.environ['VAULT_CLIENTKEY'])
    )

    data = client.write(f'pki_int/issue/{hostname}', common_name=hostname, ttl=ttl)
    print(json.dumps(data))

if __name__ == "__main__":
    main()

