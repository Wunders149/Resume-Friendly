"""
Main Window for CV-Forge.
CustomTkinter tabbed interface for resume building.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
from pathlib import Path

from models.resume import Resume, Education, Certification, Experience
from exporters.docx_exporter import DOCXExporter
from exporters.pdf_exporter import PDFExporter
from ui.forms import (
    PersonalInfoFrame,
    EducationFrame,
    CertificationFrame,
    ExperienceFrame,
    SkillsFrame,
)


class MainWindow(ctk.CTk):
    """Main application window with tabbed interface."""
    
    def __init__(self):
        super().__init__()
        
        self.title("CV-Forge - Générateur de CV ATS")
        self.geometry("1200x850")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Icons/emojis for better visual feedback
        self.save_icon = "💾"
        self.load_icon = "📂"
        self.pdf_icon = "📄"
        self.docx_icon = "📝"
        self.refresh_icon = "🔄"
        
        self.resume = Resume()
        self.profiles_path = Path(__file__).parent.parent / "data" / "profiles.json"
        
        self._build_ui()
        self._load_profiles()
    
    def _build_ui(self):
        """Build the main UI with tabs and action buttons."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Header frame with title and description
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="CV-Forge",
            font=("Helvetica", 28, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Générateur de CV optimisé pour les systèmes ATS",
            font=("Helvetica", 12),
            text_color="gray"
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # Tab view
        self.tabview = ctk.CTkTabview(header_frame)
        self.tabview.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        header_frame.grid_rowconfigure(2, weight=1)
        
        # Create tabs
        self.tab_personal = self.tabview.add("👤 Infos Personnelles")
        self.tab_education = self.tabview.add("🎓 Formation")
        self.tab_certifications = self.tabview.add("🏆 Certifications")
        self.tab_experience = self.tabview.add("💼 Expériences")
        self.tab_skills = self.tabview.add("⭐ Compétences")
        self.tab_preview = self.tabview.add("👁️ Aperçu")
        
        # Add forms to tabs with scrollable frames
        self.personal_form = PersonalInfoFrame(self.tab_personal)
        self.personal_form.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.education_form = EducationFrame(self.tab_education)
        self.education_form.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.certification_form = CertificationFrame(self.tab_certifications)
        self.certification_form.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.experience_form = ExperienceFrame(self.tab_experience)
        self.experience_form.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.skills_form = SkillsFrame(self.tab_skills)
        self.skills_form.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Preview tab with controls
        preview_container = ctk.CTkFrame(self.tab_preview)
        preview_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.preview_text = ctk.CTkTextbox(preview_container, width=800, height=500)
        self.preview_text.pack(fill="both", expand=True, pady=(0, 10))
        
        update_btn = ctk.CTkButton(
            preview_container,
            text=f"{self.refresh_icon} Actualiser l'aperçu",
            command=self._update_preview,
            height=40,
            font=("Helvetica", 12)
        )
        update_btn.pack(fill="x", pady=5)
        
        # Action buttons frame
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        # Left side buttons (Profile management)
        left_frame = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=5)
        
        ctk.CTkButton(
            left_frame,
            text=f"{self.save_icon} Sauvegarder",
            command=self._save_profile,
            width=160,
            height=40,
            font=("Helvetica", 11),
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            left_frame,
            text=f"{self.load_icon} Charger",
            command=self._load_profile,
            width=160,
            height=40,
            font=("Helvetica", 11),
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=5)
        
        # Right side buttons (Export)
        right_frame = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text=f"{self.pdf_icon} Exporter PDF",
            command=self._export_pdf,
            width=160,
            height=40,
            font=("Helvetica", 11),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text=f"{self.docx_icon} Exporter DOCX",
            command=self._export_docx,
            width=160,
            height=40,
            font=("Helvetica", 11),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(side="left", padx=5)
    
    def _collect_form_data(self) -> Resume:
        """Collect all form data into a Resume object."""
        personal_data = self.personal_form.get_data()
        education_data = self.education_form.get_data()
        certifications_data = self.certification_form.get_data()
        experiences_data = self.experience_form.get_data()
        skills_data = self.skills_form.get_data()
        
        self.resume = Resume(
            first_name=personal_data["first_name"],
            last_name=personal_data["last_name"],
            phone=personal_data["phone"],
            email=personal_data["email"],
            linkedin=personal_data["linkedin"],
            address=personal_data["address"],
            profile=personal_data["profile"],
        )
        
        for edu in education_data:
            self.resume.education.append(Education(**edu))
        
        for cert in certifications_data:
            self.resume.certifications.append(Certification(**cert))
        
        for exp in experiences_data:
            self.resume.experiences.append(Experience(**exp))
        
        self.resume.skills_hard = skills_data["skills_hard"]
        self.resume.skills_soft = skills_data["skills_soft"]
        
        return self.resume
    
    def _update_preview(self):
        """Update the preview tab with current resume data."""
        resume = self._collect_form_data()
        
        preview_content = []
        
        # Header
        preview_content.append("=" * 60)
        preview_content.append(resume.full_name.center(60))
        preview_content.append("=" * 60)
        
        contact_lines = []
        if resume.phone:
            contact_lines.append(resume.phone)
        if resume.email:
            contact_lines.append(resume.email)
        if resume.linkedin:
            contact_lines.append(resume.linkedin)
        if resume.address:
            contact_lines.append(resume.address)
        
        if contact_lines:
            preview_content.append(" | ".join(contact_lines).center(60))
        
        preview_content.append("")
        
        # Profile
        if resume.profile:
            preview_content.append("PROFIL")
            preview_content.append("-" * 40)
            preview_content.append(resume.profile)
            preview_content.append("")
        
        # Education
        if resume.education:
            preview_content.append("FORMATION")
            preview_content.append("-" * 40)
            for edu in resume.education:
                preview_content.append(f"  {edu.diploma} – {edu.institution} – {edu.dates}")
            preview_content.append("")
        
        # Certifications
        if resume.certifications:
            preview_content.append("CERTIFICATION")
            preview_content.append("-" * 40)
            for cert in resume.certifications:
                preview_content.append(f"  {cert.name} – {cert.organization} – {cert.year}")
            preview_content.append("")
        
        # Experiences
        if resume.experiences:
            preview_content.append("EXPERIENCES PROFESSIONNELLES")
            preview_content.append("-" * 40)
            for exp in resume.experiences:
                dates_range = f"{exp.start_date} – {exp.end_date}"
                preview_content.append(f"  {exp.position} – {exp.company} – {exp.city} – {dates_range}")
                for bullet in exp.bullets:
                    preview_content.append(f"    • {bullet}")
            preview_content.append("")
        
        # Skills
        if resume.skills_hard or resume.skills_soft:
            preview_content.append("COMPETENCES")
            preview_content.append("-" * 40)
            if resume.skills_hard:
                preview_content.append("  Competences Techniques:")
                for skill in resume.skills_hard:
                    preview_content.append(f"    • {skill}")
            if resume.skills_soft:
                preview_content.append("  Competences Comportementales:")
                for skill in resume.skills_soft:
                    preview_content.append(f"    • {skill}")
        
        # Update textbox
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", "\n".join(preview_content))
    
    def _export_pdf(self):
        """Export resume to PDF."""
        resume = self._collect_form_data()
        
        if not resume.first_name or not resume.last_name:
            messagebox.showwarning("Attention", "Veuillez entrer au moins le nom et le prénom")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{resume.last_name}_{resume.first_name}_CV.pdf",
        )
        
        if filepath:
            try:
                exporter = PDFExporter(resume)
                exporter.export(filepath)
                messagebox.showinfo("Succès", f"CV exporté avec succès ✓\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur d'export", f"Erreur lors de l'export PDF:\n{str(e)}")
    
    def _export_docx(self):
        """Export resume to DOCX."""
        resume = self._collect_form_data()
        
        if not resume.first_name or not resume.last_name:
            messagebox.showwarning("Attention", "Veuillez entrer au moins le nom et le prénom")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx")],
            initialfile=f"{resume.last_name}_{resume.first_name}_CV.docx",
        )
        
        if filepath:
            try:
                exporter = DOCXExporter(resume)
                exporter.export(filepath)
                messagebox.showinfo("Succès", f"CV exporté avec succès ✓\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur d'export", f"Erreur lors de l'export DOCX:\n{str(e)}")
    
    def _save_profile(self):
        """Save current profile to JSON file."""
        resume = self._collect_form_data()
        
        if not resume.first_name or not resume.last_name:
            messagebox.showwarning("Attention", "Veuillez entrer au moins le nom et le prénom")
            return
        
        # Ensure data directory exists
        self.profiles_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing profiles
        profiles = self._load_profiles()
        
        # Add/update current profile
        profile_key = f"{resume.first_name} {resume.last_name}"
        profiles[profile_key] = resume.to_dict()
        
        # Save profiles
        with open(self.profiles_path, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Succès", f"Profil sauvegardé sous: {profile_key}")
    
    def _load_profiles(self) -> dict:
        """Load all profiles from JSON file."""
        if self.profiles_path.exists():
            try:
                with open(self.profiles_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _load_profile(self):
        """Load a profile from JSON file."""
        profiles = self._load_profiles()
        
        if not profiles:
            messagebox.showinfo("Info", "Aucun profil sauvegardé")
            return
        
        # Create selection dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Charger un profil")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Sélectionnez un profil:", font=("", 12, "bold")).pack(pady=10)
        
        listbox_frame = ctk.CTkScrollableFrame(dialog, width=350, height=200)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        def on_select(profile_name):
            data = profiles[profile_name]
            self._populate_forms(data)
            dialog.destroy()
        
        for profile_name in profiles.keys():
            btn = ctk.CTkButton(
                listbox_frame,
                text=profile_name,
                command=lambda name=profile_name: on_select(name),
                width=300,
            )
            btn.pack(fill="x", pady=2)
        
        ctk.CTkButton(dialog, text="Annuler", command=dialog.destroy, width=100).pack(pady=10)
    
    def _populate_forms(self, data: dict):
        """Populate all forms with loaded profile data."""
        # Destroy existing forms
        for widget in self.tab_personal.winfo_children():
            widget.destroy()
        for widget in self.tab_education.winfo_children():
            widget.destroy()
        for widget in self.tab_certifications.winfo_children():
            widget.destroy()
        for widget in self.tab_experience.winfo_children():
            widget.destroy()
        for widget in self.tab_skills.winfo_children():
            widget.destroy()
        
        # Recreate forms
        self.personal_form = PersonalInfoFrame(self.tab_personal)
        self.personal_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.education_form = EducationFrame(self.tab_education)
        self.education_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.certification_form = CertificationFrame(self.tab_certifications)
        self.certification_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.experience_form = ExperienceFrame(self.tab_experience)
        self.experience_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.skills_form = SkillsFrame(self.tab_skills)
        self.skills_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Populate with data
        self.personal_form.set_data(data)
        self.education_form.set_data(data.get("education", []))
        self.certification_form.set_data(data.get("certifications", []))
        self.experience_form.set_data(data.get("experiences", []))
        self.skills_form.set_data({
            "skills_hard": data.get("skills_hard", []),
            "skills_soft": data.get("skills_soft", []),
        })
