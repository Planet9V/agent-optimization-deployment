# Cybersecurity Deep Research Agent (v2.0)
This folder contains a fully automated "Deep Research" agent designed to aggregate massive amounts of cybersecurity intelligence.

## Capabilities
- **Deep Research**: Generates 8000+ lines of content per report.
- **Recursive Search**: Explores sub-topics (IOCs, technical analysis, mitigation) for comprehensive coverage.
- **Mass Scrape**: Targets 50-100 unique sources per mission using multi-threading.
- **Full Transcripts**: Preserves full source text for forensic analysis.

## Prerequisites
- Python 3.8+
- Internet connection

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Agent**:
    Run the script in a terminal. It is designed to run continuously.
    ```bash
    python3 cyber_research_agent.py
    ```

2.  **Operation**:
    - The script will immediately perform one "Deep Research" mission.
    - It will then sleep and wake up every **30 minutes**.
    - Each mission generates a massive Markdown dossier in the `wiki/` directory.
    - Logs are stored in `logs/agent_activity.log`.

3.  **Output**:
    - Check the `wiki/` folder for generated reports (e.g., `CyberSec_Report_2024-11-26_14-30-00.md`).
    - Each report contains aggregated content, an executive summary, and APA citations.

## Customization
- **Topics**: Edit the `self.topics` list in `cyber_research_agent.py` to change the search focus.
- **Schedule**: Edit `schedule.every(30).minutes.do(job)` to change the frequency.

## Troubleshooting
- **Search Errors**: If DuckDuckGo rate limits you, the script logs the error and continues. You may need to increase the interval.
- **Empty Reports**: If reports are empty, check your internet connection or the log file for scraping errors.
