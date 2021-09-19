#!/bin/sh

ssh -tt -oStrictHostKeyChecking=no -i /home/phuwai/.ssh/id_rsa phu@54.179.10.115 <<EOF
  cd GuestFacing/shippingconatiner_guest
  git pull
  docker-compose pull
  docker-compose up -d
EOF