from docx.shared import Inches

def build_ch03(engine):
    engine.add_chapter(
        3, 
        "Object Lifecycle, Garbage Collection & Resource Management",
        "Mastering the stages of a Java object, constructor chaining, the deprecation of finalize(), modern try-with-resources, Generational GC mechanics, and Java's 4 Reference Types."
    )

    engine.add_h2("3.1 The Life Cycle of a Java Object")
    engine.add_body(
        "A Java object moves through a deterministic series of JVM phases: (1) Class Loading & Verification, (2) Heap Memory Allocation, (3) Default Zero-Value Field Initialization (e.g., `0`, `false`, `null`), (4) Explicit Field Initialization & Instance Block `{}` Execution, (5) Constructor Execution via `super()`, (6) Active Lifetime, (7) Unreachability Isolation, and (8) Garbage Collection Reclamation."
    )

    engine.add_h2("3.2 Constructor Chaining & Super Rules")
    engine.add_body(
        "When an object is created, its parent's constructor MUST be invoked before the child constructor executes. The compiler enforces strict syntactic rules:"
    )
    engine.add_bullet("1. Mandatory First Statement:", "The call to `super(...)` or `this(...)` must be the absolute FIRST line in any constructor. You cannot place code before it.")
    engine.add_bullet("2. Mutual Exclusivity:", "A constructor can contain `super()` OR `this()`, but NEVER both simultaneously.")
    engine.add_bullet("3. Implicit Default super():", "If you do not explicitly invoke `super()` or `this()`, the Java compiler automatically inserts an invisible `super();` call to the parent's no-argument constructor. If the parent does not have a no-arg constructor, a compilation error occurs.")

    code_constructor_chaining = """class Vehicle {
    protected String vin;
    public Vehicle(String vin) {
        this.vin = vin;
        System.out.println("1. Vehicle Constructor: VIN " + vin);
    }
}

class ElectricCar extends Vehicle {
    private int batteryCapacity;

    public ElectricCar(String vin) {
        this(vin, 75); // Constructor Chaining: Delegates to overloaded constructor
    }

    public ElectricCar(String vin, int batteryCapacity) {
        super(vin); // Parent constructor MUST be first!
        this.batteryCapacity = batteryCapacity;
        System.out.println("2. ElectricCar Constructor: " + batteryCapacity + " kWh");
    }
}"""
    engine.add_code("Java Constructor Chaining (super and this)", "java", code_constructor_chaining)

    engine.add_h2("3.3 Why finalize() is Deprecated and Hazardous")
    engine.add_body(
        "Historically, Java provided `protected void finalize()` in `Object`. Java 9 officially deprecated `finalize()`, and modern Java marks it for complete removal. Finalizers are dangerous because: (1) They run on an arbitrary, low-priority JVM thread with no execution time guarantee; (2) They can accidentally resurrect dead objects by assigning `this` to a static field; (3) Objects with finalizers must survive at least one extra GC cycle, causing severe memory bloat and latency spikes."
    )

    engine.add_h2("3.4 Deterministic Resource Cleanup: AutoCloseable & try-with-resources")
    engine.add_body(
        "Introduced in Java 7, `try-with-resources` provides deterministic cleanup for OS resources (sockets, database connections, file handles). Any class that implements `java.lang.AutoCloseable` will have its `close()` method invoked automatically when the `try` block exits, even if an unhandled exception is thrown."
    )

    code_try_with_resources = """import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ResourceManagementDemo {
    // Custom AutoCloseable Resource
    static class DatabaseConnection implements AutoCloseable {
        public void executeQuery(String sql) { System.out.println("Executing: " + sql); }
        @Override
        public void close() { System.out.println("DatabaseConnection cleanly closed."); }
    }

    public static void main(String[] args) {
        // try-with-resources guarantees deterministic closure!
        try (DatabaseConnection conn = new DatabaseConnection()) {
            conn.executeQuery("SELECT * FROM users");
            // If an exception occurs here, conn.close() is STILL guaranteed to execute!
        } // 'conn.close()' runs automatically at this exact boundary
    }
}"""
    engine.add_code("Deterministic Cleanup with try-with-resources", "java", code_try_with_resources)

    engine.add_h2("3.5 Garbage Collection Mechanics: The Generational Hypothesis")
    engine.add_body(
        "The JVM Garbage Collector relies on the Weak Generational Hypothesis: empirically, over 95% of allocated objects die shortly after creation (temporary strings, local loop variables, DTOs). To optimize performance, the JVM divides the Heap into distinct generations:"
    )

    headers_gc = ["Heap Generation", "Sub-Regions", "Allocation & Collection Characteristics"]
    rows_gc = [
        ["Young Generation", "Eden Space, Survivor 0 (From), Survivor 1 (To)", "All new objects allocated in Eden. Minor GC runs frequently using fast Copying algorithms. Survivors age across S0 and S1."],
        ["Old / Tenured Generation", "Contiguous Tenured Space", "Objects that survive 15 Minor GC cycles (configurable via `-XX:MaxTenuringThreshold`) are promoted here. Collected via Major / Full GC."],
        ["Metaspace (Native OS)", "Klass Metadata, Constant Pool", "Allocated from native RAM. Reclaimed only when entire ClassLoaders become unreferenced and are unloaded."]
    ]
    engine.add_table(headers_gc, rows_gc, [Inches(1.8), Inches(2.2), Inches(3.0)])

    engine.add_h2("3.6 The Four Java Reference Types (Crucial for High-Performance Systems)")
    engine.add_body(
        "Java provides four levels of object reachability in `java.lang.ref` to allow fine-grained control over caching and memory reclamation:"
    )
    engine.add_bullet("1. StrongReference (Default):", "Standard variable assignment (`User u = new User();`). As long as a strong GC root reaches the object, it will NEVER be garbage collected. If heap runs out, the JVM throws `OutOfMemoryError` rather than collecting it.")
    engine.add_bullet("2. SoftReference<T>:", "Objects wrapped in `SoftReference` are retained as long as memory is sufficient. The GC reclaims them ONLY as a last resort before throwing `OutOfMemoryError`. Ideal for memory-sensitive in-memory caches.")
    engine.add_bullet("3. WeakReference<T>:", "Does not prevent GC collection. On the very next GC run, any object referenced ONLY by weak references is reclaimed immediately. Critical for canonical mappings (`WeakHashMap`) and event listener registries to prevent memory leaks.")
    engine.add_bullet("4. PhantomReference<T>:", "Enqueued in a `ReferenceQueue` AFTER the object has been physically finalized and reclaimed. Used for low-level off-heap memory cleanup and post-mortem resource monitoring.")

    code_weak_ref = """import java.lang.ref.WeakReference;

public class WeakReferenceDemo {
    public static void main(String[] args) {
        String data = new String("Heavy Payload Cache");
        WeakReference<String> weakRef = new WeakReference<>(data);

        System.out.println("Before GC: " + weakRef.get()); // Accessible

        data = null; // Clear the only STRONG reference!
        System.gc(); // Request JVM Garbage Collection

        // On next GC, the weakly referenced object is reclaimed!
        System.out.println("After GC: " + weakRef.get()); // Prints: null
    }
}"""
    engine.add_code("Java WeakReference Behavior & Garbage Collection", "java", code_weak_ref)

    engine.add_callout(
        "Architectural Takeaway: Memory Leaks in Java",
        [
            "Java does have memory leaks! A memory leak in Java occurs when unused objects remain reachable from a GC Root (such as uncleaned static collections, unremoved event listeners, or thread pools holding ThreadLocals).",
            "Always clean up static collections and use `WeakReference` or `WeakHashMap` when registering observers and listeners."
        ],
        box_type="alert"
    )
