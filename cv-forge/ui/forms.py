"""
UI Forms for CV-Forge.
CustomTkinter form components for resume data entry.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, List, Optional

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.resume import Education, Certification, Experience


class PersonalInfoFrame(ctk.CTkFrame):
    """Form for personal information and profile summary."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._build_ui()
    
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        
        # First Name
        ctk.CTkLabel(self, text="Prénom:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = ctk.CTkEntry(self, width=350)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Last Name
        ctk.CTkLabel(self, text="Nom:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = ctk.CTkEntry(self, width=350)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Phone
        ctk.CTkLabel(self, text="Téléphone:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = ctk.CTkEntry(self, width=350)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Email
        ctk.CTkLabel(self, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(self, width=350)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # LinkedIn
        ctk.CTkLabel(self, text="LinkedIn:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.linkedin_entry = ctk.CTkEntry(self, width=350)
        self.linkedin_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # Address
        ctk.CTkLabel(self, text="Adresse:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.address_entry = ctk.CTkEntry(self, width=350)
        self.address_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        # Profile Summary
        ctk.CTkLabel(self, text="Profil:").grid(row=6, column=0, padx=10, pady=5, sticky="ne")
        self.profile_text = ctk.CTkTextbox(self, width=350, height=100)
        self.profile_text.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    
    def get_data(self) -> dict:
        """Get form data as dictionary."""
        return {
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "phone": self.phone_entry.get(),
            "email": self.email_entry.get(),
            "linkedin": self.linkedin_entry.get(),
            "address": self.address_entry.get(),
            "profile": self.profile_text.get("1.0", "end-1c").strip(),
        }
    
    def set_data(self, data: dict):
        """Populate form with data."""
        self.first_name_entry.insert(0, data.get("first_name", ""))
        self.last_name_entry.insert(0, data.get("last_name", ""))
        self.phone_entry.insert(0, data.get("phone", ""))
        self.email_entry.insert(0, data.get("email", ""))
        self.linkedin_entry.insert(0, data.get("linkedin", ""))
        self.address_entry.insert(0, data.get("address", ""))
        self.profile_text.insert("1.0", data.get("profile", ""))


class EducationFrame(ctk.CTkFrame):
    """Form for education entries with add/remove functionality."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.education_entries: List[dict] = []
        self._build_ui()
    
    def _build_ui(self):
        # Entry frame
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.entry_frame, text="Diplôme:").pack(anchor="w", padx=5, pady=2)
        self.diploma_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.diploma_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Établissement:").pack(anchor="w", padx=5, pady=2)
        self.institution_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.institution_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Dates (ex: 2021–2024):").pack(anchor="w", padx=5, pady=2)
        self.dates_entry = ctk.CTkEntry(self.entry_frame, width=200)
        self.dates_entry.pack(anchor="w", padx=5, pady=2)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="Ajouter", command=self._add_entry, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Effacer", command=self._clear_fields, width=100).pack(side="left", padx=5)
        
        # List of added entries
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(self.list_frame, text="Formations ajoutées:", font=("", 11, "bold")).pack(anchor="w")
        self.entries_list = ctk.CTkScrollableFrame(self.list_frame, width=450, height=150)
        self.entries_list.pack(fill="both", expand=True)
    
    def _add_entry(self):
        diploma = self.diploma_entry.get()
        institution = self.institution_entry.get()
        dates = self.dates_entry.get()
        
        if not diploma or not institution:
            messagebox.showwarning("Attention", "Diplôme et Établissement sont requis")
            return
        
        self.education_entries.append({
            "diploma": diploma,
            "institution": institution,
            "dates": dates,
        })
        
        # Add to visual list
        entry_label = ctk.CTkLabel(
            self.entries_list,
            text=f"• {diploma} – {institution} – {dates}",
            anchor="w"
        )
        entry_label.pack(fill="x", pady=2)
        
        self._clear_fields()
    
    def _clear_fields(self):
        self.diploma_entry.delete(0, "end")
        self.institution_entry.delete(0, "end")
        self.dates_entry.delete(0, "end")
    
    def get_data(self) -> List[dict]:
        return self.education_entries
    
    def set_data(self, data: List[dict]):
        self.education_entries = []
        for widget in self.entries_list.winfo_children():
            widget.destroy()
        
        for edu in data:
            self.education_entries.append(edu)
            entry_label = ctk.CTkLabel(
                self.entries_list,
                text=f"• {edu['diploma']} – {edu['institution']} – {edu['dates']}",
                anchor="w"
            )
            entry_label.pack(fill="x", pady=2)


class CertificationFrame(ctk.CTkFrame):
    """Form for certification entries."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.certification_entries: List[dict] = []
        self._build_ui()
    
    def _build_ui(self):
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.entry_frame, text="Nom:").pack(anchor="w", padx=5, pady=2)
        self.name_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.name_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Organisme:").pack(anchor="w", padx=5, pady=2)
        self.org_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.org_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Année:").pack(anchor="w", padx=5, pady=2)
        self.year_entry = ctk.CTkEntry(self.entry_frame, width=150)
        self.year_entry.pack(anchor="w", padx=5, pady=2)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="Ajouter", command=self._add_entry, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Effacer", command=self._clear_fields, width=100).pack(side="left", padx=5)
        
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(self.list_frame, text="Certifications ajoutées:", font=("", 11, "bold")).pack(anchor="w")
        self.entries_list = ctk.CTkScrollableFrame(self.list_frame, width=450, height=150)
        self.entries_list.pack(fill="both", expand=True)
    
    def _add_entry(self):
        name = self.name_entry.get()
        org = self.org_entry.get()
        year = self.year_entry.get()
        
        if not name or not org:
            messagebox.showwarning("Attention", "Nom et Organisme sont requis")
            return
        
        self.certification_entries.append({
            "name": name,
            "organization": org,
            "year": year,
        })
        
        entry_label = ctk.CTkLabel(
            self.entries_list,
            text=f"• {name} – {org} – {year}",
            anchor="w"
        )
        entry_label.pack(fill="x", pady=2)
        
        self._clear_fields()
    
    def _clear_fields(self):
        self.name_entry.delete(0, "end")
        self.org_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
    
    def get_data(self) -> List[dict]:
        return self.certification_entries
    
    def set_data(self, data: List[dict]):
        self.certification_entries = []
        for widget in self.entries_list.winfo_children():
            widget.destroy()
        
        for cert in data:
            self.certification_entries.append(cert)
            entry_label = ctk.CTkLabel(
                self.entries_list,
                text=f"• {cert['name']} – {cert['organization']} – {cert['year']}",
                anchor="w"
            )
            entry_label.pack(fill="x", pady=2)


class ExperienceFrame(ctk.CTkFrame):
    """Form for professional experience entries."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.experience_entries: List[dict] = []
        self._build_ui()
    
    def _build_ui(self):
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.entry_frame, text="Poste:").pack(anchor="w", padx=5, pady=2)
        self.position_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.position_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Entreprise:").pack(anchor="w", padx=5, pady=2)
        self.company_entry = ctk.CTkEntry(self.entry_frame, width=400)
        self.company_entry.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(self.entry_frame, text="Ville:").pack(anchor="w", padx=5, pady=2)
        self.city_entry = ctk.CTkEntry(self.entry_frame, width=200)
        self.city_entry.pack(anchor="w", padx=5, pady=2)
        
        dates_frame = ctk.CTkFrame(self.entry_frame)
        dates_frame.pack(anchor="w", padx=5, pady=2)
        
        ctk.CTkLabel(dates_frame, text="Début (MM/YYYY):").pack(side="left", padx=2)
        self.start_entry = ctk.CTkEntry(dates_frame, width=120)
        self.start_entry.pack(side="left", padx=2)
        
        ctk.CTkLabel(dates_frame, text="Fin (MM/YYYY ou Present):").pack(side="left", padx=2)
        self.end_entry = ctk.CTkEntry(dates_frame, width=150)
        self.end_entry.pack(side="left", padx=2)
        
        ctk.CTkLabel(self.entry_frame, text="Description (une ligne par puce):").pack(anchor="w", padx=5, pady=2)
        self.bullets_text = ctk.CTkTextbox(self.entry_frame, width=450, height=80)
        self.bullets_text.pack(anchor="w", padx=5, pady=2)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="Ajouter", command=self._add_entry, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Effacer", command=self._clear_fields, width=100).pack(side="left", padx=5)
        
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(self.list_frame, text="Expériences ajoutées:", font=("", 11, "bold")).pack(anchor="w")
        self.entries_list = ctk.CTkScrollableFrame(self.list_frame, width=500, height=150)
        self.entries_list.pack(fill="both", expand=True)
    
    def _add_entry(self):
        position = self.position_entry.get()
        company = self.company_entry.get()
        city = self.city_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        bullets_raw = self.bullets_text.get("1.0", "end-1c").strip()
        
        if not position or not company:
            messagebox.showwarning("Attention", "Poste et Entreprise sont requis")
            return
        
        bullets = [b.strip() for b in bullets_raw.split("\n") if b.strip()] if bullets_raw else []
        
        self.experience_entries.append({
            "position": position,
            "company": company,
            "city": city,
            "start_date": start,
            "end_date": end,
            "bullets": bullets,
        })
        
        entry_label = ctk.CTkLabel(
            self.entries_list,
            text=f"• {position} – {company} – {start} à {end}",
            anchor="w",
            wraplength=450,
        )
        entry_label.pack(fill="x", pady=2)
        
        self._clear_fields()
    
    def _clear_fields(self):
        self.position_entry.delete(0, "end")
        self.company_entry.delete(0, "end")
        self.city_entry.delete(0, "end")
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")
        self.bullets_text.delete("1.0", "end")
    
    def get_data(self) -> List[dict]:
        return self.experience_entries
    
    def set_data(self, data: List[dict]):
        self.experience_entries = []
        for widget in self.entries_list.winfo_children():
            widget.destroy()
        
        for exp in data:
            self.experience_entries.append(exp)
            entry_label = ctk.CTkLabel(
                self.entries_list,
                text=f"• {exp['position']} – {exp['company']} – {exp['start_date']} à {exp['end_date']}",
                anchor="w",
                wraplength=450,
            )
            entry_label.pack(fill="x", pady=2)


class SkillsFrame(ctk.CTkFrame):
    """Form for hard and soft skills."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.hard_skills: List[str] = []
        self.soft_skills: List[str] = []
        self._build_ui()
    
    def _build_ui(self):
        # Hard Skills
        hard_frame = ctk.CTkFrame(self)
        hard_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(hard_frame, text="Compétences Techniques:", font=("", 12, "bold")).pack(anchor="w")
        ctk.CTkLabel(hard_frame, text="(une par ligne)").pack(anchor="w")
        
        self.hard_text = ctk.CTkTextbox(hard_frame, width=200, height=200)
        self.hard_text.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkButton(hard_frame, text="Mettre à jour", command=self._update_hard_skills, width=120).pack(pady=5)
        
        self.hard_list_label = ctk.CTkLabel(hard_frame, text="", anchor="w", justify="left")
        self.hard_list_label.pack(anchor="w")
        
        # Soft Skills
        soft_frame = ctk.CTkFrame(self)
        soft_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(soft_frame, text="Compétences Comportementales:", font=("", 12, "bold")).pack(anchor="w")
        ctk.CTkLabel(soft_frame, text="(une par ligne)").pack(anchor="w")
        
        self.soft_text = ctk.CTkTextbox(soft_frame, width=200, height=200)
        self.soft_text.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkButton(soft_frame, text="Mettre à jour", command=self._update_soft_skills, width=120).pack(pady=5)
        
        self.soft_list_label = ctk.CTkLabel(soft_frame, text="", anchor="w", justify="left")
        self.soft_list_label.pack(anchor="w")
    
    def _update_hard_skills(self):
        raw = self.hard_text.get("1.0", "end-1c")
        self.hard_skills = [s.strip() for s in raw.split("\n") if s.strip()]
        self.hard_list_label.configure(text="\n".join([f"• {s}" for s in self.hard_skills]))
    
    def _update_soft_skills(self):
        raw = self.soft_text.get("1.0", "end-1c")
        self.soft_skills = [s.strip() for s in raw.split("\n") if s.strip()]
        self.soft_list_label.configure(text="\n".join([f"• {s}" for s in self.soft_skills]))
    
    def get_data(self) -> dict:
        # Always read from textboxes to get current user input
        hard_raw = self.hard_text.get("1.0", "end-1c")
        soft_raw = self.soft_text.get("1.0", "end-1c")
        
        hard_skills = [s.strip() for s in hard_raw.split("\n") if s.strip()]
        soft_skills = [s.strip() for s in soft_raw.split("\n") if s.strip()]
        
        return {
            "skills_hard": hard_skills,
            "skills_soft": soft_skills,
        }
    
    def set_data(self, data: dict):
        self.hard_skills = data.get("skills_hard", [])
        self.soft_skills = data.get("skills_soft", [])
        
        # Clear textboxes first
        self.hard_text.delete("1.0", "end")
        self.soft_text.delete("1.0", "end")
        
        self.hard_text.insert("1.0", "\n".join(self.hard_skills))
        self.soft_text.insert("1.0", "\n".join(self.soft_skills))
        
        self.hard_list_label.configure(text="\n".join([f"• {s}" for s in self.hard_skills]))
        self.soft_list_label.configure(text="\n".join([f"• {s}" for s in self.soft_skills]))
