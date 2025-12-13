#!/usr/bin/env python3
"""
Monitor E01 APT ingestion until 100% complete.
Reports progress and final Neo4j metrics.
"""
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

def get_ingestion_state():
    """Read current ingestion state."""
    state_file = Path('/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json')
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return None

def get_neo4j_metrics():
    """Query Neo4j for final metrics."""
    try:
        result = subprocess.run(
            ['python3', '/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/query_neo4j_metrics.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return f"Error querying metrics: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def store_completion_hook():
    """Store completion in Claude Flow memory."""
    try:
        subprocess.run(
            ['npx', 'claude-flow@alpha', 'hooks', 'post-task', '--task-id', 'e01-complete'],
            check=False,
            capture_output=True
        )
    except Exception:
        pass  # Non-critical if hook fails

def main():
    """Monitor ingestion until complete."""
    target_docs = 1701
    check_interval = 180  # 3 minutes

    print(f"🔍 Monitoring E01 APT ingestion progress...")
    print(f"Target: {target_docs} documents")
    print(f"Check interval: {check_interval}s\n")

    iteration = 0
    while True:
        iteration += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        state = get_ingestion_state()
        if not state:
            print(f"[{timestamp}] ⚠️  No state file found, waiting...")
            time.sleep(check_interval)
            continue

        processed = len(state.get('processed_documents', []))
        percentage = (processed * 100 / target_docs) if target_docs > 0 else 0

        print(f"[{timestamp}] Check #{iteration}: {processed}/{target_docs} ({percentage:.1f}%)")

        # Check if complete
        if processed >= target_docs:
            print(f"\n✅ INGESTION COMPLETE!")
            print(f"   Total processed: {processed}/{target_docs}")
            print(f"   Completion time: {timestamp}")

            # Store completion hook
            store_completion_hook()

            # Get final Neo4j metrics
            print(f"\n📊 Querying final Neo4j metrics...")
            metrics = get_neo4j_metrics()
            print(metrics)

            # Final state details
            print(f"\n📝 Final State Summary:")
            print(f"   Processed: {len(state.get('processed_documents', []))}")
            print(f"   Failed: {len(state.get('failed_documents', []))}")
            if state.get('failed_documents'):
                print(f"\n❌ Failed documents:")
                for failed in state['failed_documents'][:10]:  # Show first 10
                    print(f"      - {failed}")
                if len(state['failed_documents']) > 10:
                    print(f"      ... and {len(state['failed_documents']) - 10} more")

            break

        # Continue monitoring
        time.sleep(check_interval)

    print(f"\n✨ Monitoring complete!")

if __name__ == '__main__':
    main()
