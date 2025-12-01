#!/usr/bin/env python3
"""
Performance Dashboard - Real-time Streamlit dashboard for graph performance monitoring
"""

import time
from typing import Dict, List
from datetime import datetime, timedelta
from collections import deque
from neo4j import GraphDatabase
import logging

# Try to import Streamlit, provide fallback
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit not available. Install with: pip install streamlit")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceDashboard:
    """Real-time performance monitoring dashboard"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        # Historical data buffers
        self.query_history = deque(maxlen=100)
        self.latency_history = deque(maxlen=100)
        self.error_history = deque(maxlen=50)

    def close(self):
        self.driver.close()

    def collect_query_metrics(self) -> Dict:
        """Collect query performance metrics"""
        # Get recent query statistics
        query = '''
        // This requires query logging to be enabled
        // Placeholder implementation with synthetic metrics
        MATCH (n)
        WITH count(*) as node_count
        MATCH ()-[r]->()
        WITH node_count, count(r) as rel_count
        RETURN node_count, rel_count
        '''

        with self.driver.session() as session:
            start_time = time.time()

            try:
                result = session.run(query)
                record = result.single()

                latency_ms = (time.time() - start_time) * 1000

                metrics = {
                    "timestamp": datetime.now(),
                    "latency_ms": latency_ms,
                    "node_count": record["node_count"],
                    "rel_count": record["rel_count"],
                    "status": "success"
                }

                self.latency_history.append({
                    "time": datetime.now(),
                    "latency": latency_ms
                })

                return metrics

            except Exception as e:
                logger.error(f"Query failed: {e}")
                self.error_history.append({
                    "time": datetime.now(),
                    "error": str(e)
                })

                return {
                    "timestamp": datetime.now(),
                    "status": "error",
                    "error": str(e)
                }

    def get_system_metrics(self) -> Dict:
        """Get system resource metrics"""
        # This would integrate with Neo4j metrics endpoint
        # Placeholder implementation
        query = '''
        CALL dbms.queryJmx("org.neo4j:*") YIELD attributes
        RETURN attributes
        LIMIT 1
        '''

        with self.driver.session() as session:
            try:
                result = session.run(query)
                # Process JMX metrics
                # Placeholder values
                return {
                    "cpu_usage": 0.0,
                    "memory_usage_mb": 0.0,
                    "heap_usage_pct": 0.0,
                    "page_cache_usage_pct": 0.0
                }
            except:
                return {
                    "cpu_usage": 0.0,
                    "memory_usage_mb": 0.0,
                    "note": "JMX metrics not available"
                }

    def calculate_throughput(self) -> float:
        """Calculate query throughput (queries per second)"""
        if len(self.query_history) < 2:
            return 0.0

        # Get time span
        oldest = self.query_history[0]["timestamp"]
        newest = self.query_history[-1]["timestamp"]

        time_span = (newest - oldest).total_seconds()

        if time_span > 0:
            return len(self.query_history) / time_span
        else:
            return 0.0

    def calculate_error_rate(self) -> float:
        """Calculate error rate percentage"""
        if not self.query_history:
            return 0.0

        errors = sum(1 for q in self.query_history if q.get("status") == "error")
        return (errors / len(self.query_history)) * 100

    def get_latency_percentiles(self) -> Dict:
        """Calculate latency percentiles"""
        if not self.latency_history:
            return {}

        latencies = sorted([entry["latency"] for entry in self.latency_history])
        count = len(latencies)

        return {
            "p50": latencies[int(count * 0.50)] if count > 0 else 0,
            "p75": latencies[int(count * 0.75)] if count > 0 else 0,
            "p90": latencies[int(count * 0.90)] if count > 0 else 0,
            "p95": latencies[int(count * 0.95)] if count > 0 else 0,
            "p99": latencies[int(count * 0.99)] if count > 0 else 0
        }


def run_streamlit_dashboard():
    """Run Streamlit dashboard (requires streamlit package)"""
    if not STREAMLIT_AVAILABLE:
        print("Streamlit is not installed. Install with: pip install streamlit")
        print("Then run with: streamlit run performance_dashboard.py")
        return

    st.set_page_config(
        page_title="Threat Intel Performance Dashboard",
        page_icon="📊",
        layout="wide"
    )

    st.title("🔒 Cybersecurity Threat Intelligence - Performance Dashboard")

    # Initialize dashboard
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = PerformanceDashboard(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="password"
        )

    dashboard = st.session_state.dashboard

    # Create layout
    col1, col2, col3, col4 = st.columns(4)

    # Collect metrics
    query_metrics = dashboard.collect_query_metrics()
    system_metrics = dashboard.get_system_metrics()
    throughput = dashboard.calculate_throughput()
    error_rate = dashboard.calculate_error_rate()
    percentiles = dashboard.get_latency_percentiles()

    # Display metrics
    with col1:
        st.metric(
            "Query Latency",
            f"{query_metrics.get('latency_ms', 0):.2f} ms",
            delta=None
        )

    with col2:
        st.metric(
            "Throughput",
            f"{throughput:.2f} q/s",
            delta=None
        )

    with col3:
        st.metric(
            "Error Rate",
            f"{error_rate:.2f}%",
            delta=None,
            delta_color="inverse"
        )

    with col4:
        st.metric(
            "Graph Size",
            f"{query_metrics.get('node_count', 0):,} nodes",
            delta=None
        )

    # Latency chart
    st.subheader("📈 Query Latency Over Time")

    if dashboard.latency_history:
        import pandas as pd

        latency_df = pd.DataFrame([
            {
                "Time": entry["time"].strftime("%H:%M:%S"),
                "Latency (ms)": entry["latency"]
            }
            for entry in dashboard.latency_history
        ])

        st.line_chart(latency_df.set_index("Time"))

    # Latency percentiles
    st.subheader("📊 Latency Percentiles")

    if percentiles:
        perc_col1, perc_col2, perc_col3, perc_col4, perc_col5 = st.columns(5)

        with perc_col1:
            st.metric("P50", f"{percentiles['p50']:.2f} ms")
        with perc_col2:
            st.metric("P75", f"{percentiles['p75']:.2f} ms")
        with perc_col3:
            st.metric("P90", f"{percentiles['p90']:.2f} ms")
        with perc_col4:
            st.metric("P95", f"{percentiles['p95']:.2f} ms")
        with perc_col5:
            st.metric("P99", f"{percentiles['p99']:.2f} ms")

    # System metrics
    st.subheader("💻 System Resources")

    sys_col1, sys_col2 = st.columns(2)

    with sys_col1:
        st.metric("Memory Usage", f"{system_metrics.get('memory_usage_mb', 0):.2f} MB")

    with sys_col2:
        st.metric("CPU Usage", f"{system_metrics.get('cpu_usage', 0):.2f}%")

    # Recent errors
    if dashboard.error_history:
        st.subheader("⚠️ Recent Errors")

        for error in list(dashboard.error_history)[-5:]:
            st.error(f"{error['time'].strftime('%H:%M:%S')}: {error['error']}")

    # Auto-refresh
    st.text(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()


def run_console_dashboard():
    """Run console-based dashboard (no Streamlit required)"""
    dashboard = PerformanceDashboard(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        print("\n🔒 Cybersecurity Threat Intelligence - Performance Monitor")
        print("=" * 70)
        print("Press Ctrl+C to stop\n")

        iteration = 0

        while True:
            iteration += 1

            # Collect metrics
            query_metrics = dashboard.collect_query_metrics()
            system_metrics = dashboard.get_system_metrics()
            throughput = dashboard.calculate_throughput()
            error_rate = dashboard.calculate_error_rate()
            percentiles = dashboard.get_latency_percentiles()

            # Clear screen (works on Unix/Linux/Mac)
            print("\033[2J\033[H")

            print(f"\n{'=' * 70}")
            print(f"Performance Dashboard - Update #{iteration}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'=' * 70}")

            # Current metrics
            print(f"\n📊 Current Metrics:")
            print(f"  Query Latency: {query_metrics.get('latency_ms', 0):.2f} ms")
            print(f"  Throughput: {throughput:.2f} queries/sec")
            print(f"  Error Rate: {error_rate:.2f}%")
            print(f"  Graph Size: {query_metrics.get('node_count', 0):,} nodes, {query_metrics.get('rel_count', 0):,} relationships")

            # Latency percentiles
            if percentiles:
                print(f"\n📈 Latency Percentiles:")
                print(f"  P50: {percentiles['p50']:.2f} ms")
                print(f"  P75: {percentiles['p75']:.2f} ms")
                print(f"  P90: {percentiles['p90']:.2f} ms")
                print(f"  P95: {percentiles['p95']:.2f} ms")
                print(f"  P99: {percentiles['p99']:.2f} ms")

            # System resources
            print(f"\n💻 System Resources:")
            print(f"  Memory: {system_metrics.get('memory_usage_mb', 0):.2f} MB")
            print(f"  CPU: {system_metrics.get('cpu_usage', 0):.2f}%")

            # Recent errors
            if dashboard.error_history:
                print(f"\n⚠️  Recent Errors ({len(dashboard.error_history)}):")
                for error in list(dashboard.error_history)[-3:]:
                    print(f"  • {error['time'].strftime('%H:%M:%S')}: {error['error'][:50]}")

            print(f"\n{'=' * 70}")

            # Wait before next update
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user")
    finally:
        dashboard.close()


def main():
    """Main entry point"""
    import sys

    if "--streamlit" in sys.argv or STREAMLIT_AVAILABLE:
        run_streamlit_dashboard()
    else:
        run_console_dashboard()


if __name__ == "__main__":
    if STREAMLIT_AVAILABLE:
        # When run with streamlit
        run_streamlit_dashboard()
    else:
        # When run directly
        main()
