# CV Forge - Development Guide

## Project Architecture

### Directory Structure
```
cv-forge/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # User documentation
├── SETUP.md                  # Setup instructions
├── FEATURES.md               # Feature documentation
├── run.bat                   # Windows quick start script
├── run.sh                    # macOS/Linux quick start script
├── .gitignore               # Git ignore rules
│
├── src/                      # Source code directory
│   ├── __init__.py
│   │
│   ├── ui/                   # User interface module
│   │   ├── __init__.py
│   │   └── main_window.py    # Main GUI window with tabs
│   │
│   ├── utils/                # Utility modules
│   │   ├── __init__.py
│   │   ├── document_parser.py    # PDF/Word parsing
│   │   ├── resume_generator.py   # PDF/Word generation
│   │
│   └── templates/            # Resume templates (for future use)
│
└── output/                   # Generated resumes directory
```

### Module Dependencies

```
app.py
  └─> ui/main_window.py
      ├─> utils/document_parser.py
      └─> utils/resume_generator.py
```

---

## Module Documentation

### 1. document_parser.py
**Purpose**: Parse PDF and Word documents to extract resume information

**Key Classes**:
- `DocumentParser`: Main parser class with static methods

**Key Methods**:
```python
DocumentParser.parse_pdf(pdf_path: str) -> str
    # Extract text from PDF file
    
DocumentParser.parse_docx(docx_path: str) -> str
    # Extract text from Word document
    
DocumentParser.parse_document(file_path: str) -> str
    # Auto-detect and parse document
    
DocumentParser.extract_sections(text: str) -> Dict[str, str]
    # Extract organized resume sections
```

**Dependencies**:
- `pdfplumber`: PDF text extraction
- `docx` (python-docx): Word document handling

**Recognition Keywords**:
- Contact: "contact", "email", "phone"
- Summary: "summary", "objective", "profile"
- Skills: "skills", "competencies"
- Experience: "experience", "work", "employment"
- Education: "education", "degree", "university"
- Certifications: "certifications", "licenses"
- Projects: "projects", "portfolio"

---

### 2. resume_generator.py
**Purpose**: Generate professional resumes in PDF and Word formats

**Key Classes**:
- `ResumeGenerator`: Main generator class

**Key Methods**:
```python
ResumeGenerator.__init__(output_dir: str = "output")
    # Initialize generator with output directory
    
ResumeGenerator.generate_pdf(resume_data: Dict, filename: Optional[str]) -> str
    # Generate PDF resume
    
ResumeGenerator.generate_docx(resume_data: Dict, filename: Optional[str]) -> str
    # Generate Word document resume
```

**Resume Data Structure**:
```python
{
    'name': str,
    'contact': str,
    'summary': str,
    'skills': str,
    'experience': str,
    'education': str,
    'certifications': str,
    'projects': str
}
```

**Dependencies**:
- `reportlab`: PDF generation
- `docx` (python-docx): Word document creation
- `datetime`: Timestamp for filenames

**Styling**:
- Primary Color: #1f4788 (Navy Blue)
- Font: Default system fonts
- Layout: 0.5-inch margins
- Page Size: Letter (8.5" x 11")

---

### 3. main_window.py
**Purpose**: Provide user interface for CV Forge

**Key Classes**:
- `CVForgeApp`: Main application window

**Tabs**:
1. **Basic Info**: Name, contact information
2. **Summary & Skills**: Professional summary, skills list
3. **Experience**: Work history and responsibilities
4. **Education**: Degrees, certifications, licenses
5. **Projects**: Portfolio and project details

**UI Components**:
- Header with title and subtitle
- Ttk.Notebook for tabbed interface
- Text widgets for content editing
- Buttons for file upload and export
- Labels for feedback and guidance

**Dependencies**:
- `tkinter`: GUI framework (built-in)
- `tkinter.ttk`: Themed widgets
- `tkinter.filedialog`: File selection dialogs
- `tkinter.messagebox`: Alerts and confirmations

---

## Development Workflow

### Adding New Features

#### Example: Adding a New Section (e.g., Languages)

1. **Update Resume Data Structure** (main_window.py):
   ```python
   self.resume_data = {
       ...
       'languages': '',  # Add new field
       ...
   }
   ```

