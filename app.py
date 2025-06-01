from utils.parser import extract_text_from_file, extract_basic_info
from utils.section_extractor import extract_sections
import os

def main():
    
    resume_path = "/Users/mayankshukla/Downloads/Resume Analyzer/resumes/C173_CV.pdf"  # Relative path is cleaner

    # Step 1: Extract raw text from file
    text = extract_text_from_file(resume_path)
    print("📄 Raw Extracted Text:")
    print(text[:1000])  # Preview first 1000 chars

    # Step 2: Extract basic info
    basic_info = extract_basic_info(text)
    print("\nBasic Info:")
    for key, value in basic_info.items():
        print(f"{key.capitalize()}: {value}")

    # Step 3: Extract structured sections
    sections = extract_sections(text)
    print("\n📑 Extracted Sections:")
    for section, content in sections.items():
        print(f"\n🔹 {section.upper()}:")
        print(content[:300])  # Preview part of each section

if __name__ == "__main__":
    main()
