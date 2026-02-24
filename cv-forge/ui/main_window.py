"""
Main Window for CV-Forge.
CustomTkinter tabbed interface for resume building.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
from pathlib import Path

import sys
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.resume import Resume
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
        self.geometry("900x700")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.resume = Resume()
        self.profiles_path = Path(__file__).parent.parent / "data" / "profiles.json"
        
        self._build_ui()
        self._load_profiles()
    
    def _build_ui(self):
        """Build the main UI with tabs and action buttons."""
        # Tab view
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab_personal = self.tabview.add("Informations personnelles")
        self.tab_education = self.tabview.add("Formation")
        self.tab_certifications = self.tabview.add("Certifications")
        self.tab_experience = self.tabview.add("Expériences")
        self.tab_skills = self.tabview.add("Compétences")
        
        # Add forms to tabs
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
        
        # Action buttons frame
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Left side buttons
        left_frame = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=10)
        
        ctk.CTkButton(
            left_frame,
            text="Sauvegarder Profil",
            command=self._save_profile,
            width=150,
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            left_frame,
            text="Charger Profil",
            command=self._load_profile,
            width=150,
        ).pack(side="left", padx=5)
        
        # Right side buttons (export)
        right_frame = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=10)
        
        ctk.CTkButton(
            right_frame,
            text="Exporter PDF",
            command=self._export_pdf,
            width=150,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text="Exporter DOCX",
            command=self._export_docx,
            width=150,
            fg_color="#3498db",
            hover_color="#2980b9",
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
        
        from models.resume import Education, Certification, Experience
        
        for edu in education_data:
            self.resume.education.append(Education(**edu))
        
        for cert in certifications_data:
            self.resume.certifications.append(Certification(**cert))
        
        for exp in experiences_data:
            self.resume.experiences.append(Experience(**exp))
        
        self.resume.skills_hard = skills_data["skills_hard"]
        self.resume.skills_soft = skills_data["skills_soft"]
        
        return self.resume
    
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
                messagebox.showinfo("Succès", f"CV exporté avec succès:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export PDF:\n{str(e)}")
    
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
                messagebox.showinfo("Succès", f"CV exporté avec succès:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export DOCX:\n{str(e)}")
    
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
        # Clear existing entries
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