2. **Add New Tab** (main_window.py):
   ```python
   languages_tab = tk.Frame(self.notebook, bg='#ffffff')
   self.notebook.add(languages_tab, text="Languages")
   self.create_languages_tab(languages_tab)
   
   def create_languages_tab(self, parent):
       frame = tk.Frame(parent, bg='#ffffff')
       frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
       tk.Label(frame, text="Languages:", bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W, pady=5)
       self.languages_text = tk.Text(frame, font=('Arial', 9), height=10, width=60)
       self.languages_text.pack(fill=tk.BOTH, expand=True, pady=5)
       self.languages_text.bind('<KeyRelease>', lambda e: self.update_data('languages', self.languages_text.get('1.0', tk.END)))
   ```

3. **Update Resume Generator** (resume_generator.py):
   ```python
   # In generate_pdf():
   if resume_data.get('languages'):
       content.append(Paragraph("LANGUAGES", section_style))
       languages = Paragraph(resume_data['languages'], styles['Normal'])
       content.append(languages)
   ```

4. **Update Parser** (document_parser.py):
   ```python
   # In extract_sections():
   elif any(keyword in line_lower for keyword in ['languages', 'language']):
       current_section = 'languages'
   
   # Add to sections dict:
   'languages': ''
   ```

---

### Code Style Guidelines

- **Naming**: Use snake_case for functions/variables, PascalCase for classes
- **Documentation**: Use docstrings for all functions and classes
- **Comments**: Explain "why", not "what" (code shows what)
- **Line Length**: Keep under 100 characters when possible
- **Imports**: Group by standard library, third-party, local

### Example Function:
```python
def parse_document(file_path: str) -> str:
    """
    Parse document based on file extension.
    
    Args:
        file_path: Path to document file (pdf or docx)
        
    Returns:
        Extracted text from document
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format not supported
    """
    # Implementation here
```

---

## Performance Optimization Tips

### Document Parsing
- Cache parsed results to avoid re-parsing
- Use streaming for large PDFs
- Profile extraction speed with timing

### Resume Generation
- Reuse style objects instead of recreating
- Batch multiple exports together
- Consider async processing for large batches

### UI Responsiveness
- Move long-running operations to background threads
- Show progress indicators
- Use loading dialogs for file operations

---

## Testing

### Unit Tests (Future Implementation)

```python
# test_document_parser.py
import unittest
from src.utils.document_parser import DocumentParser

class TestDocumentParser(unittest.TestCase):
    def test_parse_pdf(self):
        text = DocumentParser.parse_pdf("test.pdf")
        assert len(text) > 0
    
    def test_extract_sections(self):
        sections = DocumentParser.extract_sections("EXPERIENCE\n...")
        assert 'experience' in sections
```

### Manual Testing Checklist
- [ ] Upload PDF resume
- [ ] Upload Word resume (.docx)
- [ ] Edit each tab
- [ ] Generate PDF output
- [ ] Generate Word output
- [ ] Verify file locations
- [ ] Check formatting in both formats
- [ ] Test with different document sizes

---

## Debugging Tips

### Enable Debug Output
```python
# In any module
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message here")
```

### Common Issues & Solutions

1. **Import Errors**: Check `sys.path` includes src/
2. **File Not Found**: Verify absolute paths
3. **Parsing Issues**: Print raw text to debug
4. **GUI Not Showing**: Check tkinter installation
5. **PDF Corruption**: Try with different PDF file

---

## Future Enhancement Ideas

### Short Term
- [ ] Add multiple resume templates
- [ ] Custom color schemes
- [ ] Resume preview before export
- [ ] Undo/Redo functionality
- [ ] Auto-save drafts

### Medium Term
- [ ] ATS optimization scores
- [ ] Resume analytics
- [ ] Cloud storage integration
- [ ] Share via email
- [ ] Version history

### Long Term
- [ ] Web version
- [ ] Mobile app
- [ ] AI-powered suggestions
- [ ] Job market insights
- [ ] Custom template builder

---

## Dependencies Overview

| Package | Version | Purpose |
|---------|---------|---------|
| python-docx | ≥1.0.0 | Read/write Word docs |
| PyPDF2 | ≥3.0.1 | Handle PDF files |
| pdfplumber | ≥0.10.0 | Extract PDF text |
| reportlab | ≥4.0.9 | Generate PDFs |
| Pillow | ≥10.1.0 | Image processing |

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## Version History

### v1.0.0 (Feb 23, 2026) - Initial Release
- Document parsing (PDF, Word)
- Multi-tab editing interface
- Resume generation (PDF, Word)
- Professional styling
- File management

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## License

This project is open source and available under the MIT License.

---

**Last Updated**: February 23, 2026

