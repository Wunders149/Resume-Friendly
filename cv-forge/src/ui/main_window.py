"""
Main GUI window for CV Forge application
Enhanced version with modern UI, auto-save, templates, and preview
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.document_parser import DocumentParser
from utils.resume_generator import ResumeGenerator
from utils.validation import ResumeValidator, ValidationSeverity, InputSanitizer
from utils.logger import log_debug, log_info, log_warning, log_error
from utils.ai_parser import AIParser


class CVForgeApp:
    """Main application window for CV Forge - Enhanced Version"""

    def __init__(self, root):
        """
        Initialize the application

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("CV Forge - Resume Builder")
        self.root.geometry("1200x800")
        self.root.minsize(1024, 700)
        self.root.configure(bg='#f5f5f5')

        # Set window icon (if available)
        try:
            self.root.iconbitmap(default='cvforge.ico')
        except:
            pass

        self.parser = DocumentParser()
        self.generator = ResumeGenerator()
        self.ai_parser = AIParser()

        # Auto-save configuration
        self.auto_save_enabled = True
        self.auto_save_interval = 30000  # 30 seconds
        self.last_saved = None
        self.has_unsaved_changes = False
        self.draft_file = Path.home() / ".cvforge" / "draft.json"
        self._ensure_draft_dir()

        # AI parsing option
        self.use_ai_parsing = tk.BooleanVar(value=False)
        self.ai_available = self.ai_parser.is_available()

        # Resume data with enhanced fields
        self.resume_data = {
            'name': '',
            'title': '',  # Professional title
            'contact': '',
            'summary': '',
            'skills': '',
            'experience': '',
            'education': '',
            'certifications': '',
            'projects': '',
            'languages': '',
            'references': ''
        }

        # Template selection
        self.selected_template = tk.StringVar(value="classic")
        self.template_options = {
            "classic": "Classic Professional",
            "modern": "Modern Clean",
            "minimal": "Minimal Elegant"
        }

        # Current file path
        self.current_file_path = None

        # Setup UI
        self.setup_ui()

        # Setup auto-save
        self._setup_auto_save()

        # Load any existing draft
        self._load_draft()

        # Bind keyboard shortcuts
        self._setup_keyboard_shortcuts()

    def _ensure_draft_dir(self):
        """Ensure draft directory exists"""
        self.draft_file.parent.mkdir(parents=True, exist_ok=True)

    def _setup_auto_save(self):
        """Setup auto-save timer"""
        def auto_save():
            if self.has_unsaved_changes and self.auto_save_enabled:
                self._save_draft()
            self.root.after(self.auto_save_interval, auto_save)
        
        self.root.after(self.auto_save_interval, auto_save)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-s>', lambda e: self._save_draft())
        self.root.bind('<Control-o>', lambda e: self.upload_file())
        self.root.bind('<Control-e>', lambda e: self.generate_resume('pdf'))
        self.root.bind('<Control-w>', lambda e: self.generate_resume('docx'))
        self.root.bind('<Control-n>', lambda e: self.clear_all())
        self.root.bind('<F5>', lambda e: self._refresh_preview())

    def _save_draft(self):
        """Save current state to draft file"""
        try:
            self._update_data_from_widgets()
            draft = {
                'resume_data': self.resume_data,
                'template': self.selected_template.get(),
                'timestamp': datetime.now().isoformat()
            }
            with open(self.draft_file, 'w', encoding='utf-8') as f:
                json.dump(draft, f, indent=2)
            self.last_saved = datetime.now()
            self.has_unsaved_changes = False
            self.status_label.config(text=f"✓ Auto-saved at {self.last_saved.strftime('%H:%M:%S')}")
        except Exception as e:
            pass  # Silent fail for auto-save

    def _load_draft(self):
        """Load draft if exists"""
        if self.draft_file.exists():
            try:
                with open(self.draft_file, 'r', encoding='utf-8') as f:
                    draft = json.load(f)
                self.resume_data = draft.get('resume_data', self.resume_data)
                self.selected_template.set(draft.get('template', 'classic'))
                self._populate_widgets()
                self.status_label.config(text="Draft loaded from previous session")
            except Exception as e:
                pass

    def _update_data_from_widgets(self):
        """Update resume_data from all widgets"""
        try:
            self.resume_data['name'] = self.name_entry.get().strip()
            self.resume_data['title'] = self.title_entry.get().strip()
            self.resume_data['contact'] = self.contact_text.get('1.0', tk.END).strip()
            self.resume_data['summary'] = self.summary_text.get('1.0', tk.END).strip()
            self.resume_data['skills'] = self.skills_text.get('1.0', tk.END).strip()
            self.resume_data['experience'] = self.experience_text.get('1.0', tk.END).strip()
            self.resume_data['education'] = self.education_text.get('1.0', tk.END).strip()
            self.resume_data['certifications'] = self.certifications_text.get('1.0', tk.END).strip()
            self.resume_data['projects'] = self.projects_text.get('1.0', tk.END).strip()
            self.resume_data['languages'] = self.languages_text.get('1.0', tk.END).strip()
            self.resume_data['references'] = self.references_text.get('1.0', tk.END).strip()
        except:
            pass

    def _populate_widgets(self):
        """Populate widgets with resume_data"""
        try:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.resume_data.get('name', ''))
            
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, self.resume_data.get('title', ''))
            
            self.contact_text.delete('1.0', tk.END)
            self.contact_text.insert('1.0', self.resume_data.get('contact', ''))
            
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.insert('1.0', self.resume_data.get('summary', ''))
            
            self.skills_text.delete('1.0', tk.END)
            self.skills_text.insert('1.0', self.resume_data.get('skills', ''))
            
            self.experience_text.delete('1.0', tk.END)
            self.experience_text.insert('1.0', self.resume_data.get('experience', ''))
            
            self.education_text.delete('1.0', tk.END)
            self.education_text.insert('1.0', self.resume_data.get('education', ''))
            
            self.certifications_text.delete('1.0', tk.END)
            self.certifications_text.insert('1.0', self.resume_data.get('certifications', ''))
            
            self.projects_text.delete('1.0', tk.END)
            self.projects_text.insert('1.0', self.resume_data.get('projects', ''))
            
            self.languages_text.delete('1.0', tk.END)
            self.languages_text.insert('1.0', self.resume_data.get('languages', ''))
            
            self.references_text.delete('1.0', tk.END)
            self.references_text.insert('1.0', self.resume_data.get('references', ''))
        except:
            pass

    def _mark_changed(self, event=None):
        """Mark data as changed"""
        self.has_unsaved_changes = True
        self.status_label.config(text="● Unsaved changes")

    def _get_completion_percentage(self):
        """Calculate resume completion percentage"""
        self._update_data_from_widgets()
        required_fields = ['name', 'contact', 'summary', 'skills', 'experience', 'education']
        optional_fields = ['certifications', 'projects', 'languages', 'references', 'title']
        
        completed_required = sum(1 for f in required_fields if self.resume_data.get(f, '').strip())
        completed_optional = sum(1 for f in optional_fields if self.resume_data.get(f, '').strip())
        
        required_score = (completed_required / len(required_fields)) * 0.7
        optional_score = (completed_optional / len(optional_fields)) * 0.3
        
        return int((required_score + optional_score) * 100)

    def _update_progress(self):
        """Update progress bar"""
        percentage = self._get_completion_percentage()
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage}% Complete")
        
        # Color coding
        if percentage < 40:
            self.progress_bar.configure(style='low.Horizontal.TProgressbar')
        elif percentage < 70:
            self.progress_bar.configure(style='medium.Horizontal.TProgressbar')
        else:
            self.progress_bar.configure(style='high.Horizontal.TProgressbar')

    def _refresh_preview(self):
        """Refresh the resume preview"""
        self._update_data_from_widgets()
        preview_text = self._generate_preview_text()
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview_text)
        self.preview_text.config(state=tk.DISABLED)

    def _generate_preview_text(self):
        """Generate text preview of resume"""
        lines = []
        
        # Name and title
        name = self.resume_data.get('name', '[Your Name]')
        title = self.resume_data.get('title', '')
        lines.append("=" * 60)
        lines.append(name.upper())
        if title:
            lines.append(title)
        lines.append("=" * 60)
        
        # Contact
        contact = self.resume_data.get('contact', '')
        if contact:
            lines.append(contact)
            lines.append("")
        
        # Summary
        summary = self.resume_data.get('summary', '')
        if summary:
            lines.append("PROFESSIONAL SUMMARY")
            lines.append("-" * 40)
            lines.append(summary[:200] + ("..." if len(summary) > 200 else ""))
            lines.append("")
        
        # Skills
        skills = self.resume_data.get('skills', '')
        if skills:
            lines.append("SKILLS")
            lines.append("-" * 40)
            lines.append(skills[:150] + ("..." if len(skills) > 150 else ""))
            lines.append("")
        
        # Experience
        experience = self.resume_data.get('experience', '')
        if experience:
            lines.append("EXPERIENCE")
            lines.append("-" * 40)
            lines.append(experience[:300] + ("..." if len(experience) > 300 else ""))
            lines.append("")
        
        # Education
        education = self.resume_data.get('education', '')
        if education:
            lines.append("EDUCATION")
            lines.append("-" * 40)
            lines.append(education[:200] + ("..." if len(education) > 200 else ""))
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)

    def setup_ui(self):
        """Setup the user interface with modern design"""
        
        # Configure styles
        self._setup_styles()

        # Main container with grid
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Header
        self._create_header(main_frame)
        
        # Content area - split into left (editor) and right (preview)
        content_frame = tk.Frame(main_frame, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left panel - Editor
        left_panel = tk.Frame(content_frame, bg='#f5f5f5')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel - Preview
        right_panel = tk.Frame(content_frame, bg='#f5f5f5')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(5, 0))
        right_panel.pack_propagate(False)
        right_panel.config(width=400)
        
        # Create left panel content
        self._create_left_panel(left_panel)
        
        # Create right panel content (preview)
        self._create_right_panel(right_panel)
        
        # Footer with status
        self._create_footer(main_frame)

    def _setup_styles(self):
        """Setup ttk styles for modern look"""
        style = ttk.Style()
        
        # Try to use clam theme as base
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure colors
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', foreground='#333333')
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), background='#f5f5f5')
        style.configure('Section.TLabel', font=('Segoe UI', 11, 'bold'), background='#f5f5f5')
        
        # Button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Segoe UI', 10))
        
        # Progressbar styles
        style.configure('low.Horizontal.TProgressbar', background='#e74c3c')
        style.configure('medium.Horizontal.TProgressbar', background='#f39c12')
        style.configure('high.Horizontal.TProgressbar', background='#27ae60')

    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="CV Forge",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Subtitle
        subtitle = tk.Label(
            header_frame,
            text="Professional Resume Builder",
            font=('Segoe UI', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Template selector
        template_frame = tk.Frame(header_frame, bg='#2c3e50')
        template_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        tk.Label(
            template_frame,
            text="Template:",
            font=('Segoe UI', 9),
            fg='white',
            bg='#2c3e50'
        ).pack(side=tk.LEFT, padx=5)
        
        template_combo = ttk.Combobox(
            template_frame,
            textvariable=self.selected_template,
            values=list(self.template_options.keys()),
            state='readonly',
            width=15
        )
        template_combo.pack(side=tk.LEFT, padx=5)
        template_combo.bind('<<ComboboxSelected>>', lambda e: self._mark_changed())

    def _create_left_panel(self, parent):
        """Create left panel with editor"""
        # Upload section
        upload_frame = tk.LabelFrame(
            parent,
            text="  Upload Document  ",
            font=('Segoe UI', 10, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        upload_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File path display
        self.file_label = tk.Label(
            upload_frame,
            text="No file selected",
            font=('Segoe UI', 9),
            bg='#ffffff',
            fg='#7f8c8d',
            anchor='w',
            padx=10,
            pady=5
        )
        self.file_label.pack(fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(upload_frame, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X)
        
        upload_btn = tk.Button(
            btn_frame,
            text="📁 Choose Document",
            command=self.upload_file,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            padx=15,
            pady=6,
            relief=tk.FLAT,
            cursor='hand2'
        )
        upload_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑 Clear All",
            command=self.clear_all,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 9),
            padx=15,
            pady=6,
            relief=tk.FLAT,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        save_draft_btn = tk.Button(
            btn_frame,
            text="💾 Save Draft",
            command=self._save_draft,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 9),
            padx=15,
            pady=6,
            relief=tk.FLAT,
            cursor='hand2'
        )
        save_draft_btn.pack(side=tk.LEFT, padx=2)
        
        # Progress section
        progress_frame = tk.Frame(parent, bg='#f5f5f5')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(side=tk.LEFT)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0% Complete",
            font=('Segoe UI', 9),
            bg='#f5f5f5',
            fg='#7f8c8d',
            width=15
        )
        self.progress_label.pack(side=tk.LEFT, padx=10)
        
        # Tabs section
        tabs_frame = tk.LabelFrame(
            parent,
            text="  Edit Resume Information  ",
            font=('Segoe UI', 10, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=5,
            pady=5
        )
        tabs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self._create_tabs()

    def _create_tabs(self):
        """Create all editor tabs"""
        # Tab 1: Basic Info
        basic_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(basic_tab, text="  Basic Info  ")
        self._create_basic_tab(basic_tab)
        
        # Tab 2: Summary & Skills
        summary_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(summary_tab, text="  Summary & Skills  ")
        self._create_summary_tab(summary_tab)
        
        # Tab 3: Experience
        exp_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(exp_tab, text="  Experience  ")
        self._create_experience_tab(exp_tab)
        
        # Tab 4: Education
        edu_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(edu_tab, text="  Education  ")
        self._create_education_tab(edu_tab)
        
        # Tab 5: Additional
        add_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(add_tab, text="  Additional  ")
        self._create_additional_tab(add_tab)

    def _create_basic_tab(self, parent):
        """Create basic information tab"""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Name
        tk.Label(frame, text="Full Name *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.name_entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, bg='#f9f9f9')
        self.name_entry.pack(fill=tk.X, pady=5)
        self.name_entry.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        
        # Professional Title
        tk.Label(frame, text="Professional Title", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.title_entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, bg='#f9f9f9')
        self.title_entry.pack(fill=tk.X, pady=5)
        self.title_entry.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        tk.Label(frame, text="e.g., Software Engineer | Project Manager | Data Analyst", 
                bg='#ffffff', font=('Segoe UI', 8), fg='#95a5a6').pack(anchor=tk.W, pady=(5, 0))
        
        # Contact
        tk.Label(frame, text="Contact Info *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.contact_text = tk.Text(frame, font=('Segoe UI', 9), height=4, relief=tk.FLAT, bg='#f9f9f9')
        self.contact_text.pack(fill=tk.X, pady=5)
        self.contact_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        tk.Label(frame, text="Email | Phone | Location | LinkedIn", 
                bg='#ffffff', font=('Segoe UI', 8), fg='#95a5a6').pack(anchor=tk.W, pady=(5, 0))

    def _create_summary_tab(self, parent):
        """Create summary and skills tab"""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Summary
        tk.Label(frame, text="Professional Summary *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.summary_text = tk.Text(frame, font=('Segoe UI', 9), height=6, relief=tk.FLAT, bg='#f9f9f9')
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        
        # Skills
        tk.Label(frame, text="Skills *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.skills_text = tk.Text(frame, font=('Segoe UI', 9), height=5, relief=tk.FLAT, bg='#f9f9f9')
        self.skills_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.skills_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        tk.Label(frame, text="Separate with commas: Python, Java, Project Management, Agile", 
                bg='#ffffff', font=('Segoe UI', 8), fg='#95a5a6').pack(anchor=tk.W, pady=(5, 0))

    def _create_experience_tab(self, parent):
        """Create experience tab"""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(frame, text="Professional Experience *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.experience_text = tk.Text(frame, font=('Segoe UI', 9), height=15, relief=tk.FLAT, bg='#f9f9f9')
        self.experience_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.experience_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        
        help_frame = tk.Frame(frame, bg='#ecf0f1')
        help_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(help_frame, text="Format:", bg='#ecf0f1', font=('Segoe UI', 8, 'bold'), fg='#7f8c8d').pack(anchor=tk.W)
        tk.Label(help_frame, text="Job Title | Company | Duration\n• Responsibility/Achievement\n• Responsibility/Achievement", 
                bg='#ecf0f1', font=('Segoe UI', 8), fg='#95a5a6', justify=tk.LEFT).pack(anchor=tk.W, pady=5)

    def _create_education_tab(self, parent):
        """Create education tab"""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Education
        tk.Label(frame, text="Education *", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.education_text = tk.Text(frame, font=('Segoe UI', 9), height=6, relief=tk.FLAT, bg='#f9f9f9')
        self.education_text.pack(fill=tk.X, pady=5)
        self.education_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        tk.Label(frame, text="Degree | University | Graduation Year", 
                bg='#ffffff', font=('Segoe UI', 8), fg='#95a5a6').pack(anchor=tk.W, pady=(5, 0))
        
        # Certifications
        tk.Label(frame, text="Certifications & Licenses", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.certifications_text = tk.Text(frame, font=('Segoe UI', 9), height=5, relief=tk.FLAT, bg='#f9f9f9')
        self.certifications_text.pack(fill=tk.X, pady=5)
        self.certifications_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))

    def _create_additional_tab(self, parent):
        """Create additional info tab"""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Projects
        tk.Label(frame, text="Projects", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(0, 5))
        self.projects_text = tk.Text(frame, font=('Segoe UI', 9), height=5, relief=tk.FLAT, bg='#f9f9f9')
        self.projects_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.projects_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        
        # Languages
        tk.Label(frame, text="Languages", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.languages_text = tk.Text(frame, font=('Segoe UI', 9), height=3, relief=tk.FLAT, bg='#f9f9f9')
        self.languages_text.pack(fill=tk.X, pady=5)
        self.languages_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        
        # References
        tk.Label(frame, text="References", bg='#ffffff', font=('Segoe UI', 10)).pack(anchor=tk.W, pady=(15, 5))
        self.references_text = tk.Text(frame, font=('Segoe UI', 9), height=3, relief=tk.FLAT, bg='#f9f9f9')
        self.references_text.pack(fill=tk.X, pady=5)
        self.references_text.bind('<KeyRelease>', lambda e: (self._mark_changed(), self._update_progress()))
        tk.Label(frame, text="Available upon request (optional)", 
                bg='#ffffff', font=('Segoe UI', 8), fg='#95a5a6').pack(anchor=tk.W, pady=(5, 0))

    def _create_right_panel(self, parent):
        """Create right panel with preview"""
        preview_frame = tk.LabelFrame(
            parent,
            text="  Live Preview  ",
            font=('Segoe UI', 10, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=5,
            pady=5
        )
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Preview text widget
        self.preview_text = tk.Text(
            preview_frame,
            font=('Consolas', 9),
            bg='#ffffff',
            fg='#333333',
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            preview_frame,
            text="🔄 Refresh Preview (F5)",
            command=self._refresh_preview,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 9),
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        )
        refresh_btn.pack(pady=5)

    def _create_footer(self, parent):
        """Create footer with status and export buttons"""
        footer_frame = tk.Frame(parent, bg='#ecf0f1')
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Export buttons
        btn_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        pdf_btn = tk.Button(
            btn_frame,
            text="📄 Generate PDF",
            command=lambda: self.generate_resume('pdf'),
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        pdf_btn.pack(side=tk.LEFT, padx=5)
        
        docx_btn = tk.Button(
            btn_frame,
            text="📝 Generate Word",
            command=lambda: self.generate_resume('docx'),
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        docx_btn.pack(side=tk.LEFT, padx=5)

    def update_data(self, field, value):
        """Update resume data (legacy method)"""
        self.resume_data[field] = value.strip()
        self._mark_changed()
        self._update_progress()

    def upload_file(self):
        """Upload and parse document"""
        filetypes = [
            ('All Documents', '*.pdf *.docx *.doc'),
            ('PDF Files', '*.pdf'),
            ('Word Files', '*.docx *.doc')
        ]

        filepath = filedialog.askopenfilename(
            title="Select your resume document",
            filetypes=filetypes
        )

        if filepath:
            try:
                self.current_file_path = filepath
                self.file_label.config(text=f"📄 {os.path.basename(filepath)}")
                
                # Ask user if they want to use AI parsing (if available)
                use_ai = False
                if self.ai_available:
                    use_ai = messagebox.askyesno(
                        "AI Parsing Available",
                        "AI-powered parsing is available for better extraction.\n\n"
                        "Would you like to use AI to parse this resume?\n\n"
                        "Click 'Yes' for AI parsing (more accurate)\n"
                        "Click 'No' for standard parsing (faster)",
                        icon=messagebox.QUESTION
                    )
                
                if use_ai:
                    self._parse_with_ai(filepath)
                else:
                    self._parse_standard(filepath)

            except Exception as e:
                messagebox.showerror("Error", f"Error parsing document: {str(e)}")
                self.status_label.config(text="Error parsing document")

    def _parse_standard(self, filepath):
        """Parse document using standard regex-based parser"""
        self.status_label.config(text=f"Parsing {os.path.basename(filepath)}...")
        self.root.update()

        # Parse document
        text = self.parser.parse_document(filepath)
        sections = self.parser.extract_sections(text)
        lines = text.split('\n')

        # Try to extract name from first line
        first_line = lines[0].strip() if lines else ''
        if first_line and len(first_line) < 50:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, first_line)

        # Try to extract professional title from second line
        if len(lines) > 1:
            second_line = lines[1].strip()
            if second_line and len(second_line) < 80 and (
                '|' in second_line or
                any(kw in second_line.lower() for kw in [
                    'engineer', 'developer', 'manager', 'analyst', 'designer',
                    'consultant', 'director', 'lead', 'senior', 'junior', 'intern',
                    'specialist', 'coordinator', 'administrator', 'architect'
                ])
            ):
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, second_line)

        # Populate fields
        if sections.get('contact'):
            self.contact_text.delete('1.0', tk.END)
            self.contact_text.insert('1.0', sections['contact'])

        if sections.get('summary'):
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.insert('1.0', sections['summary'])

        if sections.get('skills'):
            self.skills_text.delete('1.0', tk.END)
            self.skills_text.insert('1.0', sections['skills'])

        if sections.get('experience'):
            self.experience_text.delete('1.0', tk.END)
            self.experience_text.insert('1.0', sections['experience'])

        if sections.get('education'):
            self.education_text.delete('1.0', tk.END)
            self.education_text.insert('1.0', sections['education'])

        if sections.get('certifications'):
            self.certifications_text.delete('1.0', tk.END)
            self.certifications_text.insert('1.0', sections['certifications'])

        if sections.get('projects'):
            self.projects_text.delete('1.0', tk.END)
            self.projects_text.insert('1.0', sections['projects'])

        if sections.get('languages'):
            self.languages_text.delete('1.0', tk.END)
            self.languages_text.insert('1.0', sections['languages'])

        if sections.get('references'):
            self.references_text.delete('1.0', tk.END)
            self.references_text.insert('1.0', sections['references'])

        self._update_data_from_widgets()
        self._mark_changed()
        self._update_progress()
        self._refresh_preview()

        messagebox.showinfo("Success", f"Document parsed successfully!\n\nPlease review and edit the information as needed.")

    def _parse_with_ai(self, filepath):
        """Parse document using AI parser"""
        self.status_label.config(text=f"🤖 AI parsing {os.path.basename(filepath)}...")
        self.root.update()

        try:
            # Parse document to get text
            text = self.parser.parse_document(filepath)
            
            # Use AI to extract structured data
            ai_result = self.ai_parser.parse_resume(text)
            
            # Populate fields with AI-extracted data
            if ai_result.get('name'):
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, ai_result['name'])

            if ai_result.get('title'):
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, ai_result['title'])

            if ai_result.get('contact'):
                self.contact_text.delete('1.0', tk.END)
                self.contact_text.insert('1.0', ai_result['contact'])

            if ai_result.get('summary'):
                self.summary_text.delete('1.0', tk.END)
                self.summary_text.insert('1.0', ai_result['summary'])

            if ai_result.get('skills'):
                self.skills_text.delete('1.0', tk.END)
                self.skills_text.insert('1.0', ai_result['skills'])

            if ai_result.get('experience'):
                self.experience_text.delete('1.0', tk.END)
                self.experience_text.insert('1.0', ai_result['experience'])

            if ai_result.get('education'):
                self.education_text.delete('1.0', tk.END)
                self.education_text.insert('1.0', ai_result['education'])

            if ai_result.get('certifications'):
                self.certifications_text.delete('1.0', tk.END)
                self.certifications_text.insert('1.0', ai_result['certifications'])

            if ai_result.get('projects'):
                self.projects_text.delete('1.0', tk.END)
                self.projects_text.insert('1.0', ai_result['projects'])

            if ai_result.get('languages'):
                self.languages_text.delete('1.0', tk.END)
                self.languages_text.insert('1.0', ai_result['languages'])

            if ai_result.get('references'):
                self.references_text.delete('1.0', tk.END)
                self.references_text.insert('1.0', ai_result['references'])

            self._update_data_from_widgets()
            self._mark_changed()
            self._update_progress()
            self._refresh_preview()

            messagebox.showinfo(
                "AI Parsing Complete", 
                f"✅ AI successfully extracted resume information!\n\n"
                f"Please review the extracted data and make any necessary corrections."
            )
            
        except Exception as e:
            messagebox.showerror(
                "AI Parsing Error",
                f"AI parsing failed: {str(e)}\n\n"
                f"Falling back to standard parsing..."
            )
            # Fallback to standard parsing
            self._parse_standard(filepath)

    def generate_resume(self, format_type):
        self._update_data_from_widgets()

        if not self.resume_data['name']:
            messagebox.showwarning("Warning", "Please enter your name before generating a resume.")
            self.notebook.select(0)
            self.name_entry.focus()
            return

        if not self.resume_data['contact']:
            messagebox.showwarning("Warning", "Please enter your contact information.")
            return

        # Ask for save location
        default_filename = f"{self.resume_data['name'].replace(' ', '_')}_resume"
        filetypes = [('PDF Files', '*.pdf')] if format_type == 'pdf' else [('Word Files', '*.docx')]

        filepath = filedialog.asksaveasfilename(
            title=f"Save Resume as {format_type.upper()}",
            defaultextension=f".{format_type}",
            filetypes=filetypes,
            initialfile=default_filename,
            initialdir=Path.home() / "Documents"
        )

        if filepath:
            try:
                self.status_label.config(text=f"Generating {format_type.upper()}...")
                self.root.update()

                # Generate with selected template
                if format_type == 'pdf':
                    output_path = self.generator.generate_pdf(
                        self.resume_data,
                        filename=filepath,
                        template=self.selected_template.get()
                    )
                else:
                    output_path = self.generator.generate_docx(
                        self.resume_data,
                        filename=filepath,
                        template=self.selected_template.get()
                    )

                self.status_label.config(text=f"✓ Generated: {os.path.basename(filepath)}")

                # Show download options dialog
                try:
                    self._show_download_options(output_path)
                except Exception as e:
                    log_error(f"Error showing download dialog: {e}")
                    # Fallback to simple messagebox
                    if messagebox.askyesno("Download Complete", 
                        f"Resume generated successfully!\n\nSaved to: {output_path}\n\nOpen containing folder?"):
                        os.startfile(os.path.dirname(output_path))

            except Exception as e:
                messagebox.showerror("Error", f"Error generating resume: {str(e)}")
                self.status_label.config(text="Error generating resume")

    def _show_download_options(self, filepath):
        """Show download options dialog"""
        # Create custom dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Download Complete!")
        dialog.geometry("450x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"450x280+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg='#27ae60', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        success_icon = tk.Label(
            header_frame,
            text="✓",
            font=('Segoe UI', 28, 'bold'),
            fg='white',
            bg='#27ae60'
        )
        success_icon.pack(pady=10)
        
        tk.Label(
            header_frame,
            text="Resume Generated Successfully!",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg='#27ae60'
        ).pack()
        
        # Content
        content_frame = tk.Frame(dialog, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # File info
        info_frame = tk.LabelFrame(
            content_frame,
            text="  File Information  ",
            font=('Segoe UI', 9, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filename
        tk.Label(
            info_frame,
            text=f"File: {os.path.basename(filepath)}",
            font=('Segoe UI', 9),
            bg='#f5f5f5',
            fg='#333333',
            anchor='w'
        ).pack(fill=tk.X, pady=2)
        
        # Location
        location_text = f"Location: {os.path.dirname(filepath)}"
        if len(location_text) > 55:
            location_text = location_text[:52] + "..."
        tk.Label(
            info_frame,
            text=location_text,
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d',
            anchor='w'
        ).pack(fill=tk.X, pady=2)
        
        # Size
        try:
            file_size = os.path.getsize(filepath)
            size_text = f"Size: {file_size / 1024:.1f} KB"
        except:
            size_text = "Size: Unknown"
        tk.Label(
            info_frame,
            text=size_text,
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d',
            anchor='w'
        ).pack(fill=tk.X, pady=2)
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Open File button
        open_btn = tk.Button(
            btn_frame,
            text="📂 Open File",
            command=lambda: self._open_file(filepath, dialog),
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        open_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Open Folder button
        folder_btn = tk.Button(
            btn_frame,
            text="📁 Open Folder",
            command=lambda: self._open_folder(filepath, dialog),
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        folder_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Close button
        close_btn = tk.Button(
            btn_frame,
            text="Close",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 9),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        close_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Additional options frame
        options_frame = tk.Frame(content_frame, bg='#ecf0f1')
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            options_frame,
            text="Quick Actions:",
            font=('Segoe UI', 8, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        # Copy to clipboard option
        copy_btn = tk.Button(
            options_frame,
            text="📋 Copy File Path to Clipboard",
            command=lambda: self._copy_path(filepath, dialog),
            bg='#ffffff',
            fg='#2c3e50',
            font=('Segoe UI', 8),
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#e0e0e0'
        )
        copy_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Email option (shows mailto suggestion)
        email_btn = tk.Button(
            options_frame,
            text="📧 Prepare to Email",
            command=lambda: self._prepare_email(filepath, dialog),
            bg='#ffffff',
            fg='#2c3e50',
            font=('Segoe UI', 8),
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#e0e0e0'
        )
        email_btn.pack(fill=tk.X, padx=10, pady=5)

    def _open_file(self, filepath, dialog):
        """Open the generated file"""
        try:
            os.startfile(filepath)
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def _open_folder(self, filepath, dialog):
        """Open the containing folder"""
        try:
            os.startfile(os.path.dirname(filepath))
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")

    def _copy_path(self, filepath, dialog):
        """Copy file path to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(filepath)
            self.root.update()
            messagebox.showinfo("Copied", "File path copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy path: {str(e)}")

    def _prepare_email(self, filepath, dialog):
        """Prepare to email the resume"""
        try:
            import webbrowser
            subject = f"Resume - {self.resume_data.get('name', 'Applicant')}"
            body = f"Please find attached my resume.\n\nBest regards,\n{self.resume_data.get('name', '')}"
            mailto_url = f"mailto:?subject={subject}&body={body}"
            webbrowser.open(mailto_url)
            # Note: User will need to attach the file manually
            messagebox.showinfo(
                "Email Preparation",
                f"Your email client has been opened.\n\nPlease attach:\n{filepath}\n\nbefore sending."
            )
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open email client: {str(e)}")

    def clear_all(self):
        """Clear all fields"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all fields?"):
            self.resume_data = {key: '' for key in self.resume_data}
            self._populate_widgets()
            self.file_label.config(text="No file selected")
            self.current_file_path = None
            self._mark_changed()
            self._update_progress()
            self._refresh_preview()
            self.status_label.config(text="All fields cleared")


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set DPI awareness for Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = CVForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
