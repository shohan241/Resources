from docx.shared import Inches

def build_ch05(engine):
    engine.add_chapter(
        5, 
        "Abstraction & Modern Java Interfaces",
        "Mastering abstraction, abstract classes, interface contracts, Java 8+ default and static methods, resolving interface diamond conflicts, and Functional Interfaces."
    )

    engine.add_h2("5.1 What is Abstraction?")
    engine.add_body(
        "Abstraction is the design practice of separating the 'What' (the public contract) from the 'How' (the private implementation). When a client interacts with a Java `List`, it relies on methods like `.add()` and `.get()` without caring whether the underlying memory structure is a contiguous array (`ArrayList`) or a doubly linked list (`LinkedList`). Abstraction decouples consumers from internal volatility."
    )

    engine.add_h2("5.2 Abstract Classes in Java")
    engine.add_body(
        "An Abstract Class (`abstract class`) serves as a partial template. Key characteristics:"
    )
    engine.add_bullet("1. Cannot Be Instantiated Directly:", "Attempting `new MyAbstractClass()` causes a compile-time error.")
    engine.add_bullet("2. Can Hold State:", "Can declare instance variables, constructors, static blocks, and full access modifiers (`private`, `protected`).")
    engine.add_bullet("3. Mixes Abstract and Concrete Behavior:", "Can provide complete default algorithms while deferring specific steps to subclasses via `abstract` methods.")

    code_abstract_class = """// Java Abstract Class with Shared Template Method
public abstract class PaymentProcessor {
    protected String merchantId; // Abstract classes CAN hold state!

    public PaymentProcessor(String merchantId) {
        this.merchantId = merchantId;
    }

    // Concrete Template Method: Defines the execution workflow
    public final void processTransaction(double amount) {
        authenticate();
        executePayment(amount); // Polymorphic hook!
        auditLog(amount);
    }

    // Pure Abstract Method: Subclasses MUST implement!
    protected abstract boolean executePayment(double amount);

    private void authenticate() {
        System.out.println("Authenticating merchant: " + merchantId);
    }

    private void auditLog(double amount) {
        System.out.println("Transaction audited: $" + amount);
    }
}"""
    engine.add_code("Java Abstract Class with Template Method Pattern", "java", code_abstract_class)

    engine.add_h2("5.3 Interfaces: Pure Architectural Contracts")
    engine.add_body(
        "An Interface in Java defines a pure contract specifying 'what' a class must do, but not 'how'. A class can implement multiple interfaces (`implements A, B, C`), overcoming Java's prohibition of multiple class inheritance."
    )

    headers_abs_iface = ["Comparison Criteria", "Abstract Class (`abstract class`)", "Interface (`interface`)"]
    rows_abs_iface = [
        ["Core Relationship", "Inheritance ('What it is' - Is-A)", "Contractual Capability ('What it can do' - Can-Do)"],
        ["Multiple Inheritance", "Single inheritance only (`extends SuperClass`)", "Multiple implementation allowed (`implements A, B`)"],
        ["State & Variables", "Can declare instance fields of any access level", "Cannot have instance state; fields are implicitly `public static final` constants"],
        ["Constructors", "Can declare constructors (called via `super()`)", "CANNOT have constructors"],
        ["Method Visibility", "Can have `private`, `protected`, and `public` methods", "Methods are implicitly `public` (or `private` since Java 9)"],
        ["Dispatch Overhead", "HotSpot JVM `vtable` lookup (fast)", "HotSpot JVM `itable` lookup (slightly more indirection)"],
        ["Architectural Intent", "Shared code and tight identity hierarchy", "Loose coupling and polymorphic plug-and-play capability"]
    ]
    engine.add_table(headers_abs_iface, rows_abs_iface, [Inches(1.5), Inches(2.75), Inches(2.75)])

    engine.add_h2("5.4 Java 8+ Interface Evolution: Default & Static Methods")
    engine.add_body(
        "Historically, adding a new method to an existing interface broke every class in the world implementing that interface. To permit interface evolution (such as adding `.stream()` to `java.util.Collection`), Java 8 introduced `default` methods."
    )

    engine.add_h2("5.5 Resolving the Diamond Conflict in Interface Default Methods")
    engine.add_body(
        "If a class implements two interfaces that provide identical default method signatures, the compiler halts with an ambiguity error. The implementing class MUST explicitly override the method and choose which interface implementation to call using `InterfaceName.super.method()`:"
    )

    code_diamond_interface = """interface EngineService {
    default void start() {
        System.out.println("Engine service initialized.");
    }
}

interface ElectricalService {
    default void start() {
        System.out.println("Electrical service powered on.");
    }
}

// Resolving Ambiguity via explicit override
public class HybridCar implements EngineService, ElectricalService {
    @Override
    public void start() {
        // Disambiguate using InterfaceName.super:
        EngineService.super.start();
        ElectricalService.super.start();
        System.out.println("HybridCar is fully operational.");
    }
}"""
    engine.add_code("Resolving Interface Default Method Collision in Java", "java", code_diamond_interface)

    engine.add_h2("5.6 Functional Interfaces & Single Abstract Method (SAM)")
    engine.add_body(
        "A Functional Interface is an interface that declares exactly ONE abstract method. Marked with the `@FunctionalInterface` annotation, it serves as the foundational bridge between Object-Oriented Programming and Functional Programming in Java, enabling Lambda Expressions and Method References."
    )

    code_functional_iface = """@FunctionalInterface
public interface Validator<T> {
    boolean validate(T item); // The Single Abstract Method (SAM)

    // Can still contain default and static methods:
    default Validator<T> and(Validator<T> other) {
        return item -> this.validate(item) && other.validate(item);
    }
}

// Lambda usage:
Validator<String> emailValidator = email -> email != null && email.contains("@");"""
    engine.add_code("Functional Interface & Lambda Expressions in Java", "java", code_functional_iface)

    engine.add_callout(
        "Design Rule: Abstract Class vs. Interface",
        [
            "Use an Abstract Class when classes share significant code, internal private state, and belong to a strict natural family tree.",
            "Use an Interface when defining a polymorphic capability (e.g., `Serializable`, `Comparable`, `AutoCloseable`) across completely unrelated classes."
        ],
        box_type="success"
    )
