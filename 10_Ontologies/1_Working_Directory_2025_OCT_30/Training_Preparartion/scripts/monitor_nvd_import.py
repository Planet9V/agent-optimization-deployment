#!/usr/bin/env python3
"""
NVD IMPORT PROGRESS MONITOR
Real-time monitoring of CVE→CWE relationship import progress

Usage:
    python3 monitor_nvd_import.py [--interval 30]

Author: AEON Protocol
Date: 2025-11-07
"""

import json
import time
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

CHECKPOINT_FILE = "import_checkpoint.json"
LOG_FILE = "complete_data_import_nvd.log"
UPDATE_INTERVAL = 30  # seconds


def load_checkpoint():
    """Load current checkpoint data."""
    if not os.path.exists(CHECKPOINT_FILE):
        return None

    try:
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return None


def format_duration(seconds):
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def calculate_eta(processed, total, start_time):
    """Calculate estimated time to completion."""
    if processed == 0:
        return "Unknown"

    elapsed = time.time() - start_time
    rate = processed / elapsed
    remaining = total - processed
    eta_seconds = remaining / rate if rate > 0 else 0

    return format_duration(eta_seconds)


def display_progress(checkpoint, start_time=None):
    """Display formatted progress information."""
    if not checkpoint:
        print("No checkpoint data available yet...")
        return

    stats = checkpoint.get('stats', {})
    timestamp = checkpoint.get('timestamp', 'Unknown')

    print("\n" + "=" * 80)
    print(f"NVD IMPORT PROGRESS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Basic stats
    processed = stats.get('processed', 0)
    total = stats.get('total_cves', 0) or 1000  # Default to test mode
    cves_with_cwe = stats.get('cves_with_cwe', 0)
    relationships = stats.get('relationships_created', 0)
    errors = stats.get('errors', 0)
    skipped = stats.get('skipped', 0)

    print(f"\n📊 PROCESSING STATUS:")
    print(f"  Processed:         {processed:,} / {total:,} CVEs ({100*processed/total:.1f}%)")
    print(f"  CVEs with CWE:     {cves_with_cwe:,} ({100*cves_with_cwe/processed:.1f}% of processed)" if processed > 0 else "  CVEs with CWE:     0")
    print(f"  Relationships:     {relationships:,}")
    print(f"  Errors:            {errors:,}")
    print(f"  Skipped:           {skipped:,}")

    # Missing CWEs
    cwes_missing = stats.get('cwes_missing', {})
    if cwes_missing:
        print(f"\n⚠️  MISSING CWEs:")
        print(f"  Unique CWEs:       {len(cwes_missing)}")
        print(f"  Total occurrences: {sum(cwes_missing.values())}")

        # Top 10 most common missing CWEs
        top_missing = sorted(cwes_missing.items(), key=lambda x: x[1], reverse=True)[:10]
        if top_missing:
            print(f"\n  Top missing CWEs:")
            for cwe_id, count in top_missing:
                print(f"    {cwe_id}: {count} occurrences")

    # Performance metrics
    if start_time and processed > 0:
        elapsed = time.time() - start_time
        rate = processed / elapsed
        eta = calculate_eta(processed, total, start_time)

        print(f"\n⚡ PERFORMANCE:")
        print(f"  Processing rate:   {rate:.2f} CVE/s ({rate*60:.1f} CVE/min)")
        print(f"  Elapsed time:      {format_duration(elapsed)}")
        print(f"  Estimated ETA:     {eta}")
        print(f"  Est. completion:   {(datetime.now() + timedelta(seconds=(total-processed)/rate if rate > 0 else 0)).strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n🕐 Last checkpoint:  {timestamp}")
    print("=" * 80)


def tail_log(lines=10):
    """Display last N lines of log file."""
    if not os.path.exists(LOG_FILE):
        return

    try:
        with open(LOG_FILE, 'r') as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:]

            print(f"\n📄 RECENT LOG ENTRIES (last {lines}):")
            print("-" * 80)
            for line in recent:
                print(line.rstrip())
            print("-" * 80)
    except Exception as e:
        print(f"Error reading log: {e}")


def monitor_continuous(interval=UPDATE_INTERVAL):
    """Continuously monitor progress."""
    print("🔍 Starting continuous monitoring...")
    print(f"📊 Update interval: {interval} seconds")
    print("⌨️  Press Ctrl+C to stop\n")

    start_time = time.time()
    last_processed = 0

    try:
        while True:
            checkpoint = load_checkpoint()
            display_progress(checkpoint, start_time)

            # Check if import is complete
            if checkpoint:
                stats = checkpoint.get('stats', {})
                processed = stats.get('processed', 0)
                total = stats.get('total_cves', 0) or 1000

                if processed >= total:
                    print("\n✅ IMPORT COMPLETE!")
                    tail_log(20)
                    break

                # Check if stuck (no progress)
                if processed == last_processed and processed > 0:
                    print("\n⚠️  WARNING: No progress detected. Import may have stalled.")

                last_processed = processed

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n⏸️  Monitoring stopped by user")
        if checkpoint:
            display_progress(checkpoint, start_time)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Monitor NVD import progress')
    parser.add_argument('--interval', type=int, default=UPDATE_INTERVAL,
                       help=f'Update interval in seconds (default: {UPDATE_INTERVAL})')
    parser.add_argument('--once', action='store_true',
                       help='Display current status once and exit')
    parser.add_argument('--log', type=int, metavar='LINES',
                       help='Display last N lines of log file')

    args = parser.parse_args()

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    if args.log:
        tail_log(args.log)
    elif args.once:
        checkpoint = load_checkpoint()
        display_progress(checkpoint)
        tail_log(10)
    else:
        monitor_continuous(args.interval)


if __name__ == "__main__":
    main()
