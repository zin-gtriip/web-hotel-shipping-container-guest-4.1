#!/bin/sh

ssh -tt -oStrictHostKeyChecking=no phu@54.179.10.115 <<EOF
  cd GuestFacing/shippingconatiner_guest
  git pull
  docker-compose pull
  docker-compose up -d
EOF