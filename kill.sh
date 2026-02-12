#!/bin/bash
#
# Kills all running BigProgram instances.
#

pkill -f "java.*BigProgram" && echo "All BigProgram instances killed." || echo "No BigProgram instances running."
