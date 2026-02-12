"""
Generates a large Java program (BigProgram.java) for testing JVM AppCDS
(Application Class Data Sharing) behavior under memory pressure.

The generated program allocates ~200MB of heap memory across 500 methods,
each holding a 400KB byte array pinned in a static list to prevent GC.
After the initial allocation, it enters an infinite loop that continuously
touches all allocated memory and sleeps for a random interval between 5 and
15 seconds. This serves two purposes:

1. Keep memory warm: periodic reads/writes prevent Linux from paging the
   memory out to swap, which is important when running many instances.
2. Stagger execution: the randomized sleep ensures that when 40 instances
   are launched concurrently, they don't all spike CPU at the same time.
"""


def generate_java():
    class_name = "BigProgram"
    num_methods = 500
    lines_per_method = 18

    with open(f"{class_name}.java", "w") as f:
        f.write("import java.util.*;\n\n")
        f.write(f"public class {class_name} {{\n")
        f.write("    private static final List<Object> memoryKeep = new ArrayList<>();\n")
        f.write("    private static long checksum = 0;\n\n")

        # Generate many methods
        for i in range(num_methods):
            f.write(f"    private static void method{i}(int seed) {{\n")
            f.write(f"        byte[] data = new byte[400 * 1024]; // 400KB\n")
            f.write(f"        new Random(seed).nextBytes(data);\n")
            f.write(f"        memoryKeep.add(data);\n")
            f.write(f"        long localSum = 0;\n")
            for j in range(lines_per_method):
                f.write(f"        localSum += (seed * {j}) ^ data[{j % 1000}];\n")
            f.write(f"        checksum += localSum;\n")
            f.write(f"    }}\n\n")

        # Helper method that touches all allocated memory to keep it warm
        f.write("    private static void touchMemory() {\n")
        f.write("        long sum = 0;\n")
        f.write("        for (Object obj : memoryKeep) {\n")
        f.write("            byte[] data = (byte[]) obj;\n")
        f.write("            for (int i = 0; i < data.length; i += 4096) {\n")
        f.write("                sum += data[i];\n")
        f.write("            }\n")
        f.write("        }\n")
        f.write("        checksum += sum;\n")
        f.write("    }\n\n")

        # Main method
        f.write("    public static void main(String[] args) throws Exception {\n")
        f.write("        System.out.println(\"Allocating memory and loading classes...\");\n")
        for i in range(num_methods):
            f.write(f"        method{i}({i});\n")

        f.write("\n        // Ensure the code is 'big' by adding more dummy lines\n")
        for i in range(1000):
            f.write(f"        checksum += {i};\n")

        f.write("\n        System.out.println(\"Ready. Memory occupied. Checksum: \" + checksum);\n")
        f.write("        System.out.println(\"Entering keep-warm loop...\");\n")
        f.write("        Random rng = new Random();\n")
        f.write("        int iteration = 0;\n")
        f.write("        while (true) {\n")
        f.write("            touchMemory();\n")
        f.write("            int sleepMs = 5000 + rng.nextInt(10001); // 5–15 seconds\n")
        f.write("            iteration++;\n")
        f.write("            if (iteration % 10 == 0) {\n")
        f.write("                System.out.println(\"Iteration \" + iteration + \" checksum=\" + checksum + \" sleeping \" + sleepMs + \"ms\");\n")
        f.write("            }\n")
        f.write("            Thread.sleep(sleepMs);\n")
        f.write("        }\n")
        f.write("    }\n")
        f.write("}\n")

if __name__ == "__main__":
    generate_java()
