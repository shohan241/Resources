from docx.shared import Inches

def build_ch10(engine):
    engine.add_chapter(
        10, 
        "The SOLID Design Principles (Java Edition)",
        "Exhaustive architectural breakdown of all 5 SOLID principles with real-world violating anti-patterns and clean, production-grade Java refactored code."
    )

    engine.add_h2("10.1 Single Responsibility Principle (SRP)")
    engine.add_body(
        "Definition (Robert C. Martin): 'A class should have one, and only one, reason to change.' A class should be responsible to only one actor or business domain. When a class mixes business calculations, persistence, and reporting, changes to database schemas or HTML formats threaten the stability of the core business logic."
    )

    code_srp = """// VIOLATING SRP: God Object with 3 distinct reasons to change!
public class Invoice {
    private double amount;
    public Invoice(double amt) { this.amount = amt; }

    // Reason 1: Business Calculation
    public double calculateTotalWithTax() { return amount * 1.15; }

    // Reason 2: Database Persistence (Violates SRP!)
    public void saveToDatabase() {
        System.out.println("Executing SQL: INSERT INTO invoices VALUES (" + amount + ")");
    }

    // Reason 3: Presentation / Formatting (Violates SRP!)
    public void printInvoiceHTML() {
        System.out.println("<html><body>Total: " + calculateTotalWithTax() + "</body></html>");
    }
}

// -------------------------------------------------------------
// REFACTORED SRP: Cohesive, Segregated Classes
// -------------------------------------------------------------
public class Invoice {
    private final double amount;
    public Invoice(double amt) { this.amount = amt; }
    public double getAmount() { return amount; }
    public double calculateTotal(double taxRate) { return amount * (1.0 + taxRate); }
}

public class InvoiceRepository {
    public void save(Invoice invoice) {
        System.out.println("Saving invoice to DB: " + invoice.getAmount());
    }
}

public class InvoiceHtmlPrinter {
    public void print(Invoice invoice) {
        System.out.println("<html><body>Total: " + invoice.calculateTotal(0.15) + "</body></html>");
    }
}"""
    engine.add_code("SRP Violation vs Clean Refactored Java Architecture", "java", code_srp)

    engine.add_h2("10.2 Open/Closed Principle (OCP)")
    engine.add_body(
        "Definition: 'Software entities should be open for extension, but closed for modification.' You should be able to introduce new functionality without altering existing, tested source code. Achieved primarily via polymorphic interfaces and strategy patterns."
    )

    code_ocp = """// VIOLATING OCP: Every new payment method requires editing this class!
public class FaultyPaymentProcessor {
    public void processPayment(String paymentType, double amount) {
        if ("CREDIT_CARD".equalsIgnoreCase(paymentType)) {
            System.out.println("Charging Credit Card: $" + amount);
        } else if ("PAYPAL".equalsIgnoreCase(paymentType)) {
            System.out.println("Routing to PayPal: $" + amount);
        } else if ("BITCOIN".equalsIgnoreCase(paymentType)) { // Forces code modification!
            System.out.println("Transferring Bitcoin: $" + amount);
        }
    }
}

// -------------------------------------------------------------
// REFACTORED OCP: Polymorphic Open/Closed Architecture
// -------------------------------------------------------------
public interface PaymentMethod {
    void pay(double amount);
}

public class CreditCardPayment implements PaymentMethod {
    public void pay(double amount) { System.out.println("Charging Credit Card: $" + amount); }
}

public class PayPalPayment implements PaymentMethod {
    public void pay(double amount) { System.out.println("Routing to PayPal: $" + amount); }
}

// PaymentService is CLOSED to modification, but OPEN to new payment extensions!
public class PaymentService {
    public void executePayment(PaymentMethod method, double amount) {
        method.pay(amount); // Polymorphic dispatch!
    }
}"""
    engine.add_code("OCP Violation vs Polymorphic Open/Closed Design", "java", code_ocp)

    engine.add_h2("10.3 Liskov Substitution Principle (LSP)")
    engine.add_body(
        "Definition (Barbara Liskov, 1987): 'Subtypes must be substitutable for their base types without altering the correctness of the program.' If a client program uses a base class reference, passing any subclass must never produce unexpected side effects, broken invariants, or unnatural exceptions."
    )
    engine.add_body(
        "The Classic LSP Trap: A Square is a Rectangle mathematically, but NOT in object-oriented behavior. A Rectangle allows width and height to vary independently; forcing a Square into this hierarchy forces setters to mutate both dimensions simultaneously, breaking caller expectations."
    )

    code_lsp = """// VIOLATING LSP: Square mutates expected Rectangle behavior
public class Rectangle {
    protected int width, height;
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int getArea() { return width * height; }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(int w) { this.width = this.height = w; }  // Unexpected side effect!
    @Override
    public void setHeight(int h) { this.width = this.height = h; } // Unexpected side effect!
}

public class LSPTester {
    public static void verify(Rectangle r) {
        r.setWidth(10);
        r.setHeight(5);
        // Expectation: Area MUST be 10 * 5 = 50!
        // But if 'r' is a Square, area is 5 * 5 = 25! LSP VIOLATION!
        assert r.getArea() == 50 : "Broken assumption!";
    }
}"""
    engine.add_code("The Classic Rectangle-Square LSP Violation", "java", code_lsp)

    engine.add_h2("10.4 Interface Segregation Principle (ISP)")
    engine.add_body(
        "Definition: 'Clients should not be forced to depend upon interfaces that they do not use.' Fat, bloated interfaces force implementers to write empty method stubs or throw `UnsupportedOperationException`. Break monolithic interfaces into small, cohesive, role-based contracts."
    )

    code_isp = """// VIOLATING ISP: Fat Interface forcing unnatural dummy implementations
public interface Worker {
    void work();
    void eat();
    void sleep();
}

public class RobotWorker implements Worker {
    public void work() { System.out.println("Robot working 24/7"); }
    public void eat() { throw new UnsupportedOperationException("Robots do not eat!"); } // POLLUTION!
    public void sleep() { throw new UnsupportedOperationException("Robots do not sleep!"); } // POLLUTION!
}

// -------------------------------------------------------------
// REFACTORED ISP: Segregated Role Interfaces
// -------------------------------------------------------------
public interface Workable { void work(); }
public interface Feedable { void eat(); }
public interface Sleepable { void sleep(); }

public class HumanWorker implements Workable, Feedable, Sleepable {
    public void work() { System.out.println("Human working"); }
    public void eat() { System.out.println("Human eating lunch"); }
    public void sleep() { System.out.println("Human sleeping"); }
}

public class Robot implements Workable {
    public void work() { System.out.println("Robot assembling electronics"); } // Zero bloat!
}"""
    engine.add_code("ISP Fat Interface vs Granular Segregated Interfaces", "java", code_isp)

    engine.add_h2("10.5 Dependency Inversion Principle (DIP)")
    engine.add_body(
        "Definition: 'High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions.' High-level business orchestrators should never instantiate low-level databases or notification clients directly. Instead, dependencies are injected via interfaces (Inversion of Control via Constructor Injection)."
    )

    code_dip = """// REFACTORED DIP: High-level business logic decoupled from low-level details
public interface NotificationChannel {
    void sendNotification(String recipient, String message);
}

public class EmailNotificationChannel implements NotificationChannel {
    public void sendNotification(String recipient, String message) {
        System.out.println("Sending SMTP email to " + recipient + ": " + message);
    }
}

public class SmsNotificationChannel implements NotificationChannel {
    public void sendNotification(String recipient, String message) {
        System.out.println("Sending SMS text to " + recipient + ": " + message);
    }
}

// High-level service depends strictly on the NotificationChannel abstraction:
public class OrderNotificationService {
    private final NotificationChannel channel; // Injected abstraction

    // Constructor Injection (Dependency Inversion / IoC)
    public OrderNotificationService(NotificationChannel channel) {
        this.channel = channel;
    }

    public void notifyCustomer(String customer, String orderStatus) {
        channel.sendNotification(customer, "Order update: " + orderStatus);
    }
}"""
    engine.add_code("Dependency Inversion via Constructor Injection in Java", "java", code_dip)

    engine.add_callout(
        "The SOLID Health Checklist for Senior Engineers",
        [
            "S: Does your class have more than one reason to change? If so, break it into cohesive services.",
            "O: Can you add new business capabilities without editing previously tested `.java` files?",
            "L: Can any child class replace its parent without throwing unexpected runtime exceptions?",
            "I: Are your interfaces clean and role-specific, or do they force classes to implement empty dummy methods?",
            "D: Are your services accepting interfaces via constructor injection rather than using `new ConcreteService()`?"
        ],
        box_type="success"
    )
