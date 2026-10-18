from docx.shared import Inches

def build_ch06(engine):
    engine.add_chapter(
        6, 
        "Inheritance & Class Hierarchies in Java",
        "Deep exploration of class inheritance, why Java bans multiple class inheritance, constructor sequencing, the 4 rules of method overriding, the final keyword, and the Fragile Base Class problem."
    )

    engine.add_h2("6.1 The 'Is-A' Taxonomy")
    engine.add_body(
        "Inheritance allows a subclass to acquire methods and fields from a superclass using the `extends` keyword, establishing an 'Is-A' relationship. Java supports Single Inheritance, Multilevel Inheritance, and Hierarchical Inheritance. However, Java STRICTLY PROHIBITS Multiple Class Inheritance."
    )

    engine.add_h2("6.2 Why Java Banned Multiple Class Inheritance (The Diamond Problem)")
    engine.add_body(
        "If class `D` were allowed to inherit from both `B` and `C`, and both `B` and `C` inherited from `A`, severe architectural ambiguities arise: (1) If class `A` has an instance field `int count;`, does `D` contain one copy or two copies of `count` in its heap layout? (2) If both `B` and `C` override `void execute()`, which implementation does `D` execute? To maintain simplicity, prevent JVM memory layout bloat, and eliminate constructor ambiguity, Java designers restricted classes to single inheritance while allowing multiple interface implementation."
    )

    engine.add_h2("6.3 The Four Non-Negotiable Rules of Method Overriding in Java")
    engine.add_body(
        "When a subclass provides a specific implementation of a method defined in its superclass, the JVM enforces four strict compile-time rules:"
    )
    engine.add_bullet("Rule 1 (Signature Identity):", "The method name and argument parameter list must match the parent method exactly.")
    engine.add_bullet("Rule 2 (Access Level Cannot Be Reduced):", "The overriding method cannot be more restrictive than the parent method. If the superclass method is `protected`, the subclass method may be `protected` or `public`, but NEVER `default` or `private`.")
    engine.add_bullet("Rule 3 (Covariant Return Types):", "The return type of the overriding method must be identical to, or a subtype of, the return type declared in the superclass method.")
    engine.add_bullet("Rule 4 (Exception Restriction):", "The overriding method CANNOT throw new or broader CHECKED exceptions than declared by the superclass method. It may throw fewer exceptions, narrower subclasses of exceptions, or no exceptions at all (unchecked RuntimeExceptions are unrestricted).")

    code_overriding_rules = """import java.io.IOException;
import java.io.FileNotFoundException;

class StorageService {
    // Parent method: protected, returns Object, throws IOException
    protected Object fetchFile(String path) throws IOException {
        System.out.println("Fetching raw object from: " + path);
        return new Object();
    }
}

class S3StorageService extends StorageService {
    // 1. Access widened from 'protected' to 'public' (LEGAL)
    // 2. Return type narrowed from Object to String (Covariant Return - LEGAL)
    // 3. Exception narrowed from IOException to FileNotFoundException (LEGAL)
    @Override
    public String fetchFile(String path) throws FileNotFoundException {
        System.out.println("Fetching S3 string from: " + path);
        return "S3_BUCKET_PAYLOAD";
    }
}"""
    engine.add_code("The 4 Rules of Method Overriding in Java", "java", code_overriding_rules)

    engine.add_h2("6.4 The 'final' Keyword in Java")
    engine.add_body(
        "The `final` modifier establishes immutability and restriction across three dimensions:"
    )

    headers_final = ["Dimension", "Syntax", "Architectural Effect"]
    rows_final = [
        ["Final Variable", "`final int MAX = 100;`", "Constant value. Once assigned, cannot be reassigned. For object references, the memory address is fixed (internal fields can still mutate unless object is immutable)."],
        ["Final Method", "`public final void verify();`", "Cannot be overridden by any subclass. Enables HotSpot JVM JIT compiler to inline the method bytecode for high performance."],
        ["Final Class", "`public final class String {}`", "Cannot be extended/subclassed. Guarantees security and immutable integrity (e.g., `String`, `Integer`)."]
    ]
    engine.add_table(headers_final, rows_final, [Inches(1.5), Inches(2.2), Inches(3.3)])

    engine.add_h2("6.5 Favor Composition Over Inheritance (The Fragile Base Class Problem)")
    engine.add_body(
        "Inheritance exposes the internal implementation details of superclasses to subclasses (white-box reuse). Changes in a superclass can silently break subclasses without compiler warnings. Joshua Bloch famously demonstrated this by extending `HashSet` to count added elements:"
    )

    code_fragile_base = """// BROKEN: Fragile Base Class Trap
import java.util.HashSet;
import java.util.Collection;
import java.util.List;

public class InstrumentedHashSet<E> extends HashSet<E> {
    private int addCount = 0;

    @Override
    public boolean add(E e) {
        addCount++;
        return super.add(e);
    }

    @Override
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c); // DANGER: HashSet.addAll() internally calls add()!
    }

    public int getAddCount() { return addCount; }

    public static void main(String[] args) {
        InstrumentedHashSet<String> set = new InstrumentedHashSet<>();
        set.addAll(List.of("A", "B", "C"));
        // We added 3 elements. What is addCount?
        System.out.println("Add count: " + set.getAddCount()); 
        // OUTPUT: 6! (Double counted because super.addAll calls our overridden add()!)
    }
}"""
    engine.add_code("The Fragile Base Class Problem with Java Inheritance", "java", code_fragile_base)

    engine.add_callout(
        "Solution: Composition with Forwarding (Decorator Pattern)",
        [
            "Instead of extending a concrete class (`extends HashSet`), give your class a private reference to the interface (`private final Set<E> set;`).",
            "This completely decouples your class from internal superclass implementation quirks, creating resilient, testable code."
        ],
        box_type="warning"
    )
