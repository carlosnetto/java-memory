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

### 3. Launch instances

```bash
./Launch.sh 40
```

Launches the specified number of instances. If the AppCDS archive exists, instances are launched with `-Xshare:on` automatically. Otherwise they launch without it (with a warning).

### Stopping all instances

```bash
./kill.sh
```

### Cleaning up

```bash
./cleanup.sh
```

Removes all generated artifacts (`.jar`, `.jsa`, `.cls`, `.java`, `.class`, logs), keeping only source code.

## Files

| File | Description |
|---|---|
| `CreateBigProgram.py` | Python script that generates the Java sources (BigProgram + 100 Worker classes) |
| `CreateBigProgram.sh` | Generates sources, compiles, packages `BigProgram.jar`, and cleans up |
| `appcds_setup.sh` | Dumps class list and creates the AppCDS shared archive (requires `BigProgram.jar`) |
| `Launch.sh` | Launches N background instances, using the AppCDS archive if available |
| `kill.sh` | Kills all running BigProgram instances |
| `cleanup.sh` | Removes all generated artifacts |
