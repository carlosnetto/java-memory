# Java Memory

A synthetic Java workload for testing JVM AppCDS (Application Class Data Sharing).

## What it does

`CreateBigProgram.py` generates 20 Worker classes with 100 methods each (2000 methods total), all filled with unique arithmetic operations that produce substantial bytecode. A main class (`BigProgram`) calls all methods in a loop.

The memory footprint comes entirely from loaded class metadata and bytecode — exactly what AppCDS can share across JVM instances. No large heap allocations are used.

After the initial execution, the program loops forever, re-executing all methods and sleeping for a random 5–15 seconds. This keeps code pages warm (preventing Linux from swapping them) and staggers CPU usage across instances.

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

Runs `CreateBigProgram.sh`, then launches the program once to collect the loaded class list and creates a shared archive (`BigProgram.jsa`).

### 3. Launch 40 instances

```bash
./launch_40.sh
```

If the AppCDS archive exists, instances are launched with `-Xshare:on` automatically. Otherwise they launch without it (with a warning).

### Stopping all instances

```bash
pkill -f BigProgram
```

## Files

| File | Description |
|---|---|
| `CreateBigProgram.py` | Python script that generates the Java sources (BigProgram + 20 Worker classes) |
| `CreateBigProgram.sh` | Generates sources, compiles, packages `BigProgram.jar`, and cleans up |
| `appcds_setup.sh` | Builds the JAR, dumps class list, and creates the AppCDS shared archive |
| `launch_40.sh` | Launches 40 background instances, using the AppCDS archive if available |
