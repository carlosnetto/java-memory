# CLAUDE.md

## Project overview

Synthetic Java workload for testing JVM AppCDS (Application Class Data Sharing). The goal is to measure memory savings when sharing class metadata across multiple JVM instances.

## How it works

`CreateBigProgram.py` generates Java source code:
- 100 Worker classes (`Worker0`..`Worker99`), each with 200 methods of 200 lines of arithmetic — 20,000 methods total
- A main class (`BigProgram`) that calls all methods, then loops forever re-executing every 30–60 seconds to keep code pages warm
- Memory footprint is entirely class metadata/bytecode (~155MB+ metaspace), not heap — this is what AppCDS shares

Key parameters in `CreateBigProgram.py:generate_java()`:
- `num_classes = 100`
- `methods_per_class = 200`
- `lines_per_method = 200`
- Sleep interval: 30–60 seconds between iterations

## Workflow

1. `./CreateBigProgram.sh` — generate sources, compile in batches of 20, package into `BigProgram.jar`
2. `./appcds_setup.sh` — run once to dump class list (`.cls`) and create shared archive (`.jsa`)
3. `./Launch.sh <N>` — launch N instances (auto-uses AppCDS archive if present)
4. `./kill.sh` — kill all running instances
5. `./cleanup.sh` — remove all generated artifacts (`.jar`, `.jsa`, `.cls`, `.java`, `.class`, logs)

## Generated artifacts (not committed)

- `BigProgram.jar` — the compiled workload
- `BigProgram.cls` — AppCDS class list
- `BigProgram.jsa` — AppCDS shared archive
- `instance_*.log` — per-instance logs
- `Worker*.java`, `BigProgram.java` — intermediate generated sources (deleted by build script)

## Common tasks

- **Change workload size**: edit `num_classes`, `methods_per_class`, or `lines_per_method` in `CreateBigProgram.py`, then rebuild
- **Change sleep interval**: edit the `sleepMs` line in `CreateBigProgram.py` (~line 96)
- **After any Python changes**: must re-run `./CreateBigProgram.sh` then `./appcds_setup.sh` to rebuild jar and archive
