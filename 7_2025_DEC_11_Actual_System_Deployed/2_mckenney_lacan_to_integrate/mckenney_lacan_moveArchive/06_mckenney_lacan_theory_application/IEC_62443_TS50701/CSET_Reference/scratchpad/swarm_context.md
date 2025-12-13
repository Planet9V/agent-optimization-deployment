# CSET Swarm Context
**Mission:** Extract frameworks, questions, and assets from CSET repo.

## Active Agents
1. **Agent-1 (Orchestrator):** Managing workflow state.
2. **Agent-2 (Extractor):** Responsible for SQL parsing and data extraction.
3. **Agent-3 (Asset-Collector):** Responsible for SVG icon extraction.

## Global State
- **Status:** Initializing structure.
- **Repository Path:** `raw_data/cset` (Pending Clone)
- **Target Schema:** Postgres (See `CSET_Integration_Strategy.md`)

## Scratchpad Links
- [Extraction Log](./extraction_log.md)
- [Framework Manifest](./framework_list.md)
