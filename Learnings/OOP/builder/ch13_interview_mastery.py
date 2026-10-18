from docx.shared import Inches

def build_ch13(engine):
    engine.add_chapter(
        13, 
        "Top 35+ Java OOP Technical Interview Questions & High-Scoring Model Answers",
        "Curated, definitive answers to the most frequently asked Java OOP and JVM questions in FAANG, top-tier engineering interviews, and enterprise systems design exams."
    )

    qa_list = [
        (
            "Q1: Is Java strictly pass-by-value or pass-by-reference?",
            "Java is strictly 100% PASS-BY-VALUE. When passing primitive variables, a copy of the raw bits is passed. When passing object references, a copy of the 32-bit or 64-bit reference address pointing to the heap is passed by value. Modifying an object's fields mutates the shared heap object, but reassigning the reference variable itself (`obj = new Object()`) changes only the callee's local stack copy, leaving the caller's reference unchanged."
        ),
        (
            "Q2: What is the exact technical difference between Abstraction and Encapsulation?",
            "Abstraction is OUTSIDE-IN interface design: hiding internal implementation complexity and exposing only the essential public contract to clients (e.g., `List` interface hides array/linked-node mechanics). Encapsulation is INSIDE-OUT boundary protection: bundling fields with methods and restricting direct field access via `private` access modifiers to preserve class invariants."
        ),
        (
            "Q3: Why doesn't Java support multiple class inheritance?",
            "To eliminate the Diamond Problem and state ambiguity. If Class A defines instance field `int x`, and classes B and C inherit from A, and D inherits from both B and C: (1) Does D have one copy or two copies of `x` in its heap layout? (2) Which constructor initializes `x`? Java avoids this memory layout bloat by allowing single class inheritance (`extends`), but permitting multiple interface implementation (`implements`)."
        ),
        (
            "Q4: What is the contract between equals() and hashCode() in Java?",
            "1. If `o1.equals(o2)` is true, their `hashCode()` values MUST be identical. 2. If `o1.hashCode() == o2.hashCode()`, the objects are NOT necessarily equal (hash collision). Violating this contract breaks `HashMap` and `HashSet`: equal objects are placed into different hash buckets, making them impossible to retrieve via `.get()`."
        ),
        (
            "Q5: Why is String immutable in Java?",
            "1. Security: Strings are used for database URLs, file paths, and network sockets; immutability prevents unauthorized tampering. 2. Thread Safety: Safe across concurrent threads without locks. 3. String Constant Pool (SCP): Allows the JVM to cache identical string literals, saving massive heap RAM. 4. HashCode Caching: The hash code is computed once during creation and cached (`private int hash`), making `HashMap` lookups O(1)."
        ),
        (
            "Q6: What is the difference between String, StringBuilder, and StringBuffer?",
            "`String` is immutable; every modification creates a new heap object. `StringBuilder` is mutable and not thread-safe (fastest for single-threaded string concatenation). `StringBuffer` is mutable and thread-safe (its methods are `synchronized`, incurring lock overhead)."
        ),
        (
            "Q7: What is the Java Integer Cache and what is its range?",
            "To save heap memory, the Java compiler caches `Integer` objects for values from -128 to 127 via `Integer.valueOf()`. Comparing two `Integer` references in this range using `==` returns `true` (same cached instance), but comparing values >= 128 returns `false` (different heap instances). Always compare wrappers using `.equals()`!"
        ),
        (
            "Q8: Can static methods be overridden in Java?",
            "NO. If a subclass declares a static method with the same signature, it is Method Hiding, not overriding. Static methods are bound at compile time based on the reference type via the `invokestatic` bytecode instruction, bypassing the virtual method table (`vtable`)."
        ),
        (
            "Q9: Can a constructor be declared final, static, or abstract?",
            "No. A constructor cannot be `final` because constructors are never inherited and cannot be overridden. A constructor cannot be `static` because it belongs strictly to instance initialization and requires a `this` reference. A constructor cannot be `abstract` because it must instantiate the object's memory directly."
        ),
        (
            "Q10: Why was finalize() deprecated and marked for removal?",
            "1. Non-deterministic execution: The JVM provides no guarantee when or if finalizers run. 2. Object resurrection: Finalizers can reassign `this` to a static field, resurrecting dead objects. 3. Performance penalty: Finalizable objects must survive at least one extra GC cycle. Solution: Use `AutoCloseable` with `try-with-resources`."
        ),
        (
            "Q11: How does try-with-resources work and what interface is required?",
            "Introduced in Java 7, `try-with-resources` automatically closes any resource implementing `java.lang.AutoCloseable` when the `try` block exits. It guarantees deterministic cleanup even if exceptions are thrown and properly captures suppressed exceptions via `Throwable.getSuppressed()`."
        ),
        (
            "Q12: Explain the Weak Generational Hypothesis in JVM Garbage Collection.",
            "Empirical evidence proves >95% of allocated objects die shortly after creation. HotSpot divides the Heap into Young Generation (Eden, S0, S1) and Old Generation. Young Gen uses fast Minor GC copying algorithms. Objects surviving 15 GC cycles are promoted to Old Gen, which is collected less frequently via Major/Full GC."
        ),
        (
            "Q13: What are the 4 Reference Types in Java (java.lang.ref)?",
            "1. StrongReference: Standard reference; never collected while reachable. 2. SoftReference: Collected only before OutOfMemoryError; used for memory-sensitive caches. 3. WeakReference: Collected on the very next GC run; used in `WeakHashMap` to prevent memory leaks. 4. PhantomReference: Enqueued after finalization; used for low-level off-heap resource cleanup."
        ),
        (
            "Q14: How do vtable and itable work under the hood during dynamic method dispatch?",
            "For each loaded class, the HotSpot JVM constructs a Virtual Method Table (`vtable`) in Metaspace containing an array of method pointers. When `invokevirtual` executes: (1) Reads Klass pointer from object header, (2) Indexes into the class's `vtable` at a fixed offset, (3) Jumps directly to the overridden method bytecode. Interface references use an `itable` (Interface Table)."
        ),
        (
            "Q15: What are the differences between invokevirtual, invokespecial, and invokestatic?",
            "`invokevirtual` performs dynamic dispatch via `vtable` for public/protected instance methods. `invokestatic` performs static binding for static methods. `invokespecial` performs static binding for constructors (`<init>`), private methods, and `super.method()` calls."
        ),
        (
            "Q16: What are Covariant Return Types in Java?",
            "An overriding subclass method may declare a return type that is a subtype of the superclass method's return type (e.g., `public Dog clone()` overriding `public Animal clone()`). This eliminates the need for manual downcasting by the caller."
        ),
        (
            "Q17: What are the 4 strict rules of Method Overriding in Java?",
            "1. Signature (name and parameter types) must match exactly. 2. Access modifier cannot be more restrictive than the parent method. 3. Return type must be identical or covariant. 4. The overriding method CANNOT throw new or broader CHECKED exceptions."
        ),
        (
            "Q18: What is the difference between Checked and Unchecked Exceptions in Java OOP?",
            "Checked Exceptions (subclasses of `Exception` excluding `RuntimeException`) represent recoverable external failures (e.g., `IOException`, `SQLException`) and are verified at compile time. Unchecked Exceptions (subclasses of `RuntimeException` and `Error`) represent programming bugs (e.g., `NullPointerException`, `IndexOutOfBoundsException`) and do not require explicit handling."
        ),
        (
            "Q19: What is the Liskov Substitution Principle (LSP) and what is the classic violation?",
            "Subtypes must be substitutable for their base types without altering program correctness. The classic violation is `Square extends Rectangle`: mutating width inadvertently mutates height, breaking tests that assume width and height are independent dimensions."
        ),
        (
            "Q20: Why should we favor Composition over Inheritance (Fragile Base Class)?",
            "Inheritance creates tight white-box coupling where changes in superclass method dispatch (e.g., `HashSet.addAll()` calling `add()`) break subclass counting invariants. Composition establishes loose black-box coupling through interfaces, allowing behaviors to be mocked in unit tests and swapped at runtime."
        ),
        (
            "Q21: Why is volatile mandatory in Double-Checked Locking Singletons?",
            "Object creation `instance = new Singleton()` involves 3 JVM steps: (1) Allocate memory, (2) Initialize object fields, (3) Assign address to `instance`. Without `volatile`, the CPU/JIT compiler may reorder steps to 1 -> 3 -> 2. Another thread checking `instance == null` sees a non-null reference to a partially-initialized object, causing catastrophic runtime crashes."
        ),
        (
            "Q22: Why does Joshua Bloch recommend Enum Singletons?",
            "An Enum Singleton (`public enum Singleton { INSTANCE; }`) is 100% thread-safe by the JVM classloader, immune to reflection attacks (calling `Constructor.newInstance()` on enums throws `IllegalArgumentException`), and handles serialization automatically without duplicate instances."
        ),
        (
            "Q23: What is the difference between Static Nested Classes and Non-Static Inner Classes?",
            "A static nested class (`static class Nested {}`) is completely decoupled and does NOT hold a reference to the outer instance. A non-static inner class (`class Inner {}`) contains an implicit hidden reference `OuterClass.this`. If an inner instance is passed to a background thread or static collection, it prevents the outer instance from being garbage collected, causing a memory leak."
        ),
        (
            "Q24: What is Defensive Copying?",
            "Creating clones of mutable objects during constructor assignment and getter retrieval. If a class stores a `Date` or `List` directly, external callers can mutate private state through their retained reference. Defensive copying preserves strict encapsulation."
        ),
        (
            "Q25: What are the 5 rules for creating an Immutable Class in Java?",
            "1. No setter methods. 2. Mark class `final` to prevent subclassing. 3. Make all fields `final`. 4. Make all fields `private`. 5. Use defensive copying for any mutable field."
        ),
        (
            "Q26: What are Java Records (Java 16+)?",
            "Records (`record Point(int x, int y) {}`) are transparent, immutable data carriers. The compiler automatically generates `final` fields, canonical constructor, accessors (`x()` and `y()`), `equals()`, `hashCode()`, and `toString()`. Records cannot extend other classes (they extend `java.lang.Record`) and are implicitly `final`."
        ),
        (
            "Q27: What is the 'Tell, Don't Ask' principle?",
            "Command objects to execute operations on their own data instead of asking for their data, performing calculations externally, and setting the result back. It preserves domain logic encapsulation within the entity."
        ),
        (
            "Q28: What is an Anemic Domain Model?",
            "An entity that contains only fields and mindless getters and setters without business validation. Business logic leaks into service layers, leading to code duplication and broken domain invariants."
        ),
        (
            "Q29: What is the Lapsed Listener Problem in Java?",
            "When an observer registers with a subject, the subject holds a strong reference to it. If the client discards the observer without unsubscribing, the Garbage Collector cannot reclaim it, causing a permanent memory leak. Solution: Use `WeakReference` or explicit lifecycle deregistration."
        ),
        (
            "Q30: Why were default methods added to Java 8 interfaces?",
            "To allow interface evolution without breaking backwards compatibility. For instance, Java 8 added `.stream()` to `java.util.Collection`; default methods allowed existing collection implementations across the globe to compile and run without needing to implement `.stream()` manually."
        ),
        (
            "Q31: How does Java resolve Interface Default Method collisions (Diamond Problem)?",
            "If a class implements two interfaces sharing an identical default method signature, the compiler throws an ambiguity error. The implementing class MUST override the method and explicitly invoke the desired interface implementation using `InterfaceName.super.method()`."
        ),
        (
            "Q32: What is the Dependency Inversion Principle (DIP)?",
            "High-level business policies should not depend on low-level implementation details; both must depend on abstractions. Implemented via Constructor Dependency Injection, allowing databases or network clients to be swapped without modifying business services."
        ),
        (
            "Q33: What is Pattern Matching for instanceof (Java 16)?",
            "A modern Java syntax enhancement that combines type checking and casting into a single atomic expression: `if (obj instanceof String s) { System.out.println(s.length()); }`, eliminating redundant, unsafe casts."
        ),
        (
            "Q34: What is the difference between Factory Method and Abstract Factory?",
            "Factory Method relies on inheritance to instantiate a single product via an overridden method. Abstract Factory uses object composition to produce complete families of related or dependent objects without specifying their concrete classes."
        ),
        (
            "Q35: Can an interface have private methods in Java?",
            "Yes! Starting in Java 9, interfaces can declare `private` and `private static` methods. They are used to share common helper logic between multiple `default` methods without exposing the code to the public API."
        )
    ]

    for q, a in qa_list:
        engine.add_h3(q)
        engine.add_body(a, bold_prefix="High-Scoring Model Answer: ")

    engine.add_callout(
        "FAANG Technical Interview Strategy",
        [
            "1. Ground every Java OOP answer in JVM internals: mention memory layout, stack vs heap, classloader, or HotSpot vtable dispatch.",
            "2. When discussing design principles, connect high-level rules (SOLID, GoF) to concrete production trade-offs: latency, thread safety, and maintainability.",
            "3. Always highlight modern Java features (Records, Pattern Matching, try-with-resources) to demonstrate current enterprise-level competence."
        ],
        box_type="success"
    )
