#!/bin/bash

IP="$1"

START=$(date +"%s.%3N")
#echo $START

dig $IP  

END=$(date +"%s.%3N")
#echo $END

#DIFF=$(($END - $START))

#echo $DIFF
echo $START
echo $END
#cat $DIFF >> times.txt

#cat $INDEX | grep '*.png' >> scan_results.txt

#if[[ $? -eq 0 ]]; then
#    echo "SCAN ATTACK WORKED" >> scan_results.txt
#fi


#ls > /dev/null
