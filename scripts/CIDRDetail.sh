#!/bin/bash
#
#
# This script takes a range of IPv4 addresses and checks a bunch of
# information about them. Results are written to a file called "resultsfile"
# 
# To get a summary of the findings, run summarize-results.sh

if [ "$#" != "1" ]; then
  echo -e "Usage example: ./CIDRDetail.sh 192.0.2.0/24 \n"
  exit 1
else

  CIDR="$1"

#### Split argument into CIDR
IFS='/'
read -r -a ARRCIDR <<< "$1"
startaddr=${ARRCIDR[0]}
mask=${ARRCIDR[1]}
IFS='.'
read -r -a ARRstartaddr <<< "$startaddr"

outputfile="outputfile-"$startaddr"-"$mask
rm resultsfile-${1}
rm $outputfile

#### check routing history for full block
#### Removed, because ./lastroute.sh starts with first /24 in range
# IFS='T"' read -r -a LastRoute <<< `curl -s https://stat.ripe.net/data/routing-status/data.json?resource="$1" | grep -A 4 last_seen`

# if [ "${LastRoute[13]}" ]; then
#     echo -e "$1 Full block last seen in routing table: ${LastRoute[13]} \n\r " >> "$outputfile"
#   else
#     echo -e "$1 Full block never seen in routing table \n\r " >> "$outputfile"
#fi

# Need end octets
invmask=$((32-$mask))
numaddr=$((2**$invmask))
echo $numaddr
endA+=$(($numaddr/256/256/256+${ARRstartaddr[0]}))
echo -e $endA
endB=$(($numaddr/256/256+${ARRstartaddr[1]}))
endC=$(($numaddr/256+${ARRstartaddr[2]}))
endD=$(($numaddr+${ARRstartaddr[3]}))
echo -e "$endA.$endB.$endC.$endD\n"

for ((a=${ARRstartaddr[0]};a<=$endA;a++));
  do
    for ((b=${ARRstartaddr[1]};b<=$endB;b++));
      do 
        for ((c=${ARRstartaddr[2]};c<=$endC;c++));
          do
#### check reputation databases for each /24 
            mapfile -t blacklisted < <(grep "$a\.$b\.$c\." blacklists/*)
FS='T"' read -r -a getDate <<< ${LastRoute[3]}
            if [ "${blacklisted[1]}" ]; then
               for bl in "${blacklisted[@]}"
                 do echo "$a.$b.$c. blacklisted in: " `grep $a.$b.$c. blacklists/*`  >> "$outputfile"
                 done
            else echo "$a.$b.$c.0 not found in blacklists" >> "$outputfile"

#### check routing history for each /24
            ./lastroute.sh $a.$b.$c.0 "$outputfile" &
#		echo "$a.$b.$c.0 $outputfile"

            fi

            for ((d=${ARRstartaddr[3]};d<=$endD;d++));
              do
                ~/bin/NetDetails/history.sh $a.$b.$c.$d "$outputfile" & 
#                 echo $a.$b.$c.$d
#                 echo "Hello, World! \n" 

              done
# need to do > 45 /24s per minute to finish a /8 in 24 hours
            sleep 2s
          done
      done
  done


fi

