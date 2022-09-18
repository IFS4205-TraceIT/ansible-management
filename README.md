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
ansible-playbook playbooks/deploy_postgres.yml \
    -i hosts_prod.yaml \
    -e "encryption_key=<TDE_KEY> db_hosts=<IPS/HOSTNAMES> git_pat=<GITHUB_TOKEN> download_url=<ARTIFACT_URL> download_sha256=<ARTIFACT_HASH>" \
    -K

# Example:
# ansible-playbook playbooks/deploy_postgres.yml \
#     -i hosts_dev.yaml \
#     -e "encryption_key=... db_hosts=... git_pat=... download_url=https://api.github.com/repos/IFS4205-TraceIT/PostgreSQL-TDE/releases/assets/77121185 download_sha256=e201f63b12624ea2e85dfeb0e8e8728ce2e8840fbea9c30aef8a2bea483e8066" \
#     -K
```
