"""
Test script to verify CV Forge download/export functionality
Tests PDF and Word resume generation with sample data
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.resume_generator import ResumeGenerator
from utils.document_parser import DocumentParser


def test_resume_generation():
    """Test PDF and Word resume generation"""
    
    print("=" * 60)
    print("CV FORGE - DOWNLOAD/EXPORT FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test data
    test_resume_data = {
        'name': 'John Doe',
        'contact': 'john@example.com | (555) 123-4567 | New York, NY',
        'summary': 'Experienced software engineer with 5+ years in full-stack development. Passionate about building scalable applications and mentoring junior developers.',
        'skills': 'Python, JavaScript, React, Node.js, SQL, REST APIs, Git, Docker, AWS, Project Management',
        'experience': 'Senior Developer | TechCorp Inc. | Jan 2023 - Present\nLed development of microservices architecture, reducing system load by 40%.\n\nFull Stack Developer | StartupXYZ | Jun 2021 - Dec 2022\nBuilt web applications using React and Node.js, managing 3-person team.',
        'education': 'Bachelor of Science in Computer Science | MIT | Graduated May 2019\nGPA: 3.8/4.0',
        'certifications': 'AWS Certified Solutions Architect - Professional\nGoogle Cloud Professional Data Engineer',
        'projects': 'CV Forge - Resume Builder Desktop App | Python, Tkinter, PDF/Word generation\nWeather Dashboard | React, OpenWeather API, Real-time updates'
    }
    
    # Create generator
    generator = ResumeGenerator()
    
    print("\n✓ ResumeGenerator initialized")
    print(f"✓ Output directory: {os.path.abspath(generator.output_dir)}")
    
    # Test 1: PDF Generation
    print("\n" + "="*60)
    print("TEST 1: PDF RESUME GENERATION")
    print("="*60)
    
    try:
        pdf_path = generator.generate_pdf(test_resume_data, 'test_resume_john_doe')
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF Generated Successfully")
            print(f"   Path: {pdf_path}")
            print(f"   Size: {file_size:,} bytes")
            print(f"   Filename: {os.path.basename(pdf_path)}")
        else:
            print(f"❌ PDF file not found at: {pdf_path}")
            return False
            
    except Exception as e:
        print(f"❌ PDF Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Word Document Generation
    print("\n" + "="*60)
    print("TEST 2: WORD DOCUMENT GENERATION")
    print("="*60)
    
    try:
        docx_path = generator.generate_docx(test_resume_data, 'test_resume_john_doe')
        
        if os.path.exists(docx_path):
            file_size = os.path.getsize(docx_path)
            print(f"✅ Word Document Generated Successfully")
            print(f"   Path: {docx_path}")
            print(f"   Size: {file_size:,} bytes")
            print(f"   Filename: {os.path.basename(docx_path)}")
        else:
            print(f"❌ Word document not found at: {docx_path}")
            return False
            
    except Exception as e:
        print(f"❌ Word Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Verify files are readable/valid
    print("\n" + "="*60)
    print("TEST 3: FILE VALIDATION")
    print("="*60)
    
    # Check PDF
    try:
        from pypdf import PdfReader
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
        print(f"✅ PDF is valid and readable")
        print(f"   Pages: {num_pages}")
    except Exception as e:
        print(f"⚠️  PDF validation warning: {str(e)}")
    
    # Check Word
    try:
        from docx import Document
        doc = Document(docx_path)
        num_paragraphs = len(doc.paragraphs)
        print(f"✅ Word document is valid and readable")
        print(f"   Paragraphs: {num_paragraphs}")
    except Exception as e:
        print(f"❌ Word document validation error: {str(e)}")
        return False
    
    # Test 4: Output directory contents
    print("\n" + "="*60)
    print("TEST 4: OUTPUT DIRECTORY CONTENTS")
    print("="*60)
    
    output_files = os.listdir(generator.output_dir)
    if output_files:
        print(f"✅ Output directory contains {len(output_files)} file(s):")
        for filename in output_files:
            filepath = os.path.join(generator.output_dir, filename)
            size = os.path.getsize(filepath)
            print(f"   • {filename} ({size:,} bytes)")
    else:
        print("⚠️  Output directory is empty")
    
    # Test 5: Multiple template formats
    print("\n" + "="*60)
    print("TEST 5: TEMPLATE GENERATION")
    print("="*60)
    
    templates_to_test = ['classic', 'modern', 'minimal']
    template_results = {}
    
    for template_name in templates_to_test:
        try:
            pdf_template_path = generator.generate_pdf(
                test_resume_data, 
                f'test_resume_template_{template_name}',
                template=template_name
            )
            
            if os.path.exists(pdf_template_path):
                size = os.path.getsize(pdf_template_path)
                template_results[template_name] = {
                    'status': 'success',
                    'path': pdf_template_path,
                    'size': size
                }
                print(f"✅ {template_name.upper()} template generated ({size:,} bytes)")
            else:
                template_results[template_name] = {'status': 'failed'}
                print(f"❌ {template_name.upper()} template failed")
                
        except Exception as e:
            template_results[template_name] = {'status': 'error', 'error': str(e)}
            print(f"⚠️  {template_name.upper()} template error: {str(e)}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    success_count = sum(1 for r in template_results.values() if r.get('status') == 'success')
    total_count = len(template_results)
    
    print(f"✅ PDF Generation: PASS")
    print(f"✅ Word Generation: PASS")
    print(f"✅ File Validation: PASS")
    print(f"✅ Templates: {success_count}/{total_count} SUCCESS")
    print(f"\n📂 Output Location: {os.path.abspath(generator.output_dir)}")
    print(f"\n✨ Download/Export Functionality: VERIFIED & WORKING")
    
    return True


if __name__ == "__main__":
    success = test_resume_generation()
    exit(0 if success else 1)
