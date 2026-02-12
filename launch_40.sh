#!/bin/bash

# Compile the program first
echo "Compiling BigProgram.java..."
javac BigProgram.java

echo "Launching 40 instances of BigProgram..."
for i in {1..40}
do
   echo "Starting instance $i..."
   java BigProgram > "instance_$i.log" 2>&1 &
done

echo "40 instances launched. Use 'jps' or 'ps' to see them."
echo "To stop all instances: pkill -f BigProgram"
