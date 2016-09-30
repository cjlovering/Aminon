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


##ANS##
# goo average: 3182/150 = 21.213333333
# pi average: 3026/150 = 20.173333333
# 8s average: 2793/150 = 18.62
