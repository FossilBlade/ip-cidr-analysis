#!/bin/bash

cd ~/NetDetails/blacklists/
wget -O Cymru.bogon-reference.html https://www.team-cymru.com/bogon-reference.html
wget -O Abuse.CH.sslipblacklist.csv https://sslbl.abuse.ch/blacklist/sslipblacklist.csv
wget -O Abuse.CH.sslipblacklist_aggressive.csv https://sslbl.abuse.ch/blacklist/sslipblacklist_aggressive.csv
wget -O Abuse.CH.ransomwaretracker.TL_PS_IPBL.txt https://ransomwaretracker.abuse.ch/downloads/TL_PS_IPBL.txt
wget -O Abuse.CH.feodotracker.ipblocklist  https://feodotracker.abuse.ch/blocklist/?download=ipblocklist
wget -O Abuse.CH.feodotracker.badips  https://feodotracker.abuse.ch/blocklist/?download=badips
wget -O Abuse.CH.zeustracker.badips  https://zeustracker.abuse.ch/blocklist.php?download=badips
wget -O Abuse.CH.zeustracker.ipblocklist  https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist

wget -O Spamhaus.drop https://www.spamhaus.org/drop/drop.txt 
wget -O TalosIntelligence https://talosintelligence.com/documents/ip-blacklist
wget -O InterServer http://rbl.interserver.net/iprbl.txt
wget -O EmergingThreats-compromised-ips.txt https://rules.emergingthreats.net/blockrules/compromised-ips.txt
wget -O EmergingThreats-block-ips.txt https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt
wget -O Blocklist.de http://lists.blocklist.de/lists/dnsbl/all.list
wget -O ISC-SANS.block.txt https://feeds.dshield.org/block.txt
wget -O ISC-SANS.suspiciousdomains_Low.txt https://dshield.org/feeds/suspiciousdomains_Low.txt
wget -O ISC-SANS.suspiciousdomains_Medium.txt https://dshield.org/feeds/suspiciousdomains_Medium.txt
wget -O ISC-SANS.suspiciousdomains_High.txt https://dshield.org/feeds/suspiciousdomains_High.txt
wget -O CIArmy.SentinelIPS.badguys.txt http://cinsscore.com/list/ci-badguys.txt

