"""
Test script to debug resume parser
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.document_parser import DocumentParser

# Test with sample resume text
sample_resume = """
John Doe
Software Engineer | Developer

john.doe@email.com | +1-555-123-4567 | LinkedIn: linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years of experience in Python and Java.

SKILLS
Python, Java, JavaScript, React, Node.js, SQL, Git

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-Present
• Developed web applications using React and Node.js
• Led a team of 5 developers

EDUCATION
Bachelor of Science in Computer Science | University Name | 2018
"""

print("=" * 60)
print("Testing Document Parser Section Extraction")
print("=" * 60)

sections = DocumentParser.extract_sections(sample_resume)

print("\nExtracted Sections:")
print("-" * 40)
for section, content in sections.items():
    if content:
        print(f"\n{section.upper()}:")
        print(content[:100] + ("..." if len(content) > 100 else ""))
    else:
        print(f"\n{section.upper()}: [EMPTY]")

print("\n" + "=" * 60)
print("Testing Name Extraction")
print("=" * 60)
name = DocumentParser.extract_name(sample_resume)
print(f"Extracted Name: {name}")

print("\n" + "=" * 60)
print("Testing Format Detection")
print("=" * 60)
analysis = DocumentParser.detect_format(sample_resume)
print(f"Has sections: {analysis['has_sections']}")
print(f"Section count: {analysis['section_count']}")
print(f"Word count: {analysis['word_count']}")
print(f"Suggestions: {analysis['suggestions']}")
