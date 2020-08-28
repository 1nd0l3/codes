#!/bin/bash

####################
# author: 1nd0l3
# date: 20191122
# purpose: script to scan for live nodes
# run it from your home or add to path; modify to desire
####################

# pass first arg to variable PREFIX
PREFIX=$1
echo 'Scanning '$PREFIX.'0/24...'

# better to allow a range for seq, even if working 1-5 in example
rng=$(seq 0 255)

# loop thru subnet ip's
for num in $rng
	do
	TARGET=$PREFIX'.'$num
	ping -bc 1 $TARGET > /dev/null && echo $TARGET 'is live' >> ~/live_hosts.txt || echo $TARGET 'is down' >> ~/down_hosts.txt
	done

echo '********************'
echo '********************'
echo 'Live hosts found:'
cat ~/live_hosts.txt
echo 'Data is stored in: ~/live_hosts.txt'
echo '--------------------'
echo 'Hosts not found are stored in: ~/down_hosts.txt'
echo '--------------------'
echo 'Finished scanning. Bye!'


