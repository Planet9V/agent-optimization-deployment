#!/usr/bin/env python3
"""
E01 APT Ingestion Completion Monitor
Polls ingestion state until 100% complete, then reports final metrics
"""

import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
STATE_FILE = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json")
STATS_FILE = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_final_stats.json")
TOTAL_EXPECTED = 1701
CHECK_INTERVAL = 120  # 2 minutes

class CompletionMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = None
        self.last_count = 0

    def load_state(self):
        """Load current ingestion state"""
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR loading state: {e}")
            return None

    def load_final_stats(self):
        """Load final statistics"""
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"WARNING: Could not load final stats: {e}")
            return None

    def calculate_rate(self, current_count):
        """Calculate processing rate"""
        if self.last_check is None:
            return 0.0

        time_diff = (datetime.now() - self.last_check).total_seconds()
        if time_diff == 0:
            return 0.0

        count_diff = current_count - self.last_count
        return count_diff / time_diff * 60  # docs per minute

    def estimate_completion(self, current_count, rate):
        """Estimate time to completion"""
        if rate <= 0:
            return "Unknown"

        remaining = TOTAL_EXPECTED - current_count
        minutes_left = remaining / rate

        if minutes_left < 0:
            return "Complete"

        completion_time = datetime.now() + timedelta(minutes=minutes_left)
        return completion_time.strftime("%H:%M:%S")

    def print_progress(self, state):
        """Print progress report"""
        processed = len(state.get('processed_documents', []))
        failed = len(state.get('failed_documents', []))
        percentage = (processed / TOTAL_EXPECTED) * 100

        rate = self.calculate_rate(processed)
        eta = self.estimate_completion(processed, rate)

        elapsed = datetime.now() - self.start_time
        elapsed_str = str(elapsed).split('.')[0]  # Remove microseconds

        print(f"\n{'='*70}")
        print(f"E01 APT INGESTION PROGRESS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        print(f"Processed:    {processed:4d} / {TOTAL_EXPECTED} ({percentage:5.1f}%)")
        print(f"Failed:       {failed:4d}")
        print(f"Rate:         {rate:5.1f} docs/min")
        print(f"Elapsed:      {elapsed_str}")
        print(f"ETA:          {eta}")
        print(f"Last updated: {state.get('last_updated', 'Unknown')}")
        print(f"{'='*70}\n")

        # Update tracking variables
        self.last_check = datetime.now()
        self.last_count = processed

        return processed >= TOTAL_EXPECTED

    def print_final_report(self):
        """Print final completion report"""
        state = self.load_state()
        stats = self.load_final_stats()

        if not state:
            print("ERROR: Could not load final state")
            return

        processed = len(state.get('processed_documents', []))
        failed = len(state.get('failed_documents', []))
        total_time = datetime.now() - self.start_time

        print(f"\n{'='*70}")
        print(f"✅ E01 APT INGESTION COMPLETE")
        print(f"{'='*70}")
        print(f"\nFINAL DOCUMENT COUNT:")
        print(f"  Processed:     {processed}")
        print(f"  Failed:        {failed}")
        print(f"  Total:         {processed + failed}")
        print(f"  Expected:      {TOTAL_EXPECTED}")

        if stats:
            print(f"\nNEO4J METRICS:")
            print(f"  Total Nodes:   {stats.get('pipeline_stats', {}).get('nodes_merged', 0):,}")
            print(f"  Relationships: {stats.get('pipeline_stats', {}).get('relationships_created', 0):,}")
            print(f"  Entities:      {stats.get('pipeline_stats', {}).get('entities_extracted', 0):,}")

            validation = stats.get('pipeline_stats', {}).get('validation', {})
            print(f"\nVALIDATION:")
            print(f"  Baseline:      {validation.get('baseline_nodes', 0):,}")
            print(f"  Current:       {validation.get('total_nodes', 0):,}")
            print(f"  Added:         {validation.get('total_nodes', 0) - validation.get('baseline_nodes', 0):,}")

        print(f"\nPROCESSING TIME:")
        print(f"  Total:         {str(total_time).split('.')[0]}")
        print(f"  Average Rate:  {processed / (total_time.total_seconds() / 60):.1f} docs/min")
        print(f"\nCompleted at:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

    def monitor(self):
        """Main monitoring loop"""
        print(f"Starting E01 APT Ingestion Monitor")
        print(f"Target: {TOTAL_EXPECTED} documents")
        print(f"Check interval: {CHECK_INTERVAL} seconds\n")

        while True:
            state = self.load_state()

            if not state:
                print("Waiting for state file...")
                time.sleep(CHECK_INTERVAL)
                continue

            # Check progress
            is_complete = self.print_progress(state)

            if is_complete:
                print("\n🎉 Ingestion reached 100%!")
                time.sleep(5)  # Wait for final stats to be written
                self.print_final_report()
                break

            # Wait before next check
            time.sleep(CHECK_INTERVAL)

def main():
    monitor = CompletionMonitor()

    try:
        monitor.monitor()
    except KeyboardInterrupt:
        print("\n\nMonitoring interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
