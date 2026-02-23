# CV Forge - Testing Guide

## Manual Testing

### Before First Run
1. ✅ Python 3.7+ installed
2. ✅ Dependencies installed via `pip install -r requirements.txt`
3. ✅ All source files in place
4. ✅ `output/` directory exists

### Test Case 1: Application Startup
**Steps**:
1. Run `python app.py`
2. Observe GUI window opens
3. Check all tabs visible

**Expected Results**:
- ✅ Window titled "CV Forge - Resume Builder"
- ✅ Header displays correctly
- ✅ 5 tabs visible: Basic Info, Summary & Skills, Experience, Education, Projects
- ✅ Generate buttons visible
- ✅ File upload button accessible

---

### Test Case 2: PDF Upload and Parsing
**Prerequisites**: Sample PDF resume file

**Steps**:
1. Click "Choose PDF or Word Document"
2. Select a PDF resume
3. Wait for parsing to complete

**Expected Results**:
- ✅ File selected shows in status
- ✅ Success message appears
- ✅ Content populated in appropriate tabs
- ✅ No error messages

---

### Test Case 3: Word Document Upload
**Prerequisites**: Sample .docx resume file

**Steps**:
1. Click "Choose PDF or Word Document"
2. Select a .docx file
3. Wait for parsing

**Expected Results**:
- ✅ File parsed successfully
- ✅ Content extracted into tabs
- ✅ Formatting preserved
- ✅ All sections identified

---

### Test Case 4: Manual Editing
**Steps**:
1. Click on "Basic Info" tab
2. Enter name: "John Doe"
3. Enter contact info: "john@example.com | 555-1234 | New York, NY"
4. Switch to "Summary & Skills" tab
5. Enter summary text
6. Enter skills

**Expected Results**:
- ✅ Text appears in fields as you type
- ✅ Tab switching works smoothly
- ✅ All text is preserved
- ✅ No data loss between tabs

---

### Test Case 5: PDF Resume Generation
**Prerequisite**: At least "Name" entered

**Steps**:
1. Fill out at least name field
2. Click "Generate PDF Resume"
3. Check `output/` folder

**Expected Results**:
- ✅ Success dialog appears
- ✅ File path shown in dialog
- ✅ PDF file exists in output folder
- ✅ PDF opens and displays content
- ✅ Formatting looks professional

---

### Test Case 6: Word Resume Generation
**Prerequisite**: At least "Name" entered

**Steps**:
1. Click "Generate Word Resume"
2. Check `output/` folder

**Expected Results**:
- ✅ Success dialog appears
- ✅ .docx file created
- ✅ File opens in Word/LibreOffice
- ✅ Content editable
- ✅ Formatting preserved

---

### Test Case 7: Multiple Exports
**Steps**:
1. Generate PDF resume (name: "Test Resume")
2. Modify content
3. Generate Word resume
4. Modify content again
5. Generate PDF again

**Expected Results**:
- ✅ Each file has unique timestamp
- ✅ Files not overwritten
- ✅ All versions saved separately
- ✅ Filenames follow naming convention

---

### Test Case 8: Error Handling - Missing Name
**Steps**:
1. Clear name field
2. Click "Generate PDF Resume"

**Expected Results**:
- ✅ Warning dialog appears
- ✅ Message: "Please enter your name"
- ✅ No file generated
- ✅ Application stays responsive

---

### Test Case 9: Error Handling - Invalid File
**Steps**:
1. Click "Choose PDF or Word Document"
2. Try to select a .txt file (or .jpg)

**Expected Results**:
- ✅ File dialog only shows valid formats
- ✅ Invalid files not selectable
- Or: Error message if invalid format selected

---

### Test Case 10: Large Document Parsing
**Prerequisites**: Large PDF (>5MB if available)

**Steps**:
1. Select large PDF
2. Wait for parsing
3. Observe processing time

**Expected Results**:
- ✅ Parsing completes in reasonable time
- ✅ No application freeze
- ✅ All content extracted
- ✅ Application responsive

---

## Automated Testing (Python)

### Module Import Test
```python
import sys
sys.path.insert(0, 'src')
from utils.document_parser import DocumentParser
from utils.resume_generator import ResumeGenerator
from ui.main_window import CVForgeApp
print("✓ All modules imported successfully")
```

