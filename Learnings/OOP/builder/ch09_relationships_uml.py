from docx.shared import Inches

def build_ch09(engine):
    engine.add_chapter(
        9, 
        "Object Relationships & UML Models in Java",
        "Mastering software coupling taxonomy in Java: Dependency, Association, Aggregation, and Composition, alongside precise UML notation and memory ownership rules."
    )

    engine.add_h2("9.1 The Spectrum of Object Coupling in Java")
    engine.add_body(
        "Modern Java systems design requires precise categorization of how classes interact. Coupling ranges from weak, transient interactions to strong, life-and-death ownership:"
    )

    headers_rel = ["Relationship", "Semantic Meaning", "Ownership Level", "Part Lifetime Dependency", "UML Representation"]
    rows_rel = [
        ["Dependency", "'Uses-A' (Transient)", "None", "Transient; passed as method parameter or local variable", "Dashed line with arrow: `- - - >`"],
        ["Association", "'Knows-A' / 'Peer'", "Peer link", "Independent; both objects exist separately in the heap", "Solid line: `—————`"],
        ["Aggregation", "'Has-A' (Weak Whole-Part)", "Shared / Non-owning", "Independent; Part survives if Whole is garbage collected", "Hollow diamond at Whole: `◇————`"],
        ["Composition", "'Has-A' (Strong Whole-Part)", "Exclusive / Owning", "Bound; Part is created inside Whole and collected with it", "Filled solid diamond at Whole: `◆————`"],
        ["Generalization", "'Is-A' (Inheritance)", "Taxonomic", "Subclass `extends` Superclass", "Solid line with hollow triangle: `———▷`"],
        ["Realization", "'Implements' (Contract)", "Contractual", "Class `implements` Interface", "Dashed line with hollow triangle: `- - ▷`"]
    ]
    engine.add_table(headers_rel, rows_rel, [Inches(1.2), Inches(1.4), Inches(1.1), Inches(2.0), Inches(1.3)])

    engine.add_h2("9.2 Java Code Dissection: Aggregation vs. Composition")
    engine.add_body(
        "A critical interview question: How do you implement Aggregation versus Composition in Java, where all objects live on the heap and there are no C++ value members?"
    )
    engine.add_body(
        "In Java, the distinction is enforced through LIFETIME RESPONSIBILITY and CONSTRUCTOR INJECTION:"
    )

    code_relationships = """import java.util.List;
import java.util.ArrayList;

// 1. DEPENDENCY ("Uses-A"): Service is passed temporarily to execute()
class EmailService {
    public void sendEmail(String to, String msg) { System.out.println("Email sent to " + to); }
}

class UserRegistration {
    public void register(String email, EmailService emailer) { // Transient dependency!
        emailer.sendEmail(email, "Welcome to the Platform!");
    }
}

// 2. AGGREGATION ("Has-A" Weak): Department aggregates Professors
// If the Department is garbage collected, the Professors STILL exist!
class Professor {
    private final String name;
    public Professor(String name) { this.name = name; }
}

class Department {
    private final String deptName;
    private final List<Professor> faculty; // Aggregated reference list

    // Injected from the outside (Aggregation)
    public Department(String name, List<Professor> faculty) {
        this.deptName = name;
        this.faculty = new ArrayList<>(faculty);
    }
}

// 3. COMPOSITION ("Has-A" Strong): Order is composed of OrderItems
// If the Order is deleted, its OrderItems have NO architectural meaning and are destroyed!
class OrderItem {
    private final String sku;
    private final int quantity;
    public OrderItem(String sku, int qty) { this.sku = sku; this.quantity = qty; }
}

class Order {
    private final String orderId;
    private final List<OrderItem> items; // Composition: Owned exclusively!

    public Order(String orderId) {
        this.orderId = orderId;
        this.items = new ArrayList<>(); // Items created and managed strictly inside Order
    }

    public void addItem(String sku, int qty) {
        this.items.add(new OrderItem(sku, qty)); // Exclusive lifecycle ownership
    }
}"""
    engine.add_code("Java Implementation of Dependency, Aggregation, and Composition", "java", code_relationships)

    engine.add_callout(
        "How to Decide: Aggregation vs. Composition in Java",
        [
            "Ask yourself: 'Can the child object exist without the parent object?'",
            "1. If YES -> Use AGGREGATION (Inject the dependency into the parent class from the outside).",
            "2. If NO -> Use COMPOSITION (Instantiate and manage the child object exclusively within the parent, and ensure cascading deletion)."
        ],
        box_type="info"
    )
