#!/bin/bash
rm 'train.txt' 'test.txt'
dirs=$(find dataset ! -path dataset -type d)
for d in $dirs
do
	echo "working on $d"
	find $d -type f ! -name "*.txt" | shuf  > temp.txt;
	length=$(cat temp.txt | wc -l)
	tenpercent=$(( $length / 10)) 
	ninetypercent=$(( $length - $tenpercent))
	head -n $tenpercent 'temp.txt' >> 'test.txt' 
	tail -n $ninetypercent 'temp.txt' >> 'train.txt'
	rm 'temp.txt'
done 
