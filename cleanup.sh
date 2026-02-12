#!/bin/bash
#
# Removes all generated artifacts, keeping only source code.
#

rm -f BigProgram.jar BigProgram.cls BigProgram.jsa
rm -f BigProgram.java BigProgram.class
rm -f Worker*.java Worker*.class
rm -f instance_*.log
rm -rf build

echo "Cleaned up all generated artifacts."
