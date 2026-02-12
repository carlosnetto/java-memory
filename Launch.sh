#!/bin/bash
#
# Launches N instances of BigProgram.
# Usage: ./Launch.sh <number_of_instances>
#

NUM=${1:?Usage: ./Launch.sh <number_of_instances>}
JAR="BigProgram.jar"
AOT_CACHE="BigProgram.aot"
ARCHIVE="BigProgram.jsa"
JAVA_OPTS=""

if [ ! -f "$JAR" ]; then
    echo "BigProgram.jar not found. Run ./CreateBigProgram.sh first."
    exit 1
fi

if [ -f "$AOT_CACHE" ]; then
    echo "Leyden AOT cache found, launching with AOT cache."
    JAVA_OPTS="-XX:AOTCache=$AOT_CACHE"
elif [ -f "$ARCHIVE" ]; then
    echo "AppCDS archive found, launching with shared archive."
    JAVA_OPTS="-Xshare:on -XX:SharedArchiveFile=$ARCHIVE"
else
    echo "No AOT cache or AppCDS archive found. Run leyden_setup.sh or appcds_setup.sh first."
fi

echo "Launching $NUM instances of BigProgram..."
for (( i=1; i<=NUM; i++ )); do
    echo "Starting instance $i..."
    java $JAVA_OPTS -jar "$JAR" > "instance_$i.log" 2>&1 &
done

echo "$NUM instances launched. Use 'jps' or 'ps' to see them."
echo "To stop all instances: ./kill.sh"
