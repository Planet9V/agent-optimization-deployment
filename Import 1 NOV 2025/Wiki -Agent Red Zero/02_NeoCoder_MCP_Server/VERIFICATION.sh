#!/bin/bash
echo "=========================================="
echo "NeoCoder Wiki Migration Verification"
echo "=========================================="
echo ""

# Count files
total_files=$(find . -name "*.md" | wc -l | tr -d ' ')
echo "✓ Total markdown files: $total_files"

# Check for oversized files
oversized=$(find . -name "*.md" -exec sh -c 'lines=$(wc -l < "$1" | tr -d " "); if [ "$lines" -gt 500 ]; then echo "$1 ($lines lines)"; fi' _ {} \;)

if [ -z "$oversized" ]; then
    echo "✓ All files within 500-line limit"
else
    echo "⚠️  Files exceeding 500 lines:"
    echo "$oversized"
fi

# Count categories
categories=$(find . -type d -depth 1 | wc -l | tr -d ' ')
echo "✓ Total categories: $categories"

# Check frontmatter
files_with_frontmatter=$(grep -l "^---$" *.md */*.md 2>/dev/null | wc -l | tr -d ' ')
echo "✓ Files with frontmatter: $files_with_frontmatter"

# List category file counts
echo ""
echo "Category breakdown:"
for dir in $(find . -type d -depth 1 | sort); do
    count=$(find "$dir" -name "*.md" | wc -l | tr -d ' ')
    dirname=$(basename "$dir")
    echo "  $dirname: $count files"
done

echo ""
echo "=========================================="
echo "Verification complete!"
echo "=========================================="
