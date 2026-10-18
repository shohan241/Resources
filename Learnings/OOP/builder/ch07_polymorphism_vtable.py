from docx.shared import Inches

def build_ch07(engine):
    engine.add_chapter(
        7, 
        "Polymorphism & JVM Dynamic Dispatch Internals",
        "Mastering compile-time vs. runtime polymorphism, method overloading precedence, HotSpot JVM bytecode instructions (invokevirtual, invokespecial), vtable/itable internals, and Java 16+ pattern matching."
    )

    engine.add_h2("7.1 Compile-Time vs. Run-Time Polymorphism")
    engine.add_body(
        "Polymorphism allows objects of different types to be treated uniformly through a shared interface, while executing behavior tailored to their actual runtime class."
    )

    headers_poly = ["Dimension", "Compile-Time Polymorphism (Static)", "Run-Time Polymorphism (Dynamic)"]
    rows_poly = [
        ["Resolution Time", "Compile time by `javac` compiler", "Runtime by JVM HotSpot Execution Engine"],
        ["Mechanism", "Method Overloading", "Method Overriding (Dynamic Method Dispatch)"],
        ["Bytecode Instruction", "Statically bound via exact parameter types in constant pool", "`invokevirtual` or `invokeinterface` via `vtable`/`itable`"],
        ["Execution Overhead", "Zero runtime overhead; direct branch", "Minimal overhead: Table lookup in class metadata"]
    ]
    engine.add_table(headers_poly, rows_poly, [Inches(1.8), Inches(2.6), Inches(2.6)])

    engine.add_h2("7.2 Method Overloading & The Compiler Precedence Rules")
    engine.add_body(
        "Method Overloading allows multiple methods to share the same name within the same class, differing only in parameter count, types, or order. Overloading CANNOT be resolved by return type alone."
    )
    engine.add_body(
        "When an overloaded method is called with ambiguous arguments, the Java compiler selects the method following a strict 4-phase precedence hierarchy:"
    )
    engine.add_bullet("Phase 1: Exact Match / Widening Primitive Conversion:", "(e.g., `int` widens to `long`, then to `double`).")
    engine.add_bullet("Phase 2: Autoboxing Conversion:", "(e.g., `int` autoboxes to `Integer`).")
    engine.add_bullet("Phase 3: Variable-Arity (Varargs):", "(e.g., `int... args` is evaluated only as a last resort).")

    code_overload_precedence = """public class OverloadResolution {
    static void print(long a)      { System.out.println("1. Widened Primitive (long)"); }
    static void print(Integer a)   { System.out.println("2. Autoboxed (Integer)"); }
    static void print(int... args) { System.out.println("3. Varargs (int...)"); }

    public static void main(String[] args) {
        int val = 42;
        print(val); // Compiler prioritizes Widening over Autoboxing!
        // Output: "1. Widened Primitive (long)"
    }
}"""
    engine.add_code("Java Method Overload Resolution Precedence", "java", code_overload_precedence)

    engine.add_h2("7.3 Under the Hood of JVM Dynamic Method Dispatch: vtable & itable")
    engine.add_body(
        "How does the JVM know which overridden method to execute when calling `animal.makeSound()` on an `Animal` reference pointing to a `Dog` heap object?"
    )
    engine.add_body(
        "At the bytecode level, the compiler generates the `invokevirtual` instruction. The HotSpot JVM executes dynamic dispatch using the Virtual Method Table (`vtable`):"
    )
    engine.add_bullet("1. Class vtable Creation:", "When the ClassLoader loads a class into Metaspace, HotSpot builds an array of method pointers (the `vtable`). The subclass inherits the parent's vtable array slots.")
    engine.add_bullet("2. Method Overriding in vtable:", "If the subclass overrides `makeSound()`, the pointer at that specific vtable index is overwritten to point to the subclass's compiled method bytecode.")
    engine.add_bullet("3. Runtime Invocation:", "When `invokevirtual` executes: (1) JVM reads the object's Klass Pointer from its header to locate the runtime class metadata, (2) Indexes into the class's `vtable` at the predetermined offset, (3) Jumps directly to the target method bytecode.")

    headers_bytecode = ["Bytecode Instruction", "Target Method Type", "Dispatch Mechanism"]
    rows_bytecode = [
        ["`invokevirtual`", "Public and protected non-interface instance methods", "Dynamic dispatch via class `vtable`"],
        ["`invokeinterface`", "Methods invoked through an interface reference", "Dynamic dispatch via interface table (`itable`)"],
        ["`invokestatic`", "Static methods (`ClassName.method()`)", "Static binding at compile time (no `this` pointer)"],
        ["`invokespecial`", "Private methods, constructors (`<init>`), and `super.method()`", "Static binding directly to specific class (bypasses dynamic override)"],
        ["`invokedynamic`", "Lambdas and dynamic language invocations (Java 7+)", "Bootstrap Method (BSM) linked call site"]
    ]
    engine.add_table(headers_bytecode, rows_bytecode, [Inches(1.8), Inches(2.6), Inches(2.6)])

    engine.add_h2("7.4 Upcasting, Downcasting & Pattern Matching (Java 16+)")
    engine.add_body(
        "Upcasting (assigning a child object to a parent reference) is completely safe and implicit. Downcasting (assigning a parent reference to a child variable) is dangerous and requires an explicit cast. If the underlying object is not an instance of the target type, the JVM throws `ClassCastException`."
    )
    engine.add_body(
        "Java 16 introduced Pattern Matching for `instanceof`, eliminating tedious boilerplate casting:"
    )

    code_pattern_matching = """public class PatternMatchingDemo {
    // OLD JAVA (Pre-Java 16): Verbose and error-prone
    public static void oldProcess(Object obj) {
        if (obj instanceof String) {
            String s = (String) obj; // Manual, redundant cast!
            System.out.println("Length: " + s.length());
        }
    }

    // MODERN JAVA 16+: Pattern Matching for instanceof
    public static void modernProcess(Object obj) {
        // Declares binding variable 's' directly in the condition!
        if (obj instanceof String s && !s.isBlank()) {
            System.out.println("Clean length: " + s.length()); // 's' is immediately available!
        }
    }
}"""
    engine.add_code("Modern Java 16+ Pattern Matching for instanceof", "java", code_pattern_matching)

    engine.add_callout(
        "Covariant Return Types in Java",
        [
            "In Java 5+, an overriding method can declare a return type that is a subclass of the superclass method's return type.",
            "Example: If `Animal` declares `public Animal reproduce()`, the `Dog` class may override it as `public Dog reproduce()`.",
            "This eliminates the need for callers to cast the returned object!"
        ],
        box_type="success"
    )
