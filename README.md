# ansible-management

## Install `ansible`

```bash
chmod +x setup_ansible.sh
sudo ./setup_ansible.sh
```

## Prepare remote hosts for orchestration

```bash
ansible-playbook playbooks/setup_hosts.yml \
    -i hosts_prod.yaml \
    -K
```

## To deploy PostgreSQL TDE to database hosts

```bash
export TDE_KEY=<TDE_KEY> \
    DB_HOSTS=<IP/HOSTNAME> \
    ARTIFACT_URL=<ARTIFACT_URL> \
    ARTIFACT_HASH=<ARTIFACT_HASH> \
    GITHUB_TOKEN=<GITHUB_TOKEN>
ansible-playbook playbooks/deploy_postgres.yml \
    -i hosts_prod.yaml 
    -K
```
