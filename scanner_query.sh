#!/bin/bash

IP="$1"

wget $IP

if[[ $? -eq 0 ]]; then
    echo "SCAN ATTACK WORKED"
fi