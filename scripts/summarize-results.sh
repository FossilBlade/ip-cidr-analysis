#!/bin/bash

# sort -o resultsfile outputfile
# rm outputfile

if [ "$#" != "1" ]; then
  echo -e "Usage: summarize-results.sh <startaddress> \n"
  exit 1
else

sort -o "resultsfile-$1" "outputfile-$1"
# rm "outputfile-$1"

echo "Summary for $1:"
echo "   " `grep "Last seen" "resultsfile-$1" | wc -l` " /24s have appeared in the routing table. Look for \"Last seen\" in the results."
echo "   " `grep blacklisted "resultsfile-$1" | wc -l` " /24s appeared in blacklists. Look for \"blacklisted\" in the results."
echo "   " `grep "1 received" "resultsfile-$1" | wc -l` "addresses responded to ping. Look for \"1 received\" in the results."

echo "   " `grep Forward "resultsfile-$1" | wc -l` "addresses had reverse DNS (PTR) records for host names that also resolve to another address. The DNS for these should be updated. Look for \"Forward lookup\" in the results."


fi
