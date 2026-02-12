# Java Memory

A synthetic Java workload for testing JVM AppCDS (Application Class Data Sharing).

## What it does

`CreateBigProgram.py` generates 100 Worker classes with 200 methods each (20,000 methods total), all filled with unique arithmetic operations that produce substantial bytecode. A main class (`BigProgram`) calls all methods in a loop.

The memory footprint comes entirely from loaded class metadata and bytecode (~155MB+ metaspace) — exactly what AppCDS can share across JVM instances. No large heap allocations are used.

After the initial execution, the program loops forever, re-executing all methods and sleeping for a random 30–60 seconds. This keeps code pages warm (preventing Linux from swapping them) and staggers CPU usage across instances.

## Usage

### 1. Build BigProgram.jar

```bash
./CreateBigProgram.sh
```

Generates the Java sources, compiles them, packages everything into `BigProgram.jar`, and cleans up all intermediate `.java` and `.class` files.

### 2. Build the AppCDS shared archive

```bash
./appcds_setup.sh
```

Requires `BigProgram.jar` to exist. Launches the program once to collect the loaded class list and creates a shared archive (`BigProgram.jsa`).

### 3. (Alternative) Build the Leyden AOT cache

```bash
./leyden_setup.sh
```

Requires `BigProgram.jar` to exist and a JDK with Project Leyden support (JDK 24+). Runs the program once to record an execution profile, then creates an AOT cache (`BigProgram.aot`). This goes further than AppCDS by also caching AOT-compiled code.

### 4. Launch instances

```bash
./Launch.sh 50
```

Launches the specified number of instances (50 recommended). If the Leyden AOT cache exists, instances use it automatically; otherwise if the AppCDS archive exists, instances use that instead. If neither is found, instances launch without optimizations (with a warning).

### Stopping all instances

```bash
./kill.sh
```

### Cleaning up

```bash
./cleanup.sh
```

Removes all generated artifacts (`.jar`, `.jsa`, `.cls`, `.aot`, `.aotconf`, `.java`, `.class`, logs), keeping only source code.

## Experiment: see Leyden in action

Project Leyden (JDK 24+) caches AOT-compiled code on top of class metadata, potentially saving even more memory and startup time than AppCDS alone.

```bash
./CreateBigProgram.sh
./leyden_setup.sh
./Launch.sh 50
# Watch memory usage in Activity Monitor, then stop:
./kill.sh
```

## Experiment: see AppCDS in action

To feel the difference AppCDS makes, try launching 50 instances before and after setting up the shared archive. Tested on macOS with Java 25.

**Without AppCDS:**

```bash
./CreateBigProgram.sh
./Launch.sh 50
# Watch memory usage in Activity Monitor, then stop:
./kill.sh
```

**With AppCDS:**

```bash
./appcds_setup.sh
./Launch.sh 50
# Compare memory usage in Activity Monitor — it should be noticeably lower
./kill.sh
```

## Files

| File | Description |
|---|---|
| `CreateBigProgram.py` | Python script that generates the Java sources (BigProgram + 100 Worker classes) |
| `CreateBigProgram.sh` | Generates sources, compiles, packages `BigProgram.jar`, and cleans up |
| `appcds_setup.sh` | Dumps class list and creates the AppCDS shared archive (requires `BigProgram.jar`) |
| `leyden_setup.sh` | Records execution profile and creates the Leyden AOT cache (requires `BigProgram.jar`, JDK 24+) |
| `Launch.sh` | Launches N background instances, using Leyden AOT cache or AppCDS archive if available |
| `kill.sh` | Kills all running BigProgram instances |
| `cleanup.sh` | Removes all generated artifacts |
