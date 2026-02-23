# CV Forge - Resume Builder

**CV Forge** is a modern desktop application built with Python that helps you create professional resumes. Upload your resume information in PDF or Word format, edit it in the user-friendly interface, and generate a polished resume in PDF or Word format with multiple template options.

## ✨ What's New in Version 2.0

- 🎨 **Modern UI** - Sleek, professional interface with improved layout
- 📊 **Progress Tracking** - Real-time completion percentage
- 💾 **Auto-Save** - Never lose your work with automatic draft saving
- 👁️ **Live Preview** - See your resume as you edit
- 🎯 **Multiple Templates** - Classic, Modern, and Minimal styles
- ⌨️ **Keyboard Shortcuts** - Work faster with productivity shortcuts
- ✅ **Smart Validation** - Get helpful suggestions as you write
- 🔍 **Enhanced Parsing** - Better section detection from uploaded documents

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to project
cd cv-forge

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Or use Quick Start Scripts
```bash
# Windows
run.bat

# macOS/Linux
bash run.sh
```

---

## 📋 Features

### Document Processing
- 📄 **Parse PDF & Word** - Upload existing resumes in PDF or DOCX format
- 🧠 **Smart Section Detection** - Automatically identifies and organizes resume sections
- ✏️ **Multi-Tab Editor** - Edit information in organized tabs
- 💾 **Auto-Save Drafts** - Work is automatically saved every 30 seconds

### Resume Sections
- **Basic Info** - Name, professional title, contact details
- **Summary & Skills** - Professional summary and key competencies
- **Experience** - Work history with formatted entries
- **Education** - Degrees and academic background
- **Additional** - Certifications, projects, languages, references

### Export Options
- 📄 **PDF Export** - Professional PDF with template styling
- 📝 **Word Export** - Editable DOCX format
- 🎨 **3 Templates** - Classic, Modern, and Minimal designs
- 📍 **Choose Location** - Save directly to your preferred folder

### Productivity Features
- ⌨️ **Keyboard Shortcuts**
  - `Ctrl+S` - Save draft
  - `Ctrl+O` - Open document
  - `Ctrl+E` - Export PDF
  - `Ctrl+W` - Export Word
  - `Ctrl+N` - New/Clear all
  - `F5` - Refresh preview

### Validation & Quality
- ✅ **Required Field Checks** - Ensures essential info is complete
- 💡 **Smart Suggestions** - Helpful tips for improvement
- 📊 **Progress Indicator** - Visual completion tracking
- 👁️ **Live Preview** - See your resume content as you edit

---

## 🎨 Templates

### Classic Professional
- Traditional navy blue accents
- Clean, professional layout
- Ideal for corporate positions

### Modern Clean
- Contemporary dark slate styling
- Bold headings with bright blue accents
- Perfect for tech and creative roles

### Minimal Elegant
- Simple black and gray design
- No decorative lines
- Great for academic and formal applications

---

## 📖 Usage Guide

### Step 1: Upload Document (Optional)
1. Click **"📁 Choose Document"**
2. Select your existing resume (PDF or Word)
3. The app automatically parses and fills in your information

### Step 2: Edit Information
Navigate through the tabs to complete your resume:

#### Basic Info Tab
- Enter your full name (required)
- Add professional title (e.g., "Software Engineer")
- Include contact details: email, phone, location, LinkedIn

#### Summary & Skills Tab
- Write a compelling professional summary (50+ words recommended)
- List key skills separated by commas

#### Experience Tab
- Add work history in reverse chronological order
- Use bullet points for responsibilities and achievements
- Format: Job Title | Company | Duration | Details

#### Education Tab
- Include degrees, universities, and graduation years
- Add relevant certifications

#### Additional Tab
- List notable projects
- Add languages spoken
- Include references (optional)

