#!/bin/bash

SLEEPTIME=$1

hostname
pwd
whoami

for i in {1..5}
do 
 echo "performing iteration $i"
 sleep $SLEEPTIME
done
