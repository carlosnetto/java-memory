#!/bin/bash
#
# Automates the AppCDS workflow for BigProgram:
#   1. Run BigProgram.jar briefly to dump the loaded class list
#   2. Create the shared archive (.jsa) from the class list
#
# After running this script, launch instances with:
#   java -Xshare:on -XX:SharedArchiveFile=BigProgram.jsa -jar BigProgram.jar
#

set -e

JAR="BigProgram.jar"
CLASS_LIST="BigProgram.cls"
ARCHIVE="BigProgram.jsa"
TMPLOG=$(mktemp)
trap 'rm -f "$TMPLOG"' EXIT

if [ ! -f "$JAR" ]; then
    echo "$JAR not found. Run ./CreateBigProgram.sh first."
    exit 1
fi

echo "=== Step 1: Dumping loaded class list ==="
java -Xshare:off -XX:DumpLoadedClassList="$CLASS_LIST" -jar "$JAR" > "$TMPLOG" 2>&1 &
PID=$!
echo "Waiting for classes to load (PID $PID)..."
while ! grep -q "Entering keep-warm loop" "$TMPLOG" 2>/dev/null; do
    sleep 1
done
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
echo "Class list written to $CLASS_LIST ($(wc -l < "$CLASS_LIST") classes)"

echo "=== Step 2: Creating shared archive ==="
java -Xshare:dump -cp "$JAR" -XX:SharedClassListFile="$CLASS_LIST" -XX:SharedArchiveFile="$ARCHIVE"
echo "Archive created: $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"

echo ""
echo "=== Done ==="
echo "Launch instances with:"
echo "  java -Xshare:on -XX:SharedArchiveFile=$ARCHIVE -jar $JAR"
