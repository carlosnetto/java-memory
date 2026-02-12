#!/bin/bash
#
# Generates Java sources, compiles, packages into BigProgram.jar,
# and cleans up all intermediate .java and .class files.
#

set -e

echo "=== Generating Java sources ==="
python3 CreateBigProgram.py

echo "=== Compiling Workers in batches ==="
mkdir -p build
BATCH_SIZE=20
workers=(Worker*.java)
total=${#workers[@]}
for (( i=0; i<total; i+=BATCH_SIZE )); do
    batch=("${workers[@]:i:BATCH_SIZE}")
    echo "  Compiling Worker$((i))..Worker$((i + ${#batch[@]} - 1)) (${#batch[@]} files)"
    javac -J-Xmx2g -d build "${batch[@]}"
done

echo "=== Compiling BigProgram ==="
javac -J-Xmx2g -d build -cp build BigProgram.java

echo "=== Packaging JAR ==="
jar cfe BigProgram.jar BigProgram -C build .

echo "=== Cleaning up ==="
rm -rf build
rm -f BigProgram.java Worker*.java Worker*.class BigProgram.class

echo "Done: BigProgram.jar ($(du -h BigProgram.jar | cut -f1))"
echo "Run with: java -jar BigProgram.jar"
