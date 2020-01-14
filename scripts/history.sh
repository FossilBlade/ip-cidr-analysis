#!/bin/bash
#
# address a.b.c.d
IFS='.' read -r -a address <<< "$1"

# echo $1
# ping: count 1, wait 1sec, no DNS, only output summary line
IFS="," read -r -a pingresult <<< `ping -c 1 -W 1 -n -q $1 | grep -A 2 statistics`
echo $1 "Ping result: " ${pingresult[1]}  >> "${2}"

# check for reverse DNS; there could be multiples, so use an array
mapfile -t PTR < <(dig PTR ${address[3]}.${address[2]}.${address[1]}.${address[0]}.in-addr.arpa +short +tries=1 +time=3)

if [ $PTR ]; then
    echo "$1 Reverse DNS record found:  " $PTR  >> "${2}"
    for names in "${PTR[@]}"
      do
#        mapfile -t FWD < <(dig A $names +short +tries=1 +time=3)
#        echo "$1 A records for $names found: $FWD " >> "${2}"
         echo "$1 A records for $names found: " `dig A $names +short +tries=1 +time=3` | xargs  >> "${2}"
         sleep 1s
      done 

#    for i in "${FWD[@]}"
#	do echo  "$1 Forward lookup for $PTR is $i"  >> "${2}"
#	done

else echo "$1 no PTR record found. "  >> "${2}"
fi


exit 0

