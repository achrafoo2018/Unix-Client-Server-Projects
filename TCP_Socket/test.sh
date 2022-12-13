#!/bin/bash
for i in $(seq 1 $1) # $1 is the first argument passed to the script
do
	./Client & # Run client in background and redirect output to /dev/null
done
echo $1 clients finished successfully.
