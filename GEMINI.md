# RingWars Project Instructions

## Workflow & Routine
- **Feedback Loop**: Use `todo.txt` for instructions and `response.txt` for reporting.
- **GitHub Synchronization**:
    - **MANDATORY**: Always ask for permission before pushing changes to GitHub.
    - **Repository**: `Chidis58/ringwars`
    - **Post-Push Reporting**: After a push, `response.txt` MUST include a list of updated files using raw GitHub URLs for easy remote consumption by other agents.
    - **Format**: `https://raw.githubusercontent.com/Chidis58/ringwars/main/<file_path>`

## Architecture
- **Agents**: `sim/agents/` (Connector and Node logic)
- **Core**: `sim/core/` (Engine, Mechanics, Logger)
- **Scenarios**: `sim/scenarios/` (World initialization)
- **Output**: `sim/output/` (Logs and snapshots)

## Coding Standards
- Minimal dependencies (prefer standard library, then `numpy`/`networkx`).
- CLI-only output for Termux compatibility.
- Modular imports using `python3 -m sim.run`.
