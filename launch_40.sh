#!/bin/bash

JAR="BigProgram.jar"
ARCHIVE="BigProgram.jsa"
JAVA_OPTS=""

if [ ! -f "$JAR" ]; then
    echo "BigProgram.jar not found. Run ./compile.sh first."
    exit 1
fi

if [ -f "$ARCHIVE" ]; then
    echo "AppCDS archive found, launching with shared archive."
    JAVA_OPTS="-Xshare:on -XX:SharedArchiveFile=$ARCHIVE"
else
    echo "No AppCDS archive found. Run appcds_setup.sh first for faster startup."
fi

echo "Launching 40 instances of BigProgram..."
for i in {1..40}
do
   echo "Starting instance $i..."
   java $JAVA_OPTS -jar "$JAR" > "instance_$i.log" 2>&1 &
done

echo "40 instances launched. Use 'jps' or 'ps' to see them."
echo "To stop all instances: pkill -f BigProgram"
