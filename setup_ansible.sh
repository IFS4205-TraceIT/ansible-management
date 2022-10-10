#!/bin/bash -e

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

apt-add-repository -y ppa:ansible/ansible
apt-get update

apt-get install -y sshpass ansible ansible-lint