### Basic Functionality Test
```python
import sys
sys.path.insert(0, 'src')
from utils.resume_generator import ResumeGenerator

# Test PDF generation
test_data = {
    'name': 'Test User',
    'contact': 'test@example.com | 555-0000',
    'summary': 'Test summary text',
    'skills': 'Python, JavaScript, HTML',
    'experience': 'Senior Developer at TechCorp',
    'education': 'BS Computer Science',
    'certifications': 'AWS Certified',
    'projects': 'Built CV Forge application'
}

gen = ResumeGenerator()
pdf_path = gen.generate_pdf(test_data, 'test_resume')
docx_path = gen.generate_docx(test_data, 'test_resume')

print(f"✓ PDF generated: {pdf_path}")
print(f"✓ DOCX generated: {docx_path}")
```

---

## Performance Testing

### Parsing Speed Test
```bash
# Small PDF (< 1 MB)
Expected time: < 1 second

# Medium PDF (1-5 MB)
Expected time: 1-3 seconds

# Large PDF (5-50 MB)
Expected time: 5-15 seconds
```

### Generation Speed Test
```bash
# PDF generation
Expected time: < 2 seconds

# Word generation
Expected time: < 2 seconds
```

---

## Browser/Compatibility Testing

### Windows
- [ ] Windows 10: Works
- [ ] Windows 11: Works
- [ ] Python 3.7-3.14: Compatible

### macOS
- [ ] macOS 10.x+: Works
- [ ] Python 3.7+: Compatible

### Linux
- [ ] Ubuntu 18.04+: Works
- [ ] Python 3.7+: Compatible

---

## File Format Testing

### PDF Input
- [ ] Standard PDF (text-based)
- [ ] Scanned PDF (image-based) - May not parse well
- [ ] Password-protected PDF - Will show error
- [ ] Large PDF (>50 MB) - May be slow

### Word Input (.docx)
- [ ] Modern Word (.docx): ✅ Works
- [ ] Legacy Word (.doc): ✅ Works
- [ ] Large document (>25 MB): May be slow
- [ ] Complex formatting: May lose some styling

---

## Output Validation

### PDF Output
- [ ] File created in output/ folder
- [ ] PDF opens in standard readers
- [ ] Text selectable and copyable
- [ ] Formatting preserved
- [ ] Colors display correctly
- [ ] Page breaks appropriate

### Word Output
- [ ] File created in output/ folder
- [ ] Opens in Microsoft Word
- [ ] Opens in LibreOffice Writer
- [ ] Text is editable
- [ ] Formatting can be modified
- [ ] Maintains structure

---

## Stress Testing

### Multiple Generations
```bash
# Generate 10 resumes consecutively
# Expected: All create successfully
# Check: Unique filenames, no overwrites
```

### Large Content
```bash
# Add very long text to each section
# Expected: Handles gracefully
# Check: No truncation, proper pagination
```

### Rapid Tab Switching
```bash
# Switch between tabs quickly
# Expected: No data loss, responsive UI
# Check: All content preserved
```

---

## Regression Testing Checklist

After any code changes, test:
- [ ] App starts without errors
- [ ] PDF parsing still works
- [ ] Word parsing still works
- [ ] PDF generation still works
- [ ] Word generation still works
- [ ] Tab navigation works
- [ ] Text editing works
- [ ] File dialogs work

---

## Known Limitations & Testing Notes

1. **Scanned PDFs**: Text extraction may fail for image-based PDFs
2. **Complex Formatting**: Some formatting may not transfer between formats
3. **Very Large Documents**: Processing may be slow (>50 MB)
4. **Password-Protected Files**: Cannot be opened by the parser

---

## Reporting Bugs

When reporting issues, include:
1. **Environment**: OS, Python version
2. **Steps to Reproduce**: Exact steps taken
3. **Expected Result**: What should happen
4. **Actual Result**: What happened instead
5. **Error Message**: Full error text if applicable
6. **Screenshot**: Visual of issue if applicable

---

## Test Coverage Goals

- [ ] UI Components: 100% manual testing
- [ ] Document Parsing: 95% test coverage
- [ ] Resume Generation: 95% test coverage
- [ ] Error Handling: 90% coverage
- [ ] Edge Cases: 80% coverage

---

## Continuous Testing

### Before Each Release
1. Run all manual test cases
2. Test on multiple OS versions
3. Test with various document sizes
4. Verify performance metrics
5. Check error handling
6. Validate output quality

---

**Last Updated**: February 23, 2026  
**Test Coverage**: Comprehensive manual testing framework

