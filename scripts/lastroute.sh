#!/bin/bash


# mapfile -t LastRoute < <(curl -s https://stat.ripe.net/data/routing-status/data.json?resource="$1" | grep -A 4 last_seen)
# echo ${LastRoute[3]}

IFS='T"' read -r -a LastRoute <<< `curl -s https://stat.ripe.net/data/routing-status/data.json?resource="$1" | grep -A 4 last_seen`

# echo ${LastRoute[0]} ${LastRoute[3]}
echo $LastRoute

# if [ "${LastRoute[3]}" = "}" ]; then
if [ "${LastRoute[13]}" ]; then
#    IFS='T"' read -r -a getDate <<< ${LastRoute[3]}
#    echo "$1 Last seen in routing table: ${getDate[3]} " 
    echo "$1 Last seen in routing table: ${LastRoute[13]} " 
   else
     echo "$1 never seen in routing table" 
fi

