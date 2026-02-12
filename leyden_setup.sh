#!/bin/bash
#
# Automates the Project Leyden AOT cache workflow for BigProgram:
#   1. Training run to record an execution profile (.aotconf)
#   2. Create the AOT cache (.aot) from the profile
#
# After running this script, launch instances with:
#   java -XX:AOTCache=BigProgram.aot -jar BigProgram.jar
#

set -e

JAR="BigProgram.jar"
AOT_CONF="BigProgram.aotconf"
AOT_CACHE="BigProgram.aot"
TMPLOG=$(mktemp)
trap 'rm -f "$TMPLOG"' EXIT

if [ ! -f "$JAR" ]; then
    echo "$JAR not found. Run ./CreateBigProgram.sh first."
    exit 1
fi

echo "=== Step 1: Training run (recording execution profile) ==="
java -XX:AOTMode=record -XX:AOTConfiguration="$AOT_CONF" -jar "$JAR" > "$TMPLOG" 2>&1 &
PID=$!
echo "Waiting for classes to load (PID $PID)..."
while ! grep -q "Entering keep-warm loop" "$TMPLOG" 2>/dev/null; do
    sleep 1
done
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
echo "AOT configuration written to $AOT_CONF ($(du -h "$AOT_CONF" | cut -f1))"

echo "=== Step 2: Creating AOT cache ==="
java -XX:AOTMode=create -XX:AOTConfiguration="$AOT_CONF" -XX:AOTCache="$AOT_CACHE" -cp "$JAR"
echo "AOT cache created: $AOT_CACHE ($(du -h "$AOT_CACHE" | cut -f1))"

echo ""
echo "=== Done ==="
echo "Launch instances with:"
echo "  java -XX:AOTCache=$AOT_CACHE -jar $JAR"
