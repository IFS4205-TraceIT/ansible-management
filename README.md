# ansible-management

This repository houses the `Github Action` workflows and `Ansible` playbooks that automate the deployment and teardown of the `TraceIT` infrastructure.

Triggering a `Github Action` workflow is really ***simple***:
* Browse to the [`Actions` page](https://github.com/IFS4205-TraceIT/ansible-management/actions)
* Click on the target workflow on the left
* Click on `Run workflow` on the right
* Fill in the required information
* Hit the green `Run workflow` button
* Wait for a new workflow run to appear in the list with the yellow status

Once the status of the workflow run turns green :heavy_check_mark:, it means that the workflow had ran successfully. If the status turns red ❌, it means that a step in the workflow might have failed.

## Table of Contents

- [ansible-management](#ansible-management)
  - [Table of Contents](#table-of-contents)
  - [Day-to-Day operations](#day-to-day-operations)
    - [Unsealing the Vault](#unsealing-the-vault)
    - [Tearing down the `TraceIT` Infrastructure](#tearing-down-the-traceit-infrastructure)
    - [Deploying the `TraceIT` infrastructure](#deploying-the-traceit-infrastructure)
  - [Setting up](#setting-up)
    - [The operator workstation](#the-operator-workstation)
    - [The orchestrated hosts in the `prod` and `dev` environment](#the-orchestrated-hosts-in-the-prod-and-dev-environment)
    - [The `Vault` server](#the-vault-server)
    - [The Github Action Secrets](#the-github-action-secrets)

## Day-to-Day operations

### Unsealing the Vault

> The Vault becomes sealed when the Vault service is stopped, which is normally when the machine shuts down or restarts. Therefore, when the machine is first booted up again, the Vault would require unsealing to be performed.

Steps:
1. Run the [`Unseal Vault` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/unseal.yml) while specifying which environment to run it in and the corresponding unseal key for that environment.

### Tearing down the `TraceIT` Infrastructure

Steps:
1. Run the [`Teardown from environment` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/teardown.yml) while specifying which environment to execute it in.

### Deploying the `TraceIT` infrastructure

> It is **highly recommended** to perform the teardown of the `TraceIT` infrastructure first before attempting to deploy it. This is because the deployment workflow was designed to run on a clean environment (i.e no files / configurations / installations / processes from the previous deployment that may potentially affect the next).

Steps:
1. Perform [Unsealing the Vault](#unsealing-the-vault) if the Vault is not already unsealed.
2. Perform [Tearing down the `TraceIT` Infrastructure](#tearing-down-the-traceit-infrastructure) if this is not the first deployment or it is unclear whether the environment is clean.
3. Run the [`Deploy to environment` workflow](https://github.com/IFS4205-TraceIT/ansible-management/actions/workflows/deploy.yml) while specifying which environment to execute it in.

## Setting up

### The operator workstation

> Any Ubuntu environment **completely separate** from the virtual machines in the `prod` and `dev` environment can serve as the operator workstation. The operator workstation is used to run `Ansible` playbooks that are normally executed once or pertains to **really really sensitive** operations. Each environment should have their own separate operator workstation.

> The operator workstation will also house the `SSH` keypair whose private key is the **exact same** as the one stored as `SSH_PRIVATE_KEY` in the `Github Action` secrets of this repository. This also implies that the same `SSH` keypair is used in both the `prod` and `dev` environment.

Steps:

1. Install `ansible` by running the `setup_ansible.sh` script.
    ```bash
    ./setup_ansible.sh
    ```

2. If there is no existing `SSH` keypair yet, generate a new one.
    ```bash
    ssh-keygen -t ed25519 -f $HOME/.ssh/id_ed25519 -q -N ""
    ```
    > If there is already an existing `SSH` keypair, ensure that it meets the following requirements:
    > * Located in the `$HOME/.ssh` directory with the name  `id_ed25519` and configured with the right permissions.
    > * Has no passphrase configured on it

3. Add the contents of the private key to `Github Action` secrets as `SSH_PRIVATE_KEY`.

### The orchestrated hosts in the `prod` and `dev` environment

> Ensure that all hosts have a user called `sadm` that has `sudo` rights to run any commands as `root` and can be remotely logged in via `SSH`.

Steps:  

1.  Execute the `setup_hosts.yml` playbook:
    ```bash
    ANSIBLE_HOST_KEY_CHECKING=false ansible-playbook \
        -i hosts_prod.yml \
        -Kk \
        playbooks/setup_hosts.yml
    ```

### The `Vault` server

> Ensure the previous instance of `Vault` (if any) has been uninstalled.

Steps:

1) Deploy `Vault` to the server:
    ```bash
    ansible-playbook \
        -i hosts_prod.yml \
        playbooks/deploy_vault.yml
    ```
    
2) Save the unseal key **offline** outputted from step 1.

3) Save the initial root token to `Github Action` secrets as: 
    * `VAULT_TOKEN_DEV` if you are deploying in the `dev` environment
    * `VAULT_TOKEN_PROD` if you are deploying in the `prod` environment

4) Setup the PKI and configure Vault:
    ```bash
    export UNSEAL_KEY=<UNSEAL KEY 1> VAULT_TOKEN=<INITIAL ROOT TOKEN>
    ansible-playbook \
        -i hosts_prod.yml \
        playbooks/configure_pki.yml
    ```

    Base64-encode the client certificate as `VAULT_CA_CLIENTCERT_DEV` for `dev`, `VAULT_CA_CLIENTCERT_PROD` for `prod`.
    Base64-encode the client private key as `VAULT_CA_CLIENTKEY_DEV` for `dev`, `VAULT_CA_CLIENTKEY_PROD` for `prod`.
    Base64-encode the CA certificate as `VAULT_CA_CERT_DEV` for `dev`, `VAULT_CA_CERT_PROD` for `prod`.

5) Execute the rest:
    ```bash
    export UNSEAL_KEY=<UNSEAL KEY 1> VAULT_TOKEN=<INITIAL ROOT TOKEN>
    ansible-playbook \
        -i hosts_prod.yml \
        playbooks/certify_vault.yml && \
    ansible-playbook \
        -i hosts_prod.yml \
        playbooks/mount_vault.yml   
    ```

### The Github Action Secrets

1) Save the PAT (Personal Access Token) of the Github user that has read-only access to the organization, as `PAT`.

2) Save the necessary PKI components:
   * Base64-encode the client certificate as `VAULT_CA_CLIENTCERT_DEV` for `dev`, `VAULT_CA_CLIENTCERT_PROD` for `prod`.
   * Base64-encode the client private key as `VAULT_CA_CLIENTKEY_DEV` for `dev`, `VAULT_CA_CLIENTKEY_PROD` for `prod`.
   * Base64-encode the CA certificate as `VAULT_CA_CERT_DEV` for `dev`, `VAULT_CA_CERT_PROD` for `prod`.