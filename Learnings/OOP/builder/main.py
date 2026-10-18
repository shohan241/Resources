import os
import sys
import subprocess

from builder.doc_engine import DocEngine
from builder.ch01_foundations import build_ch01
from builder.ch02_classes_objects import build_ch02
from builder.ch03_lifecycle_memory import build_ch03
from builder.ch04_encapsulation import build_ch04
from builder.ch05_abstraction import build_ch05
from builder.ch06_inheritance import build_ch06
from builder.ch07_polymorphism_vtable import build_ch07
from builder.ch08_static_smartptr import build_ch08
from builder.ch09_relationships_uml import build_ch09
from builder.ch10_solid_principles import build_ch10
from builder.ch11_design_patterns import build_ch11
from builder.ch12_lld_parking_lot import build_ch12
from builder.ch13_interview_mastery import build_ch13

def main():
    base_dir = "/home/shohan241/Documents/Learnings/OOP"
    docx_path = os.path.join(base_dir, "Java_OOP_Complete_Mastery_Guide.docx")
    pdf_path = os.path.join(base_dir, "Java_OOP_Complete_Mastery_Guide.pdf")
    md_path = os.path.join(base_dir, "Java_OOP_Complete_Mastery_Guide.md")

    print(">>> Initializing Java OOP DocEngine...")
    engine = DocEngine(docx_path, md_path)

    print(">>> Adding Document Title & Executive Overview...")
    engine.add_title(
        "Java Object-Oriented Programming & Low-Level Design (LLD)",
        "The Comprehensive Industry Mastery Guide (Java Edition): From JVM Architecture, Memory Layout, and Bytecode Dispatch to SOLID, GoF Design Patterns, and Enterprise Machine Coding"
    )

    print(">>> Building Chapter 1: Paradigm Shift & Java Memory Architecture...")
    build_ch01(engine)

    print(">>> Building Chapter 2: Classes, Objects & The Java Type System...")
    build_ch02(engine)

    print(">>> Building Chapter 3: Object Lifecycle, Garbage Collection & Resource Management...")
    build_ch03(engine)

    print(">>> Building Chapter 4: Encapsulation, Defensive Copying & Immutability...")
    build_ch04(engine)

    print(">>> Building Chapter 5: Abstraction & Modern Java Interfaces...")
    build_ch05(engine)

    print(">>> Building Chapter 6: Inheritance & Class Hierarchies in Java...")
    build_ch06(engine)

    print(">>> Building Chapter 7: Polymorphism & JVM Dynamic Dispatch Internals...")
    build_ch07(engine)

    print(">>> Building Chapter 8: Static Members, Advanced Enums & Nested Classes...")
    build_ch08(engine)

    print(">>> Building Chapter 9: Object Relationships & UML Models in Java...")
    build_ch09(engine)

    print(">>> Building Chapter 10: The SOLID Design Principles (Java Edition)...")
    build_ch10(engine)

    print(">>> Building Chapter 11: Essential Gang of Four (GoF) Design Patterns in Java...")
    build_ch11(engine)

    print(">>> Building Chapter 12: Production Low-Level Design (LLD): Parking Lot System in Java...")
    build_ch12(engine)

    print(">>> Building Chapter 13: Top 35+ Java OOP Technical Interview Questions & Model Answers...")
    build_ch13(engine)

    print(">>> Saving DOCX and Markdown documents...")
    engine.save()

    print(">>> Converting DOCX to PDF using LibreOffice headless...")
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        docx_path,
        "--outdir",
        base_dir
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f">>> PDF successfully generated: {pdf_path}")
    else:
        print(f">>> PDF generation error: {res.stderr}")

    print(">>> Build Complete! All Java OOP documents generated successfully.")

if __name__ == "__main__":
    main()
