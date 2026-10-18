from docx.shared import Inches

def build_ch11(engine):
    engine.add_chapter(
        11, 
        "Essential Gang of Four (GoF) Design Patterns in Java",
        "Mastering the 8 most critical industry design patterns across Creational, Structural, and Behavioral categories with thread-safe, production-ready Java code."
    )

    engine.add_h2("11.1 The Gang of Four Taxonomy in Enterprise Java")
    engine.add_body(
        "Design patterns represent reusable, battle-tested solutions to recurring software engineering challenges. Categorized by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (GoF), they span three operational domains:"
    )
    engine.add_bullet("1. Creational Patterns:", "Isolate instantiation logic, ensuring the client remains decoupled from concrete classes.")
    engine.add_bullet("2. Structural Patterns:", "Compose classes and objects into flexible, larger architectures without tight coupling.")
    engine.add_bullet("3. Behavioral Patterns:", "Orchestrate algorithms, state transitions, and communication contracts between objects.")

    engine.add_h2("11.2 Creational: The Three Thread-Safe Java Singletons")
    engine.add_body(
        "A Singleton ensures only one instance exists and provides a global access point. In multithreaded enterprise environments, naive singletons create duplicate instances due to thread race conditions."
    )

    code_singletons = """// 1. Double-Checked Locking Singleton (Industry Standard)
public class DclSingleton {
    // 'volatile' is MANDATORY to prevent CPU instruction reordering!
    // (1. Allocate memory -> 2. Initialize instance -> 3. Point reference)
    private static volatile DclSingleton instance;

    private DclSingleton() {}

    public static DclSingleton getInstance() {
        if (instance == null) { // 1st check: Avoids lock overhead once initialized
            synchronized (DclSingleton.class) {
                if (instance == null) { // 2nd check: Inside critical section
                    instance = new DclSingleton();
                }
            }
        }
        return instance;
    }
}

// 2. Bill Pugh Static Inner Class Singleton (Lazy, Zero-Lock Overhead)
public class BillPughSingleton {
    private BillPughSingleton() {}

    // Inner class is loaded into memory ONLY when getInstance() is called!
    private static class Holder {
        private static final BillPughSingleton INSTANCE = new BillPughSingleton();
    }

    public static BillPughSingleton getInstance() {
        return Holder.INSTANCE;
    }
}

// 3. Joshua Bloch's Enum Singleton (100% Reflection & Serialization Proof)
public enum EnumSingleton {
    INSTANCE;
    public void executeBusinessLogic() {
        System.out.println("Executing thread-safe operation");
    }
}"""
    engine.add_code("The Three Thread-Safe Java Singleton Implementations", "java", code_singletons)

    engine.add_h2("11.3 Creational: Fluent Builder Pattern")
    engine.add_body(
        "The Builder pattern solves the 'Telescoping Constructor' anti-pattern where constructors accept 10+ confusing parameters with multiple booleans and defaults."
    )

    code_builder = """public class HttpRequest {
    private final String url;
    private final String method;
    private final String body;
    private final int timeoutMs;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.body = builder.body;
        this.timeoutMs = builder.timeoutMs;
    }

    public static class Builder {
        private final String url;          // Required parameter
        private String method = "GET";     // Optional with default
        private String body = "";
        private int timeoutMs = 5000;

        public Builder(String url) { this.url = url; }
        public Builder method(String method) { this.method = method; return this; }
        public Builder body(String body) { this.body = body; return this; }
        public Builder timeout(int ms) { this.timeoutMs = ms; return this; }

        public HttpRequest build() { return new HttpRequest(this); }
    }
}

// Fluent Chaining Usage:
HttpRequest req = new HttpRequest.Builder("https://api.payments.com/charge")
        .method("POST")
        .body("{\\"amount\\": 100.0}")
        .timeout(2500)
        .build();"""
    engine.add_code("Java Fluent Builder Pattern", "java", code_builder)

    engine.add_h2("11.4 Structural: Decorator Pattern (Dynamic Behavior Stacking)")
    engine.add_body(
        "The Decorator Pattern attaches additional responsibilities to an object dynamically at runtime without subclassing (the exact architecture used by `java.io.BufferedReader(new InputStreamReader(...))`):"
    )

    code_decorator = """public interface Coffee {
    String getDescription();
    double getCost();
}

public class Espresso implements Coffee {
    public String getDescription() { return "Espresso"; }
    public double getCost() { return 2.50; }
}

// Base Decorator wraps Coffee
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee coffee) { this.decoratedCoffee = coffee; }
}

public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }
    public String getDescription() { return decoratedCoffee.getDescription() + ", Steamed Milk"; }
    public double getCost() { return decoratedCoffee.getCost() + 0.60; }
}

public class CaramelDecorator extends CoffeeDecorator {
    public CaramelDecorator(Coffee coffee) { super(coffee); }
    public String getDescription() { return decoratedCoffee.getDescription() + ", Caramel Drizzle"; }
    public double getCost() { return decoratedCoffee.getCost() + 0.75; }
}

// Dynamic Stacking:
// Coffee myOrder = new CaramelDecorator(new MilkDecorator(new Espresso()));
// Cost: 2.50 + 0.60 + 0.75 = $3.85"""
    engine.add_code("Java Decorator Pattern Dynamic Stacking", "java", code_decorator)

    engine.add_h2("11.5 Behavioral: Observer & Strategy Patterns")
    engine.add_body(
        "The Observer Pattern implements a one-to-many publish-subscribe model. The Strategy Pattern encapsulates interchangeable algorithms behind a shared interface."
    )

    code_strategy = """// Java Strategy Pattern: Dynamic Sorting Algorithms
import java.util.List;

public interface SortStrategy {
    void sort(List<Integer> dataset);
}

public class QuickSortStrategy implements SortStrategy {
    public void sort(List<Integer> dataset) { System.out.println("Sorting via O(N log N) QuickSort"); }
}

public class MergeSortStrategy implements SortStrategy {
    public void sort(List<Integer> dataset) { System.out.println("Sorting via Stable MergeSort"); }
}

public class SortContext {
    private SortStrategy strategy;
    public void setStrategy(SortStrategy strategy) { this.strategy = strategy; }
    public void executeSort(List<Integer> data) {
        if (strategy == null) throw new IllegalStateException("Strategy not set");
        strategy.sort(data); // Dynamic polymorphic execution!
    }
}"""
    engine.add_code("Java Strategy Pattern Interchangeable Algorithms", "java", code_strategy)

    engine.add_callout(
        "Gang of Four Pattern Selection Matrix",
        [
            "Need only one global instance with safe initialization? -> Singleton (Double-Checked or Enum)",
            "Complex constructor with multiple optional parameters? -> Builder",
            "Decouple object instantiation from calling code? -> Factory Method",
            "Bridge incompatible third-party interfaces? -> Adapter",
            "Dynamically stack features at runtime without subclass explosion? -> Decorator",
            "Interchangeable business algorithms or payment processors? -> Strategy",
            "Event-driven pub/sub state broadcasting? -> Observer"
        ],
        box_type="info"
    )
