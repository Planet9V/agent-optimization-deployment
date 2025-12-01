#!/bin/bash
# Simple hourly research executor
# Just runs your prompt once per hour

PROMPT_FILE="/home/jim/2_OXOT_Projects_Dev/Agents_Special/Prompt_Critical_Sector_Infrastrure.md"
LOG_DIR="/home/jim/2_OXOT_Projects_Dev/docs/Hourly_Critical_Infrastructure_Research_Claude/logs"
KB_DIR="/home/jim/2_OXOT_Projects_Dev/docs/Hourly_Critical_Infrastructure_Research_Claude/kb"

# Create directories if needed
mkdir -p "$LOG_DIR"
mkdir -p "$KB_DIR"

# Get current timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOUR_ID=$(( $(date +%s) / 3600 ))

echo "===========================================" >> "$LOG_DIR/hourly_research.log"
echo "Starting research cycle: $TIMESTAMP" >> "$LOG_DIR/hourly_research.log"
echo "Hour ID: $HOUR_ID" >> "$LOG_DIR/hourly_research.log"
echo "===========================================" >> "$LOG_DIR/hourly_research.log"

# Calculate rotation (as specified in prompt)
SECTOR_IDX=$(( HOUR_ID % 13 ))
SUBSECTOR_IDX=$(( HOUR_ID % 7 ))
FACILITY_IDX=$(( HOUR_ID % 5 ))

# Execute the prompt via Claude Code CLI (if available) or via API
# Option 1: Using Claude Code CLI with full path for cron compatibility
cat "$PROMPT_FILE" | /home/jim/.nvm/versions/node/v22.15.0/bin/claude --print >> "$LOG_DIR/research_${TIMESTAMP}.log" 2>&1

# Option 2: Using Claude API directly (if preferred)
# python3 /path/to/claude_api_runner.py --prompt-file "$PROMPT_FILE"

echo "Research cycle complete: $TIMESTAMP" >> "$LOG_DIR/hourly_research.log"
