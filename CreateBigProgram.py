"""
Generates a large Java program for testing JVM AppCDS (Application Class
Data Sharing).

AppCDS shares loaded class metadata and bytecode across JVM instances via a
shared archive (.jsa). To benefit from this, the program needs a large CODE
footprint — lots of classes and methods with substantial bytecode — rather
than large heap allocations.

The generator produces multiple Worker classes (Worker0..WorkerN), each
containing many methods filled with unique arithmetic operations that produce
real bytecode. A main class (BigProgram) calls all methods in a loop. All
memory consumption comes from the loaded class data itself, which is exactly
what AppCDS can share across 40 concurrent instances.

After the initial execution, the program loops forever, re-executing all
methods and sleeping for a random 30-60 seconds. This keeps code pages warm
(preventing Linux from swapping them out) and staggers CPU usage across
instances.
"""


def generate_java():
    num_classes = 100
    methods_per_class = 200
    lines_per_method = 200

    ops = ['+', '-', '^', '|', '&']

    # Generate worker classes, each with its own constant pool
    for cls_idx in range(num_classes):
        class_name = f"Worker{cls_idx}"
        with open(f"{class_name}.java", "w") as f:
            f.write(f"public class {class_name} {{\n")
            for m in range(methods_per_class):
                gid = cls_idx * methods_per_class + m
                f.write(f"    public static long method{m}(long seed) {{\n")
                f.write(f"        long a = seed ^ {(gid * 31 + 17) % 32000};\n")
                f.write(f"        long b = seed + {(gid * 7 + 3) % 32000};\n")
                f.write(f"        long c = seed - {(gid * 13 + 5) % 32000};\n")
                for j in range(lines_per_method):
                    op = ops[j % len(ops)]
                    c1 = (j * 13 + gid) % 32000
                    c2 = (j * 7 + 11) % 32000 + 1  # never 0, safe for multiply
                    c3 = (gid * j + 37) % 32000
                    c4 = (j + gid * 3) % 32000
                    f.write(f"        a = (a {op} {c1}) * {c2} + c;\n")
                    f.write(f"        b = (b ^ a) + {c3};\n")
                    f.write(f"        c = (c {op} b) ^ {c4};\n")
                f.write(f"        return a + b + c;\n")
                f.write(f"    }}\n\n")
            f.write("}\n")
        print(f"Generated {class_name}.java ({methods_per_class} methods)")

    # Generate main class
    with open("BigProgram.java", "w") as f:
        f.write("import java.lang.management.ManagementFactory;\n")
        f.write("import java.lang.management.MemoryPoolMXBean;\n")
        f.write("import java.util.Random;\n\n")
        f.write("public class BigProgram {\n")
        f.write("    private static long checksum = 0;\n\n")

        # One helper per worker to stay under 64KB method bytecode limit
        for cls_idx in range(num_classes):
            f.write(f"    private static void runWorker{cls_idx}() {{\n")
            for m in range(methods_per_class):
                f.write(f"        checksum += Worker{cls_idx}.method{m}(checksum);\n")
            f.write("    }\n\n")

        f.write("    private static void runAll() {\n")
        for cls_idx in range(num_classes):
            f.write(f"        runWorker{cls_idx}();\n")
        f.write("    }\n\n")

        f.write("    private static String memoryReport() {\n")
        f.write("        Runtime rt = Runtime.getRuntime();\n")
        f.write("        long heapUsed = (rt.totalMemory() - rt.freeMemory()) / (1024 * 1024);\n")
        f.write("        long heapMax = rt.maxMemory() / (1024 * 1024);\n")
        f.write("        long metaspace = 0;\n")
        f.write("        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {\n")
        f.write("            if (pool.getName().contains(\"Metaspace\")) {\n")
        f.write("                metaspace = pool.getUsage().getUsed() / (1024 * 1024);\n")
        f.write("            }\n")
        f.write("        }\n")
        f.write("        return \"heap=\" + heapUsed + \"/\" + heapMax + \"MB metaspace=\" + metaspace + \"MB\";\n")
        f.write("    }\n\n")

        f.write("    public static void main(String[] args) throws Exception {\n")
        f.write("        System.out.println(\"Running initial pass to load all code...\");\n")
        f.write("        runAll();\n")
        f.write("        System.out.println(\"Ready. Entering keep-warm loop. \" + memoryReport());\n")
        f.write("        Random rng = new Random();\n")
        f.write("        int iteration = 0;\n")
        f.write("        while (true) {\n")
        f.write("            runAll();\n")
        f.write("            int sleepMs = 30000 + rng.nextInt(30001); // 30-60 seconds\n")
        f.write("            iteration++;\n")
        f.write("            if (iteration % 10 == 0) {\n")
        f.write("                System.out.println(\"Iteration \" + iteration + \" \" + memoryReport());\n")
        f.write("            }\n")
        f.write("            Thread.sleep(sleepMs);\n")
        f.write("        }\n")
        f.write("    }\n")
        f.write("}\n")
    print(f"Generated BigProgram.java (main class, calls {num_classes * methods_per_class} methods)")


if __name__ == "__main__":
    generate_java()
