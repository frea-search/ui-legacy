#!/usr/bin/env bash

sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https git
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update

sudo apt install -y curl caddy redis-server

git clone https://git.sda1.net/frea/search
sudo -H ./search/utils/searx.sh install all
