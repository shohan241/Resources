from docx.shared import Inches

def build_ch08(engine):
    engine.add_chapter(
        8, 
        "Static Members, Advanced Enums & Nested Classes",
        "Deep exploration of static memory allocation, static method hiding vs. virtual overriding, Java Enums as rich OOP classes, and static vs. inner nested classes."
    )

    engine.add_h2("8.1 Static Variables & Methods in the Metaspace")
    engine.add_body(
        "The `static` keyword binds a member to the Class itself rather than any individual heap instance. Static fields are stored in the Metaspace (or class mirror in the heap) and are initialized when the class is loaded. Static methods do NOT receive an implicit `this` reference; therefore, they cannot access non-static instance fields or call non-static methods directly."
    )

    engine.add_h2("8.2 Static Method Hiding vs. Virtual Overriding (Critical Trap)")
    engine.add_body(
        "A common interview trap: Can static methods be overridden? NO. If a subclass declares a static method with the same signature as a superclass static method, it is called Method Hiding, NOT overriding. Static methods are resolved at compile-time based on the reference type (`invokestatic`), not the runtime object type!"
    )

    code_static_hiding = """class Parent {
    public static void display() {
        System.out.println("Parent static display");
    }
}

class Child extends Parent {
    // This HIDES Parent.display(), it does NOT override it!
    public static void display() {
        System.out.println("Child static display");
    }
}

public class StaticHidingDemo {
    public static void main(String[] args) {
        Parent ref = new Child();
        ref.display(); 
        // OUTPUT: "Parent static display"!
        // Statically bound to the reference type 'Parent' at compile time!
    }
}"""
    engine.add_code("Static Method Hiding vs Polymorphic Overriding", "java", code_static_hiding)

    engine.add_h2("8.3 Java Enums as Advanced OOP Classes")
    engine.add_body(
        "Unlike C/C++ where enums are mere integer wrappers, Java Enums (`enum`) are full-blown classes extending `java.lang.Enum`. They can declare private constructors, instance fields, regular methods, abstract methods, and constant-specific class bodies (implementing the Strategy Pattern directly inside the Enum!)."
    )

    code_enum_oop = """public enum Operation {
    PLUS("+") {
        @Override
        public double apply(double x, double y) { return x + y; }
    },
    MINUS("-") {
        @Override
        public double apply(double x, double y) { return x - y; }
    },
    MULTIPLY("*") {
        @Override
        public double apply(double x, double y) { return x * y; }
    },
    DIVIDE("/") {
        @Override
        public double apply(double x, double y) {
            if (y == 0) throw new ArithmeticException("Division by zero");
            return x / y;
        }
    };

    private final String symbol;

    // Enum constructors are strictly private
    Operation(String symbol) {
        this.symbol = symbol;
    }

    public String getSymbol() { return symbol; }

    // Constant-Specific Method: Enforces Strategy Pattern in each constant!
    public abstract double apply(double x, double y);
}

// Clean usage:
// double result = Operation.MULTIPLY.apply(4, 5); // 20.0"""
    engine.add_code("Java Enum as a Rich Strategy Pattern Entity", "java", code_enum_oop)

    engine.add_h2("8.4 Java Nested Classes: Static vs. Inner")
    engine.add_body(
        "Java permits classes to be defined within other classes. Understanding the memory implications of Static Nested Classes vs. Non-Static Inner Classes is vital to avoiding memory leaks:"
    )

    headers_nested = ["Category", "Declaration", "Implicit Outer Reference?", "Memory Leak Risk in Async / Listeners"]
    rows_nested = [
        ["Static Nested Class", "`static class Nested {}`", "NO (Completely decoupled; cannot access outer instance fields)", "Zero leak risk. Ideal for Builders and DTOs."],
        ["Non-Static Inner Class", "`class Inner {}`", "YES (`OuterClass.this` stored in every inner instance)", "HIGH: Holds outer instance in memory, preventing GC reclamation."],
        ["Anonymous Inner Class", "`new Runnable() { ... }`", "YES (Holds implicit outer reference if declared in non-static context)", "HIGH: Common source of memory leaks in thread pools."],
        ["Local Inner Class", "Inside a method body", "YES (Can also capture `effectively final` local variables)", "Moderate: Scoped strictly to method execution."]
    ]
    engine.add_table(headers_nested, rows_nested, [Inches(1.8), Inches(1.8), Inches(1.6), Inches(1.8)])

    engine.add_callout(
        "Joshua Bloch's Rule on Nested Classes",
        [
            "Favor static member classes over non-static member classes.",
            "If an inner class does not require access to the enclosing instance's state, ALWAYS mark it `static`. Omitting `static` wastes 4 to 8 bytes per instance for the hidden outer pointer and risks leaking the enclosing object in memory."
        ],
        box_type="warning"
    )