### Step 3: Generate Resume
1. Select your preferred template from the dropdown
2. Click **"📄 Generate PDF"** or **"📝 Generate Word"**
3. Choose save location
4. Optionally open the containing folder

---

## 🛠️ Project Structure

```
cv-forge/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── run.bat                         # Windows launcher
├── run.sh                          # macOS/Linux launcher
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py         # Enhanced GUI with modern UI
│   └── utils/
│       ├── __init__.py
│       ├── document_parser.py      # Enhanced PDF/Word parsing
│       ├── resume_generator.py     # Multi-template generation
│       ├── validation.py           # Input validation
│       └── logger.py               # Logging utility
└── output/                         # Generated resumes
```

---

## 🔧 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| python-docx | ≥1.0.0 | Word document handling |
| PyPDF2 | ≥3.0.1 | PDF file operations |
| pdfplumber | ≥0.10.0 | PDF text extraction |
| reportlab | ≥4.0.9 | PDF generation |
| Pillow | ≥10.1.0 | Image processing support |

---

## 💡 Tips for Best Results

### Content Quality
1. **Name**: Use your full professional name
2. **Contact**: Include email and at least one other contact method
3. **Summary**: Write 3-5 sentences highlighting your value proposition
4. **Skills**: List 5+ relevant skills for your target role
5. **Experience**: Use action verbs and quantify achievements
6. **Formatting**: Use consistent date formats and bullet points

### ATS Optimization
- Include relevant keywords from job descriptions
- Use standard section headings
- Avoid graphics and complex formatting
- Keep it to 1-2 pages

### Template Selection
- **Classic**: Finance, law, government, traditional industries
- **Modern**: Tech, startups, marketing, creative fields
- **Minimal**: Academia, research, formal applications

---

## 🐛 Troubleshooting

### Issue: Application won't start
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: PDF parsing errors
**Solution**: 
- Ensure PDF is not password-protected
- Try converting to Word format first
- Some scanned PDFs may not be parseable

### Issue: Formatting looks different in exported file
**Solution**:
- This is normal - templates optimize for each format
- PDF provides the most consistent appearance
- Word format allows further editing

### Issue: Auto-save not working
**Solution**:
- Check write permissions in your home directory
- Drafts are saved to: `~/.cvforge/draft.json`

### Issue: Missing sections after upload
**Solution**:
- The parser uses pattern matching
- Manually add missing sections
- Ensure section headers are clearly labeled

---

## 📊 Resume Completion Guide

| Completion | Status | Recommendation |
|------------|--------|----------------|
| 0-40% | 🔴 Incomplete | Add required sections |
| 40-70% | 🟡 Good progress | Add more details |
| 70-100% | 🟢 Ready to export | Review and export |

---

## 🔒 Privacy & Security

- ✅ **100% Local Processing** - Your data never leaves your computer
- ✅ **No Account Required** - No registration needed
- ✅ **No Data Collection** - We don't track or store your information
- ✅ **No Internet Required** - Works completely offline

---

## 📝 Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save draft |
| `Ctrl+O` | Open document |
| `Ctrl+E` | Export as PDF |
| `Ctrl+W` | Export as Word |
| `Ctrl+N` | Clear all fields |
| `F5` | Refresh preview |

---

## 🆘 Support

### Getting Help
1. Check this README for feature documentation
2. Review the troubleshooting section above
3. Check log files at: `~/.cvforge/logs/`

### Common Questions

**Q: Can I import my LinkedIn profile?**
A: Currently only PDF and Word documents are supported for import.

**Q: How do I create multiple resume versions?**
A: Save drafts with different names, or export and save separately.

**Q: Can I customize the templates?**
A: Template customization is planned for a future release.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

Built with:
- Python & Tkinter for the GUI
- ReportLab for PDF generation
- python-docx for Word documents
- pdfplumber for PDF parsing

---

**CV Forge v2.0** | Built with Python • Designed for Professionals

Made with ❤️ for job seekers everywhere
