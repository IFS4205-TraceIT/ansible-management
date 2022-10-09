# ansible-management

This repository houses the `Github Action` workflows and `Ansible` playbooks that automate the deployment and teardown of the `TraceIT` infrastructure.

Triggering a `Github Action` workflow is really ***simple***:
* Browse to the [`Actions` page](https://github.com/IFS4205-TraceIT/ansible-management/actions)
* Click on the target workflow on the left
* Click on `Run workflow` on the right
* Fill in the required information
* Hit the green `Run workflow` button
* Wait for a new workflow run to appear in the list with the yellow status

Once the status of the workflow run turns green, it means that the workflow had ran successfully. If the status turns red, it means that a step in the workflow might have failed.

# Table of Contents
1. [Day-to-Day operations](#day-to-day-operations)

## Day-to-Day operations

### Unsealing the Vault

> The Vault becomes sealed when the Vault service is stopped, which is normally when the machine shuts down or restarts. Therefore, when the machine is first booted up again, the Vault would require unsealing to be performed.

Steps:
1. Run the [`Unseal Vault` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/unseal.yml) while specifying which environment to run it in and the corresponding unseal key for that environment.

### Tearing down the `TraceIT` Infrastructure

Steps:
1. Run the [`Teardown from environment` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/teardown.yml) while specifying which environment to run it in.

### Deploying the `TraceIT` infrastructure

> It is **highly recommended** to perform the teardown of the `TraceIT` infrastructure first before attempting to deploy it. This is because the deployment workflow was designed to run on a clean environment (i.e no files / configurations / installations / processes from the previous deployment that may potentially affect the next).

Steps:
1. Perform [Unsealing the Vault](#unsealing-the-vault) if the Vault is not already unsealed.
2. Perform [Tearing down the `TraceIT` Infrastructure](#tearing-down-the-traceit-infrastructure) if this is not the first deployment or it is unclear whether the environment is clean.
3. Run the [`Deploy to environment` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/deploy.yml) while specifying which environment to run it in.

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
