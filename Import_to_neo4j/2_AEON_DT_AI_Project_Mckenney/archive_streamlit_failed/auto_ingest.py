#!/usr/bin/env python3
"""
AEON Automated Document Ingestion System
Main entry point with CLI interface
"""

import argparse
import logging
import sys
import signal
import time
from pathlib import Path
from typing import Optional
import yaml

from agents import OrchestratorAgent

# Global orchestrator instance for signal handling
orchestrator: Optional[OrchestratorAgent] = None


def setup_logging(config: dict) -> logging.Logger:
    """
    Setup logging configuration

    Args:
        config: Configuration dictionary

    Returns:
        Logger instance
    """
    logging_config = config.get('logging', {})

    level = logging_config.get('level', 'INFO')
    format_str = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level),
        format=format_str
    )

    # File logging if enabled
    if logging_config.get('file_logging', True):
        log_dir = Path(logging_config.get('log_directory', 'logs'))
        log_dir.mkdir(parents=True, exist_ok=True)

        from datetime import datetime
        log_filename = logging_config.get('log_filename', 'auto_ingest_{date}.log')
        log_filename = log_filename.format(date=datetime.now().strftime('%Y%m%d'))

        log_file = log_dir / log_filename

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_str))
        logging.getLogger().addHandler(file_handler)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at {level} level")

    return logger


def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global orchestrator

    print("\n\n🛑 Shutdown signal received...")

    if orchestrator:
        print("Stopping orchestrator...")
        orchestrator.stop()

    print("Shutdown complete.")
    sys.exit(0)


def run_watch_mode(orchestrator: OrchestratorAgent, args: argparse.Namespace) -> int:
    """
    Run in continuous monitoring mode

    Args:
        orchestrator: Orchestrator agent instance
        args: Command-line arguments

    Returns:
        Exit code
    """
    print("""
╔══════════════════════════════════════════════════════════╗
║   AEON Automated Document Ingestion System              ║
║   Continuous Monitoring Mode                            ║
╚══════════════════════════════════════════════════════════╝
    """)

    print(f"📂 Watching directories...")
    for watch_dir in orchestrator.config.get('monitoring', {}).get('watch_directories', []):
        print(f"   - {watch_dir}")

    print(f"\n⚙️  Configuration:")
    print(f"   - Batch size: {orchestrator.batch_size}")
    print(f"   - Parallel workers: {orchestrator.parallel_workers}")
    print(f"   - Supported formats: {', '.join(orchestrator.config.get('monitoring', {}).get('supported_extensions', []))}")

    if args.duration:
        print(f"   - Duration: {args.duration} seconds")

    print("\n🚀 Starting monitoring...")
    print("   Press Ctrl+C to stop\n")

    try:
        # Start orchestrator
        orchestrator.run({
            'mode': 'watch',
            'duration': args.duration
        })

        # Show final report
        if not args.quiet:
            print("\n" + orchestrator.get_progress_report())

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        orchestrator.stop()
        return 1

    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logging.exception("Fatal error in watch mode")
        return 1


def run_batch_mode(orchestrator: OrchestratorAgent, args: argparse.Namespace) -> int:
    """
    Run in one-time batch processing mode

    Args:
        orchestrator: Orchestrator agent instance
        args: Command-line arguments

    Returns:
        Exit code
    """
    print("""
╔══════════════════════════════════════════════════════════╗
║   AEON Automated Document Ingestion System              ║
║   Batch Processing Mode                                 ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Get files to process
    files = []

    if args.files:
        files = args.files
    elif args.directory:
        dir_path = Path(args.directory)
        if not dir_path.exists():
            print(f"❌ Directory not found: {args.directory}")
            return 1

        # Get all supported files from directory
        supported_exts = orchestrator.config.get('monitoring', {}).get('supported_extensions', [])
        for ext in supported_exts:
            if args.recursive:
                files.extend([str(f) for f in dir_path.rglob(f'*{ext}')])
            else:
                files.extend([str(f) for f in dir_path.glob(f'*{ext}')])

    if not files:
        print("❌ No files to process")
        return 1

    print(f"📂 Processing {len(files)} files...")

    if args.verbose:
        print("\nFiles to process:")
        for i, file_path in enumerate(files[:10], 1):
            print(f"   {i}. {file_path}")
        if len(files) > 10:
            print(f"   ... and {len(files) - 10} more")

    print(f"\n⚙️  Configuration:")
    print(f"   - Parallel workers: {orchestrator.parallel_workers}")

    print("\n🚀 Starting batch processing...\n")

    try:
        # Start orchestrator
        result = orchestrator.run({
            'mode': 'batch',
            'files': files
        })

        # Show final report
        if not args.quiet:
            print("\n" + orchestrator.get_progress_report())

        state = result.get('state', {})
        print(f"\n✅ Batch processing complete!")
        print(f"   - Converted: {state.get('files_converted', 0)}/{len(files)}")
        print(f"   - Errors: {len(state.get('errors', []))}")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        orchestrator.stop()
        return 1

    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logging.exception("Fatal error in batch mode")
        return 1


def run_progress_monitor(orchestrator: OrchestratorAgent, interval: int = 10):
    """
    Display progress updates while processing

    Args:
        orchestrator: Orchestrator agent instance
        interval: Update interval in seconds
    """
    try:
        while orchestrator.running:
            time.sleep(interval)
            if not orchestrator.running:
                break

            # Clear screen and show progress
            print("\033[2J\033[H")  # Clear screen
            print(orchestrator.get_progress_report())

    except KeyboardInterrupt:
        pass


def main():
    """Main entry point"""
    global orchestrator

    parser = argparse.ArgumentParser(
        description='AEON Automated Document Ingestion System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Mode selection
    parser.add_argument(
        'mode',
        choices=['watch', 'batch'],
        help='Operation mode: watch (continuous monitoring) or batch (one-time processing)'
    )

    # Configuration
    parser.add_argument(
        '--config',
        default='config/main_config.yaml',
        help='Path to configuration file (default: config/main_config.yaml)'
    )

    # Watch mode options
    parser.add_argument(
        '--duration',
        type=int,
        help='Duration in seconds for watch mode (default: run indefinitely)'
    )

    # Batch mode options
    parser.add_argument(
        '--files',
        nargs='+',
        help='Specific files to process in batch mode'
    )

    parser.add_argument(
        '--directory',
        help='Directory to process in batch mode'
    )

    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process directory recursively in batch mode'
    )

    # Output options
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress reports'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress information'
    )

    parser.add_argument(
        '--progress-interval',
        type=int,
        default=10,
        help='Progress update interval in seconds (default: 10)'
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {args.config}")
        return 1
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1

    # Setup logging
    logger = setup_logging(config)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize orchestrator
    try:
        orchestrator = OrchestratorAgent("Orchestrator", config)
    except Exception as e:
        print(f"❌ Error initializing orchestrator: {e}")
        logging.exception("Orchestrator initialization failed")
        return 1

    # Run in selected mode
    try:
        if args.mode == 'watch':
            return run_watch_mode(orchestrator, args)
        elif args.mode == 'batch':
            return run_batch_mode(orchestrator, args)
        else:
            print(f"❌ Unknown mode: {args.mode}")
            return 1

    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        logging.exception("Fatal error in main")
        return 1


if __name__ == '__main__':
    sys.exit(main())
