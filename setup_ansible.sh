#!/bin/bash -e

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

apt-get update

apt-get install -y sshpass ansible