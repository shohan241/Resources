from docx.shared import Inches

def build_ch01(engine):
    engine.add_chapter(
        1, 
        "The Paradigm Shift & Java Memory Architecture",
        "A rigorous exploration of programming paradigms, JVM runtime internals (Heap, Stack, Metaspace), why Java is strictly pass-by-value, and the famous Integer Cache trap."
    )

    engine.add_h2("1.1 The Evolution of Object-Oriented Programming in Java")
    engine.add_body(
        "Before Java emerged in 1995, procedural languages like C and early C++ dominated industry computing. However, procedural systems suffered from architectural entropy: data structures and global state were decoupled from functions, leading to fragile spaghetti logic where altering a struct field would cascade into hundreds of broken functions. Java was engineered from the ground up to enforce strict Object-Oriented principles, platform independence ('Write Once, Run Anywhere'), and automated memory management."
    )

    headers_paradigms = ["Dimension", "Procedural (C)", "Object-Oriented (Java)", "Functional (Haskell / Streams)"]
    rows_paradigms = [
        ["Core Unit", "Procedures / Functions", "Classes & Objects", "Pure Mathematical Functions"],
        ["State Management", "Decoupled global / local structs", "Encapsulated private fields within objects", "Immutable state & transformation pipelines"],
        ["Memory Management", "Manual (`malloc` / `free`) - error prone", "Automatic Garbage Collector (JVM)", "Garbage Collected / Immutable allocations"],
        ["Extensibility", "Conditional switch-cases & function pointers", "Polymorphism, Interfaces & Subtyping", "Higher-order functions & Currying"],
        ["Concurrency Model", "Manual OS threads & raw mutexes", "Java Memory Model (`volatile`, `synchronized`)", "Lock-free immutable parallelism"]
    ]
    engine.add_table(headers_paradigms, rows_paradigms, [Inches(1.2), Inches(1.8), Inches(2.2), Inches(1.8)])

    engine.add_h2("1.2 The Four Pillars of OOP in Java")
    engine.add_body(
        "Java enforces the four core OOP pillars as fundamental language semantics:"
    )
    engine.add_bullet("1. Encapsulation:", "Bundling data (fields) and methods operating on that data into a cohesive class, while restricting direct access using access modifiers (`private`, `protected`, `public`).")
    engine.add_bullet("2. Abstraction:", "Hiding internal implementation complexity and exposing a clean public contract using `interface` and `abstract class` declarations.")
    engine.add_bullet("3. Inheritance:", "Acquiring properties and behaviors from a superclass via the `extends` keyword to model 'Is-A' taxonomies and enable code reuse.")
    engine.add_bullet("4. Polymorphism:", "Enabling a single reference type or method signature to dynamically execute different runtime behaviors via dynamic method dispatch.")

    engine.add_h2("1.3 Inside the Java Virtual Machine (JVM) Architecture")
    engine.add_body(
        "To write production-grade Java, an engineer must understand the physical memory regions managed by the JVM during execution:"
    )
    engine.add_bullet("1. JVM Stack (Thread-Private):", "Each operating thread possesses its own stack. Whenever a method is invoked, a new Stack Frame is pushed. A stack frame contains: (1) Local Variable Array, (2) Operand Stack, and (3) Frame Data (runtime constant pool references). Deallocated automatically when the method returns (LIFO).")
    engine.add_bullet("2. JVM Heap (Thread-Shared):", "The shared memory zone where ALL Java objects and arrays reside. Divided into Young Generation (Eden space, Survivor S0/S1 spaces) and Old/Tenured Generation. Managed by the Garbage Collector.")
    engine.add_bullet("3. Metaspace / Method Area (Thread-Shared):", "Stores class-level metadata, runtime constant pool, field and method bytecodes, and static variables. In Java 8+, Metaspace replaced the old PermGen and is allocated out of native OS memory.")
    engine.add_bullet("4. Program Counter (PC) Register:", "Holds the address of the current JVM bytecode instruction being executed by each thread.")

    headers_mem = ["Memory Region", "Lifetime", "Thread Scope", "Contents", "Exception on Overflow"]
    rows_mem = [
        ["JVM Stack", "Method invocation scope", "Thread-Private", "Primitives, Object reference pointers, Stack frames", "`StackOverflowError`"],
        ["JVM Heap", "Application runtime (until GC)", "Thread-Shared", "All instantiated Objects, Arrays, Instance fields", "`OutOfMemoryError: Java heap space`"],
        ["Metaspace", "ClassLoader lifecycle", "Thread-Shared", "Class definitions, bytecode, Static variables, Constant Pool", "`OutOfMemoryError: Metaspace`"]
    ]
    engine.add_table(headers_mem, rows_mem, [Inches(1.2), Inches(1.5), Inches(1.1), Inches(2.0), Inches(1.2)])

    engine.add_h2("1.4 Why Java is Strictly 100% Pass-by-Value (The Ultimate Clarification)")
    engine.add_body(
        "One of the most persistent misconceptions in Java interviews is that 'primitives are passed by value, but objects are passed by reference.' This is FALSE. Java is strictly 100% PASS-BY-VALUE in all scenarios."
    )
    engine.add_body(
        "When an object variable is passed to a method, you are NOT passing the object itself, nor are you passing a C++ style reference alias. You are passing a COPY OF THE MEMORY ADDRESS (reference) stored on the caller's stack frame. Both the caller and the callee hold independent copies of the reference pointing to the same heap object."
    )

    code_pass_by_value = """public class ParameterPassingMechanics {
    static class User {
        String name;
        User(String name) { this.name = name; }
    }

    // 1. Primitive: Pass-by-value of raw bits
    public static void modifyPrimitive(int x) {
        x = 999; // Alters only the local stack frame copy!
    }

    // 2. Object Mutation: Operates on the shared heap instance
    public static void mutateObject(User u) {
        u.name = "Alice"; // Mutates the object on the heap!
    }

    // 3. Object Reassignment: Proves Java is Pass-by-Value!
    public static void reassignReference(User u) {
        // 'u' is a local copy of the reference on the stack.
        // Pointing 'u' to a new object does NOT alter the caller's reference!
        u = new User("Bob"); 
    }

    public static void main(String[] args) {
        int num = 10;
        modifyPrimitive(num);
        System.out.println("num: " + num); // Output: 10 (Unchanged!)

        User user = new User("Initial");
        mutateObject(user);
        System.out.println("After mutate: " + user.name); // Output: Alice (Field mutated!)

        reassignReference(user);
        System.out.println("After reassign: " + user.name); // Still Alice! NOT Bob!
    }
}"""
    engine.add_code("Proof of Java Strict Pass-by-Value Semantics", "java", code_pass_by_value)

    engine.add_h2("1.5 Autoboxing, Wrapper Classes & The Integer Cache Trap")
    engine.add_body(
        "Java provides Object Wrapper Classes (`Integer`, `Long`, `Double`, `Boolean`) for every primitive type. Autoboxing is the automatic conversion made by the Java compiler between primitive types and their corresponding wrapper objects (e.g., `int` to `Integer`)."
    )
    engine.add_body(
        "However, wrapper objects are heap instances compared via memory address when using `==`. To conserve memory, the Java Language Specification mandates caching for `Integer` objects between -128 and 127 via `Integer.valueOf()`."
    )

    code_cache_trap = """public class IntegerCacheTrap {
    public static void main(String[] args) {
        // Within Cache Range (-128 to 127): Reuses cached instances!
        Integer a = 127;
        Integer b = 127;
        System.out.println(a == b);      // TRUE! (Both point to identical cached heap object)
        System.out.println(a.equals(b)); // TRUE! (Values match)

        // Outside Cache Range: Instantiates new distinct heap objects!
        Integer x = 128;
        Integer y = 128;
        System.out.println(x == y);      // FALSE! (Different heap memory addresses!)
        System.out.println(x.equals(y)); // TRUE! (Logical values match)
    }
}"""
    engine.add_code("The Java Integer Cache Trap (-128 to 127)", "java", code_cache_trap)

    engine.add_callout(
        "Senior Software Engineer Rule of Equality",
        [
            "1. ALWAYS compare Java Objects using `.equals()` rather than `==`.",
            "2. Using `==` on Wrapper Classes causes catastrophic, intermittent bugs when values cross the 127 cache boundary.",
            "3. Use `==` strictly for primitive type comparison (`int`, `boolean`, `double`) or checking `null`."
        ],
        box_type="alert"
    )
