#!/bin/bash

# If an argument was given use it as the working directory
if [ $# -eq 1 ]
then
  cd $1
fi

# Search for runnable executables
FILES=$(ls *.ini | grep -v '^verify')
for inifile in $FILES
do
  line=$(grep ^"opcounter = " $inifile)
  extract=${line##opcounter = }
  UPPER=10
  if [ $extract -eq 1 ]
  then
    UPPER=1
  fi
  COUNT=0
  while [ $COUNT -lt $UPPER ]; do
    exec=${inifile%.ini}
    MAXCORES=68
    CORE=0
    while [ $CORE -lt $MAXCORES ]; do
		hwloc-bind core:$CORE -- numactl --membind 1 ./$exec $inifile &
		CORE=$((CORE + 1))
	done
	wait
    COUNT=$((COUNT + 1))
  done
done
