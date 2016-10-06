#!/bin/bash

IP="$1"

wget $IP --no-dns-cache

if[[ $? -eq 0 ]]; then
    echo "SCAN ATTACK WORKED" >> scan_results.txt
fi
