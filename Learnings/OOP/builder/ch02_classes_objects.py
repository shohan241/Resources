from docx.shared import Inches

def build_ch02(engine):
    engine.add_chapter(
        2, 
        "Classes, Objects & The Java Type System",
        "Deep exploration of class structure, execution ordering of initializers, 'this' keyword mechanics, HotSpot JVM in-memory object layout, and the sacred equals() / hashCode() contract."
    )

    engine.add_h2("2.1 Class Blueprint vs. Heap Object Instance")
    engine.add_body(
        "In Java, a Class is a compile-time schema loaded into the Metaspace. An Object is a dynamically allocated chunk of contiguous memory on the JVM Heap created via the `new` keyword or reflection. Every class in Java implicitly or explicitly extends `java.lang.Object`, the ultimate root of the Java class hierarchy."
    )

    engine.add_h2("2.2 Anatomy of a Class: Fields, Methods & Initializer Blocks")
    engine.add_body(
        "A Java class comprises four structural elements: (1) Fields, (2) Methods, (3) Constructors, and (4) Initializer Blocks. The exact execution order during class loading and instantiation is a classic interview question:"
    )

    engine.add_bullet("1. Static Initializers (`static {}`):", "Execute exactly ONCE when the class is first loaded into memory by the ClassLoader. Runs top-to-bottom.")
    engine.add_bullet("2. Instance Initializers (`{}`):", "Execute EVERY time a new instance is created, running immediately BEFORE the constructor body.")
    engine.add_bullet("3. Constructor (`ClassName(...)`):", "Executes after instance variable assignments and instance initializer blocks have finished.")

    code_init_order = """public class InitializationOrderDemo {
    // 1. Static field & static block (Executed once on class load)
    static int staticCounter = initStatic();
    static { System.out.println("2. Static Block Executed"); }

    // 2. Instance field & instance block (Executed on every 'new')
    int instanceVal = initInstance();
    { System.out.println("4. Instance Initializer Block Executed"); }

    // 3. Constructor
    public InitializationOrderDemo() {
        System.out.println("5. Constructor Body Executed");
    }

    private static int initStatic() {
        System.out.println("1. Static Field Initialized");
        return 100;
    }

    private int initInstance() {
        System.out.println("3. Instance Field Initialized");
        return 200;
    }

    public static void main(String[] args) {
        System.out.println("--- Instantiating Object 1 ---");
        new InitializationOrderDemo();
        System.out.println("--- Instantiating Object 2 ---");
        new InitializationOrderDemo();
    }
}"""
    engine.add_code("Exact Initialization Order in Java", "java", code_init_order)

    engine.add_h2("2.3 The Four Powers of the 'this' Keyword")
    engine.add_body(
        "The `this` keyword is an implicit reference variable that points to the current object instance whose method or constructor is being invoked. It serves four distinct architectural functions:"
    )
    engine.add_bullet("1. Variable Shadowing Resolution:", "Disambiguates between instance fields and local parameters of the same name: `this.name = name;`.")
    engine.add_bullet("2. Explicit Constructor Chaining:", "Invoking an overloaded constructor from within another constructor: `this(arg1, arg2);`. Must be the very FIRST statement in the constructor!")
    engine.add_bullet("3. Passing Current Instance as Parameter:", "Passing the active object to an external service or event listener: `eventPublisher.register(this);`.")
    engine.add_bullet("4. Fluent Method Chaining (Method Chaining / Builder):", "Returning `this` at the end of mutating methods to enable fluent API chaining: `builder.setA().setB();`.")

    engine.add_h2("2.4 In-Memory Layout of a Java Object (HotSpot JVM)")
    engine.add_body(
        "What does an object actually look like in physical RAM? On a 64-bit HotSpot JVM, every object consists of three distinct segments:"
    )

    headers_layout = ["Component", "Byte Size (64-bit with Compressed OOPs)", "Internal Contents"]
    rows_layout = [
        ["Mark Word (Header)", "8 Bytes (64 bits)", "Identity HashCode, GC Age bits (4 bits for 15 promotions), Lock state flags, Biased Locking info"],
        ["Klass Pointer (Header)", "4 Bytes (Compressed OOPs) or 8 Bytes", "Pointer to class metadata residing in Metaspace (identifies runtime type)"],
        ["Array Length (Header)", "4 Bytes (Arrays ONLY)", "Integer denoting the number of elements in the array"],
        ["Instance Data", "Variable (aligned to 4/8 bytes)", "Actual primitive values and 4-byte reference pointers to other heap objects"],
        ["Padding", "0 to 7 Bytes", "Zero-filled bytes added to pad the total object size to a multiple of 8 bytes (64-bit alignment)"]
    ]
    engine.add_table(headers_layout, rows_layout, [Inches(1.8), Inches(2.2), Inches(3.0)])

    engine.add_h2("2.5 Object Identity (==) vs. Logical Equality (.equals())")
    engine.add_body(
        "By default, the `.equals()` method inherited from `java.lang.Object` simply executes `this == obj` (memory address identity). If you want two distinct objects with identical fields to be considered equal, you MUST override `.equals()`."
    )

    engine.add_h2("2.6 The Sacred equals() and hashCode() Contract")
    engine.add_body(
        "Violating the contract between `equals()` and `hashCode()` is one of the most common causes of silent, catastrophic bugs in production Java applications. The Java Language Specification mandates:"
    )
    engine.add_bullet("Rule 1 (Consistency):", "If `o1.equals(o2)` is `true`, then `o1.hashCode()` MUST EQUAL `o2.hashCode()`.")
    engine.add_bullet("Rule 2 (Collisions):", "If `o1.hashCode() == o2.hashCode()`, `o1.equals(o2)` is NOT necessarily true (hash collision).")
    engine.add_bullet("Consequence of Violation:", "If you override `equals()` without overriding `hashCode()`, hash-based collections (`HashMap`, `HashSet`, `Hashtable`) will store equal objects in completely different hash buckets, making it impossible to retrieve them via `.get()`!")

    code_hash_contract = """import java.util.Objects;
import java.util.HashMap;
import java.util.Map;

public class Employee {
    private final int id;
    private final String department;

    public Employee(int id, String dept) {
        this.id = id;
        this.department = dept;
    }

    // 1. Standard Robust equals() Implementation
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                         // Step 1: Identity check
        if (o == null || getClass() != o.getClass()) return false; // Step 2: Exact type check
        Employee employee = (Employee) o;                   // Step 3: Safe cast
        return id == employee.id && Objects.equals(department, employee.department);
    }

    // 2. Mandatory Corresponding hashCode()
    @Override
    public int hashCode() {
        return Objects.hash(id, department); // Combines field hashes
    }

    public static void main(String[] args) {
        Map<Employee, String> employeeMap = new HashMap<>();
        Employee e1 = new Employee(101, "Engineering");
        employeeMap.put(e1, "Tech Lead");

        // Lookup with an equal, distinct object instance:
        Employee lookupKey = new Employee(101, "Engineering");
        System.out.println("Role: " + employeeMap.get(lookupKey)); 
        // Output: "Tech Lead" (Works because both equals() and hashCode() are overridden!)
    }
}"""
    engine.add_code("Robust equals() and hashCode() Contract Implementation", "java", code_hash_contract)

    engine.add_callout(
        "Why Cloneable is Flawed (Joshua Bloch's Recommendation)",
        [
            "The `Cloneable` interface in Java is widely recognized as a broken design: it has no methods, and `Object.clone()` is protected and bypasses constructors, performing shallow bitwise copies.",
            "Best Practice: Avoid `Cloneable`. Instead, implement a Copy Constructor (`public Employee(Employee other)`) or a static factory method (`Employee.copy(other)`). This provides type-safe, explicit deep copying without reflection."
        ],
        box_type="warning"
    )
