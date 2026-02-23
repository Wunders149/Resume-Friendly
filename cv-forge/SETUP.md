# CV Forge Setup Instructions

## Quick Start (Recommended)

### Windows
1. Double-click `run.bat`
   - The script will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Launch the application

### macOS/Linux
1. Open Terminal in the `cv-forge` directory
2. Run: `bash run.sh`
   - The script will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Launch the application

---

## Manual Setup

If the quick start scripts don't work, follow these steps:

### Step 1: Install Python
- Download Python 3.7+ from https://www.python.org
- During installation on Windows, **check "Add Python to PATH"**
- Verify installation: `python --version`

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
```bash
python app.py
```

---

## Troubleshooting

### Python not found
- Check if Python is installed: `python --version`
- On some systems, you may need to use `python3` instead of `python`
- Ensure Python is added to your system PATH

### Permission denied (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Module not found errors
- Make sure the virtual environment is activated
- If still having issues, reinstall dependencies:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

### PDF/Word parsing fails
1. Ensure the file is in standard format (not password-protected)
2. Try a different document
3. Check the Requirements section in README.md

---

## File Structure

After setup, your directory should look like:
```
cv-forge/
├── app.py
├── run.bat
├── run.sh
├── requirements.txt
├── README.md
├── SETUP.md  (this file)
├── .gitignore
├── src/
│   ├── ui/main_window.py
│   └── utils/
│       ├── document_parser.py
│       └── resume_generator.py
└── output/  (created when you generate a resume)
```

---

## First Run

1. Launch the application
2. Click "Choose PDF or Word Document" to upload your resume
3. Edit the information in the tabs
4. Click "Generate PDF Resume" or "Generate Word Resume"
5. Your resume will be saved in the `output/` folder

---

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **RAM**: 256 MB minimum
- **Disk Space**: 100 MB (including dependencies)

---

## Next Steps

1. Read the README.md for detailed feature documentation
2. Explore the GUI and familiarize yourself with the interface
3. Try uploading a sample resume
4. Experiment with editing and generating different formats

Happy resume building! 🚀
