"""
Progress Tracker Utility
Provides rich progress reporting for document processing
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Rich progress reporting for document ingestion"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize progress tracker

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.console = Console()

        progress_config = config.get('progress', {})
        self.show_progress_bar = progress_config.get('show_progress_bar', True)
        self.update_frequency = progress_config.get('update_frequency_seconds', 5)
        self.detailed_stats = progress_config.get('detailed_stats', True)

        # State tracking
        self.stats = {
            'start_time': None,
            'files_discovered': 0,
            'files_converted': 0,
            'files_classified': 0,
            'files_ner_processed': 0,
            'files_ingested': 0,
            'errors': 0
        }

    def start(self):
        """Start progress tracking"""
        self.stats['start_time'] = datetime.now()
        logger.info("Progress tracking started")

    def update(self, **kwargs):
        """
        Update progress statistics

        Args:
            **kwargs: Statistics to update
        """
        for key, value in kwargs.items():
            if key in self.stats:
                self.stats[key] = value

    def increment(self, stat_name: str, count: int = 1):
        """
        Increment a statistic

        Args:
            stat_name: Name of statistic
            count: Amount to increment
        """
        if stat_name in self.stats:
            self.stats[stat_name] += count

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        stats = self.stats.copy()

        # Calculate derived statistics
        if stats['start_time']:
            elapsed = datetime.now() - stats['start_time']
            stats['elapsed_seconds'] = elapsed.total_seconds()
            stats['elapsed_formatted'] = str(timedelta(seconds=int(elapsed.total_seconds())))

            # Calculate processing rate
            if stats['elapsed_seconds'] > 0:
                stats['files_per_second'] = stats['files_converted'] / stats['elapsed_seconds']
                stats['files_per_minute'] = stats['files_per_second'] * 60

        return stats

    def generate_table(self) -> Table:
        """
        Generate progress table

        Returns:
            Rich Table object
        """
        stats = self.get_stats()

        table = Table(title="Document Processing Progress", show_header=True)

        table.add_column("Stage", style="cyan", no_wrap=True)
        table.add_column("Count", style="magenta", justify="right")
        table.add_column("Status", style="green")

        # Add rows
        table.add_row(
            "📂 Files Discovered",
            str(stats['files_discovered']),
            "✓" if stats['files_discovered'] > 0 else "⏳"
        )

        table.add_row(
            "🔄 Files Converted",
            str(stats['files_converted']),
            "✓" if stats['files_converted'] > 0 else "⏳"
        )

        table.add_row(
            "🏷️  Files Classified",
            str(stats['files_classified']),
            "✓" if stats['files_classified'] > 0 else "⏳"
        )

        table.add_row(
            "🔍 Files NER Processed",
            str(stats['files_ner_processed']),
            "✓" if stats['files_ner_processed'] > 0 else "⏳"
        )

        table.add_row(
            "💾 Files Ingested",
            str(stats['files_ingested']),
            "✓" if stats['files_ingested'] > 0 else "⏳"
        )

        table.add_row(
            "❌ Errors",
            str(stats['errors']),
            "⚠️" if stats['errors'] > 0 else "✓"
        )

        return table

    def generate_summary(self) -> Panel:
        """
        Generate summary panel

        Returns:
            Rich Panel object
        """
        stats = self.get_stats()

        summary_text = Text()

        summary_text.append("⏱️  ", style="bold cyan")
        summary_text.append(f"Elapsed: {stats.get('elapsed_formatted', 'N/A')}\n", style="white")

        if stats.get('files_per_minute'):
            summary_text.append("⚡ ", style="bold yellow")
            summary_text.append(f"Processing Rate: {stats['files_per_minute']:.1f} files/min\n", style="white")

        summary_text.append("📊 ", style="bold green")
        total_processed = stats['files_converted']
        total_discovered = stats['files_discovered']

        if total_discovered > 0:
            completion_pct = (total_processed / total_discovered) * 100
            summary_text.append(f"Completion: {completion_pct:.1f}%\n", style="white")
        else:
            summary_text.append("Completion: 0%\n", style="white")

        return Panel(summary_text, title="Summary", border_style="blue")

    def print_progress(self):
        """Print current progress to console"""
        self.console.clear()
        self.console.print(self.generate_table())

        if self.detailed_stats:
            self.console.print(self.generate_summary())

    def print_final_report(self):
        """Print final completion report"""
        stats = self.get_stats()

        self.console.print("\n")
        self.console.rule("[bold green]Processing Complete", style="green")

        # Final statistics table
        final_table = Table(show_header=False, box=None)
        final_table.add_column("Metric", style="cyan", no_wrap=True)
        final_table.add_column("Value", style="white", justify="right")

        final_table.add_row("Total Files Discovered", str(stats['files_discovered']))
        final_table.add_row("Successfully Converted", str(stats['files_converted']))
        final_table.add_row("Successfully Classified", str(stats['files_classified']))
        final_table.add_row("NER Processed", str(stats['files_ner_processed']))
        final_table.add_row("Ingested to Neo4j", str(stats['files_ingested']))
        final_table.add_row("Errors", str(stats['errors']))

        if stats.get('elapsed_formatted'):
            final_table.add_row("Total Time", stats['elapsed_formatted'])

        if stats.get('files_per_minute'):
            final_table.add_row("Average Rate", f"{stats['files_per_minute']:.1f} files/min")

        self.console.print(Panel(final_table, title="Final Report", border_style="green"))

        # Success/failure summary
        if stats['errors'] == 0:
            self.console.print("\n✅ [bold green]All files processed successfully!")
        else:
            self.console.print(f"\n⚠️  [bold yellow]Completed with {stats['errors']} errors")

        self.console.print("\n")
