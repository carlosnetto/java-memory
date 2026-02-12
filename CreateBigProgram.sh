#!/bin/bash
#
# Generates Java sources, compiles, packages into BigProgram.jar,
# and cleans up all intermediate .java and .class files.
#

set -e

echo "=== Generating Java sources ==="
python3 CreateBigProgram.py

echo "=== Compiling ==="
mkdir -p build
javac -d build BigProgram.java Worker*.java

echo "=== Packaging JAR ==="
jar cfe BigProgram.jar BigProgram -C build .

echo "=== Cleaning up ==="
rm -rf build
rm -f BigProgram.java Worker*.java Worker*.class BigProgram.class

echo "Done: BigProgram.jar ($(du -h BigProgram.jar | cut -f1))"
echo "Run with: java -jar BigProgram.jar"
