# ansible-management

## Install `ansible`

```bash
chmod +x setup_ansible.sh
sudo ./setup_ansible.sh
```

## Prepare remote hosts for orchestration

```bash
ssh-keygen -t ed25519
export PUBLIC_KEY="$(cat ~/.ssh/id_ed25519.pub)"
ansible-playbook playbooks/setup_hosts.yml \
    -i hosts_prod.yml \
    -Kk
```

## To deploy Vault to secret hosts

```bash
export GITHUB_TOKEN=<GITHUB_TOKEN> \ 
    KEY_SHARES=<KEY_SHARES> \
    KEY_THRESHOLD=<KEY_THRESHOLD>
ansible-playbook playbooks/deploy_vault.yml \
    -i hosts_prod.yml 
```

## To deploy PostgreSQL TDE to database hosts

```bash
export TDE_KEY=<TDE_KEY> \
    DB_HOSTS=<IP/HOSTNAME> \
    ARTIFACT_URL=<ARTIFACT_URL> \
    ARTIFACT_SHA256=<ARTIFACT_SHA256> \
    GITHUB_TOKEN=<GITHUB_TOKEN>
ansible-playbook playbooks/deploy_postgres.yml \
    -i hosts_prod.yml 
```

## To deploy Django to app hosts

```bash
export GITHUB_TOKEN=<GITHUB_TOKEN> \
    REPOSITORY=<REPOSITORY> \
ansible-playbook playbooks/deploy_django.yml \
    -i hosts_prod.yml 
```

## To deploy NGINX to proxy hosts

```bash
ansible-playbook playbooks/deploy_nginx.yml \
    -i hosts_prod.yml 
```


## Workflow

### Preparing workstation

1) Have an environment with `ansible` installed.
    ```bash
    sudo ./setup_ansible.sh
    ```

### Setting up remote hosts for ansible orchestration

1) Setup SSH keypair:
    ```bash
    ssh-keygen -t ed25519
    ```

    Save the public and private keys into this repository's Github Secrets:

    ```bash
    SSH_PRIVATE_KEY: <Contents of SSH private key>
    SSH_PUBLIC_KEY: <Contents of SSH public key>
    ```

2) Setup remote hosts:
    ```bash
    ANSIBLE_HOST_KEY_CHECKING=false ansible-playbook -i hosts_prod.yml playbooks/setup_hosts.yml -Kk
    ```

### Setting up `vault`

1) Deploy `vault`:
    ```bash
    GITHUB_TOKEN=... ansible-playbook -i hosts_prod.yml playbooks/deploy_vault.yml
    ```
    **Save the unseal key offline** and save the initial root token into this repository's Github Secrets:
    ```
    VAULT_TOKEN: <Initial Root Token>
    ```

2) Unseal `vault`:
    ```bash
    UNSEAL_KEY=... ansible-playbook -i hosts_prod.yml playbooks/unseal_vault.yml
    ```
