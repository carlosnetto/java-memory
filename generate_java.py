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
            f.write(f"        byte[] data = new byte[200 * 1024]; // 200KB\n")
            f.write(f"        new Random(seed).nextBytes(data);\n")
            f.write(f"        memoryKeep.add(data);\n")
            f.write(f"        long localSum = 0;\n")
            for j in range(lines_per_method):
                f.write(f"        localSum += (seed * {j}) ^ data[{j % 1000}];\n")
            f.write(f"        checksum += localSum;\n")
            f.write(f"    }}\n\n")
            
        # Main method
        f.write("    public static void main(String[] args) throws Exception {\n")
        f.write("        System.out.println(\"Allocating memory and loading classes...\");\n")
        for i in range(num_methods):
            f.write(f"        method{i}({i});\n")
            
        f.write("\n        // Ensure the code is 'big' by adding more dummy lines\n")
        for i in range(1000):
            f.write(f"        checksum += {i};\n")
            
        f.write("\n        System.out.println(\"Ready. Memory should be occupied. Checksum: \" + checksum);\n")
        f.write("        System.out.println(\"Press Enter to stop the program...\");\n")
        f.write("        System.in.read();\n")
        f.write("        System.out.println(\"Final Checksum to prevent optimization: \" + checksum + \" List size: \" + memoryKeep.size());\n")
        f.write("    }\n")
        f.write("}\n")

if __name__ == "__main__":
    generate_java()
