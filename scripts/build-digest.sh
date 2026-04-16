#!/bin/bash
# build-digest.sh — Inject JSON data into digest template
# Usage: ./scripts/build-digest.sh <data.json> <output.html>

set -e

DATA_FILE="$1"
OUTPUT="$2"

if [ -z "$DATA_FILE" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <data.json> <output.html>"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="$SCRIPT_DIR/../templates/digest-template.html"

if [ ! -f "$TEMPLATE" ]; then
    echo "Error: Template not found at $TEMPLATE"
    exit 1
fi

if [ ! -f "$DATA_FILE" ]; then
    echo "Error: Data file not found at $DATA_FILE"
    exit 1
fi

# Create output directory if needed
mkdir -p "$(dirname "$OUTPUT")"

# Replace __DIGEST_DATA__ placeholder with JSON content
awk -v datafile="$DATA_FILE" '
/__DIGEST_DATA__/ {
    while ((getline line < datafile) > 0) print line
    close(datafile)
    next
}
{ print }
' "$TEMPLATE" > "$OUTPUT"

echo "Built: $OUTPUT"
