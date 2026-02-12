#!/bin/bash

# Compile the program first
echo "Compiling BigProgram.java..."
javac BigProgram.java

echo "Launching 40 instances of BigProgram..."
for i in {1..40}
do
   # Launch in background, redirecting input from a pipe to keep them alive
   # and output to a log file.
   echo "Starting instance $i..."
   sleep 0.1 | java BigProgram > "instance_$i.log" 2>&1 &
done

echo "40 instances launched. Use 'jps' or 'ps' to see them."
echo "Note: These instances will wait for input. To kill all of them, use 'pkill -f BigProgram'."
