# Simple Hourly Research Setup

## What You Asked For
Run your prompt every hour. The prompt already handles:
- ✅ Rotating through sectors/subsectors/facilities
- ✅ Generating 2 reports per hour
- ✅ Saving with timestamps (never overwrites)
- ✅ Cross-referencing
- ✅ Session tracking

## Setup (5 minutes)

### 1. Add to Crontab
```bash
crontab -e
```

Add this line:
```
0 * * * * /home/jim/2_OXOT_Projects_Dev/docs/Hourly_Critical_Infrastructure_Research_Claude/scripts/run_hourly_research.sh
```

### 2. Done
That's it. Your prompt runs every hour at :00.

## How It Works

1. Cron triggers script at top of each hour
2. Script calculates rotation (Hour ID % 13, % 7, % 5)
3. Script executes your prompt
4. Your prompt does the research and generates reports
5. Reports save to `kb/sectors/[SECTOR]/` with timestamps
6. Next hour, repeat with different sector/subsector/facility

## Knowledge Accumulation

Your prompt already handles this with timestamps in filenames:
- `facility-large-20251102-14.md` (Hour 1)
- `facility-large-20251107-17.md` (Hour 2, different time)
- Files never overwritten = cumulative knowledge

## Files Generated

Your prompt creates:
```
kb/sectors/[SECTOR]/
  ├── architectures/facility-[TYPE]-[TIMESTAMP].md
  ├── control-systems/[SECTOR]-control-[TIMESTAMP].md
  └── network/network-pattern-[TYPE]-[TIMESTAMP].md

kb/tracking/session-[HOUR_ID].json
```

## Logs

Check execution:
```bash
tail -f /home/jim/2_OXOT_Projects_Dev/docs/Hourly_Critical_Infrastructure_Research_Claude/logs/hourly_research.log
```

## That's It

No vector stores, no knowledge graphs, no swarm coordination needed.
Your prompt already does everything. Just runs hourly.
