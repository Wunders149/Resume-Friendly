#!/usr/bin/env python3
"""
Quick test to verify UI loads without errors.
"""

import sys
from pathlib import Path

# Add cv-forge directory to path
sys.path.insert(0, str(Path(__file__).parent / "cv-forge"))

try:
    from models.resume import Resume, Education, Certification, Experience
    from exporters.pdf_exporter import PDFExporter
    from exporters.docx_exporter import DOCXExporter
    from ui.main_window import MainWindow
    from ui.forms import PersonalInfoFrame, EducationFrame, CertificationFrame, ExperienceFrame, SkillsFrame
    
    print("✓ All modules imported successfully")
    print("✓ UI improvements are syntactically correct")
    print("✓ Ready to run: python cv-forge/main.py")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
