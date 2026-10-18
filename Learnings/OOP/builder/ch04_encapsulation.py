from docx.shared import Inches

def build_ch04(engine):
    engine.add_chapter(
        4, 
        "Encapsulation, Defensive Copying & Immutability",
        "Deep exploration of information hiding, Java access modifier boundaries, anemic vs. rich domain models, defensive copying against state leaks, and Java 16+ records."
    )

    engine.add_h2("4.1 Information Hiding: The Real Meaning of Encapsulation")
    engine.add_body(
        "Encapsulation is not merely making fields `private` and generating getters and setters. True encapsulation is Information Hiding: enclosing data with the business behavior that governs it, protecting invariants, and shielding internal representations from external consumers so that internal changes do not break client code."
    )

    headers_access = ["Modifier", "Same Class", "Same Package", "Subclass (Different Package)", "World (Anywhere)"]
    rows_access = [
        ["`private`", "YES", "NO", "NO", "NO"],
        ["`default` (no modifier)", "YES", "YES", "NO", "NO"],
        ["`protected`", "YES", "YES", "YES (Inheritance access)", "NO"],
        ["`public`", "YES", "YES", "YES", "YES"]
    ]
    engine.add_table(headers_access, rows_access, [Inches(1.8), Inches(1.3), Inches(1.3), Inches(1.8), Inches(0.8)])

    engine.add_h2("4.2 The Getter/Setter Anti-Pattern & Anemic Domain Models")
    engine.add_body(
        "Mindlessly exposing getters and setters for all private fields produces an Anemic Domain Model. When business logic is pulled out of entities and scattered across service classes, objects are reduced to passive data holders, causing massive code duplication and broken invariants."
    )

    code_anemic_vs_rich = """// BAD: Anemic Domain Model (Zero Encapsulation)
public class AnemicBankAccount {
    private double balance;
    public double getBalance() { return balance; }
    public void setBalance(double balance) { this.balance = balance; }
}
// Client code must remember to validate logic:
// if (acc.getBalance() >= amt) acc.setBalance(acc.getBalance() - amt);

// -------------------------------------------------------------
// GOOD: Rich Domain Model (Encapsulated Invariants)
// -------------------------------------------------------------
public class RichBankAccount {
    private double balance;

    public RichBankAccount(double initialDeposit) {
        if (initialDeposit < 0) throw new IllegalArgumentException("Initial deposit cannot be negative");
        this.balance = initialDeposit;
    }

    // Business Operation: Protects invariants internally
    public void withdraw(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Withdrawal must be positive");
        if (amount > this.balance) throw new IllegalStateException("Insufficient funds");
        this.balance -= amount;
    }

    public double getBalance() { return this.balance; } // Read-only view
}"""
    engine.add_code("Anemic Domain Model vs Rich Encapsulated Domain Model", "java", code_anemic_vs_rich)

    engine.add_h2("4.3 Defensive Copying: Preventing Sneaky State Corruption")
    engine.add_body(
        "Even when all fields are marked `private`, if a class accepts or returns a reference to a mutable object (such as `java.util.Date`, arrays, or `List`), external code can mutate the object's internal state directly from the outside! Defensive Copying creates an independent clone during both input (constructor) and output (getter)."
    )

    code_defensive_copy = """import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

public final class UserSession {
    private final String userId;
    private final Date loginTime;               // Mutable object!
    private final List<String> permissions;    // Mutable collection!

    // Constructor with Defensive Copying
    public UserSession(String userId, Date loginTime, List<String> permissions) {
        this.userId = userId;
        // DEFENSIVE COPY: Do NOT store the caller's Date reference directly!
        this.loginTime = new Date(loginTime.getTime());
        // DEFENSIVE COPY: Copy collection elements into a new internal list
        this.permissions = new ArrayList<>(permissions);
    }

    // Getter with Defensive Copying
    public Date getLoginTime() {
        return new Date(this.loginTime.getTime()); // Return copy! Never return raw field!
    }

    // Returning an Unmodifiable View
    public List<String> getPermissions() {
        return Collections.unmodifiableList(this.permissions); // Prevents mutation attempts!
    }
}"""
    engine.add_code("Defensive Copying in Java Constructors and Getters", "java", code_defensive_copy)

    engine.add_h2("4.4 The 5 Rules for Immutable Classes & Java 16+ Records")
    engine.add_body(
        "Immutable objects are thread-safe, cannot be corrupted, and make perfect Map keys and Set elements. Joshua Bloch specifies 5 rules for immutability:"
    )
    engine.add_bullet("1. No Mutators:", "Do not provide any methods that modify the object's state (no setters).")
    engine.add_bullet("2. Prevent Subclassing:", "Ensure the class cannot be extended (mark class `final` or use private constructors).")
    engine.add_bullet("3. Make All Fields final:", "Enforces single assignment and ensures thread-safe publication.")
    engine.add_bullet("4. Make All Fields private:", "Prevents direct client access.")
    engine.add_bullet("5. Defensive Copying:", "Ensure exclusive access to any mutable components.")

    engine.add_body(
        "In Java 14+ (standardized in Java 16), the `record` keyword provides first-class language support for immutable data carriers with concise syntax:"
    )

    code_record = """// Java 16+ Record: Automatically generates final fields, constructor, 
// getters (x() and y()), equals(), hashCode(), and toString()!
public record Point(int x, int y) {
    // Compact Constructor for Invariant Validation
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be non-negative");
        }
    }
}

// Usage:
Point p1 = new Point(10, 20);
System.out.println(p1.x()); // 10 (Accessors do not use 'get' prefix)
System.out.println(p1);     // Point[x=10, y=20]"""
    engine.add_code("Modern Java 16+ Immutable Records", "java", code_record)

    engine.add_callout(
        "The 'Tell, Don't Ask' Principle",
        [
            "Instead of querying an object about its internal state, making a decision outside, and then mutating the object, tell the object directly what operation to perform.",
            "Violating Example: `if (cart.getItems().size() > 10) cart.setDiscount(0.1);`",
            "Refactored Clean Code: `cart.applyBulkDiscount();` (Encapsulates business rules inside Cart)."
        ],
        box_type="success"
    )
