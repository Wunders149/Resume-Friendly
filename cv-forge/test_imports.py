import sys
sys.path.insert(0, 'src')

try:
    from utils.document_parser import DocumentParser
    from utils.resume_generator import ResumeGenerator
    from ui.main_window import CVForgeApp
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
