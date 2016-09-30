#!/bin/bash
x=0
while [ $x -le 149 ]
do
 dig 8.8.8.8
 x=$(( $x + 1 ))
done

# sh qr.sh | grep Query >> site.cut
# subl site.cut #eliminate non numerics
# awk '{ sum += $1 } END { print sum }' site.cut
# sort -t= -nr -k3 site.cut| tail -1 # yeilds the min
# sort -t= -nr -k3 site.cut| head -1 # yeilds the max

##ANS##
# goo average: 3182/150 = 21.213333333 min: 10 max: 41
# pi average: 3026/150 = 20.173333333 min: 12 max: 97
# 8s average: 2793/150 = 18.62 		 min: 14 max: 99
