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
        # Create scrollable frame for better UX
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            scroll_frame,
            text="Informations Personnelles",
            font=("Helvetica", 14, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        current_row = 1
        
        # First Name
        ctk.CTkLabel(
            scroll_frame,
            text="👤 Prénom:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.first_name_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: Jean")
        self.first_name_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # Last Name
        ctk.CTkLabel(
            scroll_frame,
            text="Nom:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.last_name_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: Dupont")
        self.last_name_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # Phone
        ctk.CTkLabel(
            scroll_frame,
            text="☎️ Téléphone:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.phone_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: +33 1 23 45 67 89")
        self.phone_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # Email
        ctk.CTkLabel(
            scroll_frame,
            text="✉️ Email:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.email_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: jean@example.com")
        self.email_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # LinkedIn
        ctk.CTkLabel(
            scroll_frame,
            text="🔗 LinkedIn:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.linkedin_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: linkedin.com/in/jean")
        self.linkedin_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # Address
        ctk.CTkLabel(
            scroll_frame,
            text="📍 Adresse:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
        self.address_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Ex: Paris, France")
        self.address_entry.grid(row=current_row, column=1, padx=10, pady=8, sticky="ew")
        current_row += 1
        
        # Profile Summary with better layout
        ctk.CTkLabel(
            scroll_frame,
            text="📝 Profil:",
            font=("Helvetica", 11)
        ).grid(row=current_row, column=0, padx=10, pady=(15, 5), sticky="ne")
        
        profile_container = ctk.CTkFrame(scroll_frame)
        profile_container.grid(row=current_row, column=1, padx=10, pady=(15, 8), sticky="ew")
        profile_container.grid_columnconfigure(0, weight=1)
        
        self.profile_text = ctk.CTkTextbox(profile_container, height=100)
        self.profile_text.pack(fill="both", expand=True)
        
        hint = ctk.CTkLabel(
            profile_container,
            text="💡 Accroche courte (2-3 lignes) décrivant votre profil",
            font=("Helvetica", 9),
            text_color="gray"
        )
        hint.pack(fill="x", pady=(5, 0))
    
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
        # Main scrollable frame
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.pack(fill="both", expand=True)
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            main_scroll,
            text="🎓 Formations",
            font=("Helvetica", 14, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 15), padx=10)
        
        # Entry frame with border
        entry_frame_container = ctk.CTkFrame(main_scroll)
        entry_frame_container.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        entry_frame_container.grid_columnconfigure(0, weight=1)
        
        self.entry_frame = ctk.CTkFrame(entry_frame_container)
        self.entry_frame.pack(fill="x", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        
        # Diplôme
        ctk.CTkLabel(self.entry_frame, text="Diplôme:", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.diploma_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: Master en Informatique")
        self.diploma_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=8)
        
        # Établissement
        ctk.CTkLabel(self.entry_frame, text="Établissement:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.institution_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: Université de Paris")
        self.institution_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=8)
        
        # Dates
        ctk.CTkLabel(self.entry_frame, text="Dates:", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        self.dates_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: 2021–2024")
        self.dates_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=8)
        
        # Buttons
        btn_frame = ctk.CTkFrame(entry_frame_container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="✚ Ajouter",
            command=self._add_entry,
            width=120,
            fg_color="#27ae60",
            hover_color="#229954",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Effacer",
            command=self._clear_fields,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        # List of added entries with title
        list_title = ctk.CTkLabel(
            main_scroll,
            text="✓ Formations ajoutées",
            font=("Helvetica", 12, "bold")
        )
        list_title.grid(row=2, column=0, sticky="w", pady=(10, 8), padx=10)
        
        self.entries_list = ctk.CTkScrollableFrame(main_scroll, height=200)
        self.entries_list.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.entries_list.grid_columnconfigure(0, weight=1)
    
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
        
        # Add to visual list with better styling
        entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
        entry_container.pack(fill="x", pady=4)
        entry_container.grid_columnconfigure(0, weight=1)
        
        text = f"📚 {diploma}\n   📍 {institution} • {dates}"
        entry_label = ctk.CTkLabel(
            entry_container,
            text=text,
            anchor="w",
            justify="left",
            font=("Helvetica", 10)
        )
        entry_label.pack(fill="x", padx=10, pady=8)
        
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
            entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
            entry_container.pack(fill="x", pady=4)
            entry_container.grid_columnconfigure(0, weight=1)
            
            text = f"📚 {edu['diploma']}\n   📍 {edu['institution']} • {edu['dates']}"
            entry_label = ctk.CTkLabel(
                entry_container,
                text=text,
                anchor="w",
                justify="left",
                font=("Helvetica", 10)
            )
            entry_label.pack(fill="x", padx=10, pady=8)


class CertificationFrame(ctk.CTkFrame):
    """Form for certification entries."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.certification_entries: List[dict] = []
        self._build_ui()
    
    def _build_ui(self):
        # Main scrollable frame
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.pack(fill="both", expand=True)
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            main_scroll,
            text="🏆 Certifications",
            font=("Helvetica", 14, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 15), padx=10)
        
        # Entry frame with border
        entry_frame_container = ctk.CTkFrame(main_scroll)
        entry_frame_container.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        entry_frame_container.grid_columnconfigure(0, weight=1)
        
        self.entry_frame = ctk.CTkFrame(entry_frame_container)
        self.entry_frame.pack(fill="x", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        
        # Nom
        ctk.CTkLabel(self.entry_frame, text="Nom:", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.name_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: AWS Certified Solutions Architect")
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=8)
        
        # Organisme
        ctk.CTkLabel(self.entry_frame, text="Organisme:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.org_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: Amazon Web Services")
        self.org_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=8)
        
        # Année
        ctk.CTkLabel(self.entry_frame, text="Année:", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        self.year_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: 2023")
        self.year_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=8)
        
        # Buttons
        btn_frame = ctk.CTkFrame(entry_frame_container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="✚ Ajouter",
            command=self._add_entry,
            width=120,
            fg_color="#27ae60",
            hover_color="#229954",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Effacer",
            command=self._clear_fields,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        # List of added entries
        list_title = ctk.CTkLabel(
            main_scroll,
            text="✓ Certifications ajoutées",
            font=("Helvetica", 12, "bold")
        )
        list_title.grid(row=2, column=0, sticky="w", pady=(10, 8), padx=10)
        
        self.entries_list = ctk.CTkScrollableFrame(main_scroll, height=200)
        self.entries_list.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.entries_list.grid_columnconfigure(0, weight=1)
    
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
        
        entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
        entry_container.pack(fill="x", pady=4)
        entry_container.grid_columnconfigure(0, weight=1)
        
        text = f"🎖️ {name}\n   🏢 {org} • {year}"
        entry_label = ctk.CTkLabel(
            entry_container,
            text=text,
            anchor="w",
            justify="left",
            font=("Helvetica", 10)
        )
        entry_label.pack(fill="x", padx=10, pady=8)
        
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
            entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
            entry_container.pack(fill="x", pady=4)
            entry_container.grid_columnconfigure(0, weight=1)
            
            text = f"🎖️ {cert['name']}\n   🏢 {cert['organization']} • {cert['year']}"
            entry_label = ctk.CTkLabel(
                entry_container,
                text=text,
                anchor="w",
                justify="left",
                font=("Helvetica", 10)
            )
            entry_label.pack(fill="x", padx=10, pady=8)


class ExperienceFrame(ctk.CTkFrame):
    """Form for professional experience entries."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.experience_entries: List[dict] = []
        self._build_ui()
    
    def _build_ui(self):
        # Main scrollable frame
        main_scroll = ctk.CTkScrollableFrame(self)
        main_scroll.pack(fill="both", expand=True)
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            main_scroll,
            text="💼 Expériences Professionnelles",
            font=("Helvetica", 14, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 15), padx=10)
        
        # Entry frame with border
        entry_frame_container = ctk.CTkFrame(main_scroll)
        entry_frame_container.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        entry_frame_container.grid_columnconfigure(0, weight=1)
        
        self.entry_frame = ctk.CTkFrame(entry_frame_container)
        self.entry_frame.pack(fill="x", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Poste
        ctk.CTkLabel(self.entry_frame, text="Poste:", font=("Helvetica", 10)).grid(row=current_row, column=0, sticky="w", padx=5, pady=8)
        self.position_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: Développeur Senior")
        self.position_entry.grid(row=current_row, column=1, sticky="ew", padx=5, pady=8)
        current_row += 1
        
        # Entreprise
        ctk.CTkLabel(self.entry_frame, text="Entreprise:", font=("Helvetica", 10)).grid(row=current_row, column=0, sticky="w", padx=5, pady=8)
        self.company_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: TechCorp")
        self.company_entry.grid(row=current_row, column=1, sticky="ew", padx=5, pady=8)
        current_row += 1
        
        # Ville
        ctk.CTkLabel(self.entry_frame, text="Ville:", font=("Helvetica", 10)).grid(row=current_row, column=0, sticky="w", padx=5, pady=8)
        self.city_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Ex: Paris")
        self.city_entry.grid(row=current_row, column=1, sticky="ew", padx=5, pady=8)
        current_row += 1
        
        # Dates
        dates_label = ctk.CTkLabel(self.entry_frame, text="Dates:", font=("Helvetica", 10))
        dates_label.grid(row=current_row, column=0, sticky="w", padx=5, pady=8)
        
        dates_frame = ctk.CTkFrame(self.entry_frame)
        dates_frame.grid(row=current_row, column=1, sticky="ew", padx=5, pady=8)
        dates_frame.grid_columnconfigure(0, weight=1)
        dates_frame.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(dates_frame, text="Début:", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w")
        self.start_entry = ctk.CTkEntry(dates_frame, placeholder_text="MM/YYYY")
        self.start_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        ctk.CTkLabel(dates_frame, text="Fin:", font=("Helvetica", 9)).grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.end_entry = ctk.CTkEntry(dates_frame, placeholder_text="MM/YYYY ou Present")
        self.end_entry.grid(row=0, column=3, sticky="ew", padx=5)
        current_row += 1
        
        # Descriptions
        ctk.CTkLabel(self.entry_frame, text="Descriptions:", font=("Helvetica", 10)).grid(row=current_row, column=0, sticky="w", padx=5, pady=(8, 0))
        hint = ctk.CTkLabel(self.entry_frame, text="(une ligne = une puce)", font=("Helvetica", 8), text_color="gray")
        hint.grid(row=current_row, column=1, sticky="w", padx=5, pady=(8, 0))
        current_row += 1
        
        self.bullets_text = ctk.CTkTextbox(self.entry_frame, height=80)
        self.bullets_text.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=5, pady=8)
        current_row += 1
        
        # Buttons
        btn_frame = ctk.CTkFrame(entry_frame_container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="✚ Ajouter",
            command=self._add_entry,
            width=120,
            fg_color="#27ae60",
            hover_color="#229954",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Effacer",
            command=self._clear_fields,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Helvetica", 10)
        ).pack(side="left", padx=2)
        
        # List of added entries
        list_title = ctk.CTkLabel(
            main_scroll,
            text="✓ Expériences ajoutées",
            font=("Helvetica", 12, "bold")
        )
        list_title.grid(row=2, column=0, sticky="w", pady=(10, 8), padx=10)
        
        self.entries_list = ctk.CTkScrollableFrame(main_scroll, height=200)
        self.entries_list.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.entries_list.grid_columnconfigure(0, weight=1)
    
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
        
        entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
        entry_container.pack(fill="x", pady=4)
        entry_container.grid_columnconfigure(0, weight=1)
        
        dates_str = f"{start} → {end}" if start and end else "Dates non spécifiées"
        text = f"🏢 {position} • {company}\n   📍 {city} | {dates_str}"
        entry_label = ctk.CTkLabel(
            entry_container,
            text=text,
            anchor="w",
            justify="left",
            font=("Helvetica", 10)
        )
        entry_label.pack(fill="x", padx=10, pady=8)
        
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
            entry_container = ctk.CTkFrame(self.entries_list, fg_color="gray25")
            entry_container.pack(fill="x", pady=4)
            entry_container.grid_columnconfigure(0, weight=1)
            
            dates_str = f"{exp['start_date']} → {exp['end_date']}"
            text = f"🏢 {exp['position']} • {exp['company']}\n   📍 {exp['city']} | {dates_str}"
            entry_label = ctk.CTkLabel(
                entry_container,
                text=text,
                anchor="w",
                justify="left",
                font=("Helvetica", 10)
            )
            entry_label.pack(fill="x", padx=10, pady=8)


class SkillsFrame(ctk.CTkFrame):
    """Form for hard and soft skills."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.hard_skills: List[str] = []
        self.soft_skills: List[str] = []
        self._build_ui()
    
    def _build_ui(self):
        # Main container with two columns
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Hard Skills (Left side)
        hard_frame = ctk.CTkFrame(container)
        hard_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        hard_frame.grid_rowconfigure(2, weight=1)
        hard_frame.grid_columnconfigure(0, weight=1)
        
        hard_title = ctk.CTkLabel(
            hard_frame,
            text="⚙️ Compétences Techniques",
            font=("Helvetica", 12, "bold")
        )
        hard_title.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        hint_hard = ctk.CTkLabel(
            hard_frame,
            text="(une par ligne: Python, Docker, AWS...)",
            font=("Helvetica", 9),
            text_color="gray"
        )
        hint_hard.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
        
        self.hard_text = ctk.CTkTextbox(hard_frame)
        self.hard_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 8))
        
        hard_btn_frame = ctk.CTkFrame(hard_frame, fg_color="transparent")
        hard_btn_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            hard_btn_frame,
            text="✓ Mettre à jour",
            command=self._update_hard_skills,
            width=150,
            fg_color="#27ae60",
            hover_color="#229954",
            font=("Helvetica", 10)
        ).pack(fill="x")
        
        self.hard_list_label = ctk.CTkLabel(
            hard_frame,
            text="",
            anchor="w",
            justify="left",
            font=("Helvetica", 9)
        )
        self.hard_list_label.grid(row=4, column=0, sticky="w", padx=10, pady=(5, 0))
        
        # Soft Skills (Right side)
        soft_frame = ctk.CTkFrame(container)
        soft_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        soft_frame.grid_rowconfigure(2, weight=1)
        soft_frame.grid_columnconfigure(0, weight=1)
        
        soft_title = ctk.CTkLabel(
            soft_frame,
            text="👥 Compétences Comportementales",
            font=("Helvetica", 12, "bold")
        )
        soft_title.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        hint_soft = ctk.CTkLabel(
            soft_frame,
            text="(une par ligne: Leadership, Communication...)",
            font=("Helvetica", 9),
            text_color="gray"
        )
        hint_soft.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
        
        self.soft_text = ctk.CTkTextbox(soft_frame)
        self.soft_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 8))
        
        soft_btn_frame = ctk.CTkFrame(soft_frame, fg_color="transparent")
        soft_btn_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            soft_btn_frame,
            text="✓ Mettre à jour",
            command=self._update_soft_skills,
            width=150,
            fg_color="#27ae60",
            hover_color="#229954",
            font=("Helvetica", 10)
        ).pack(fill="x")
        
        self.soft_list_label = ctk.CTkLabel(
            soft_frame,
            text="",
            anchor="w",
            justify="left",
            font=("Helvetica", 9)
        )
        self.soft_list_label.grid(row=4, column=0, sticky="w", padx=10, pady=(5, 0))
    
    def _update_hard_skills(self):
        raw = self.hard_text.get("1.0", "end-1c")
        self.hard_skills = [s.strip() for s in raw.split("\n") if s.strip()]
        display = "\n".join([f"✓ {s}" for s in self.hard_skills]) if self.hard_skills else "Aucune compétence ajoutée"
        self.hard_list_label.configure(text=display)
    
    def _update_soft_skills(self):
        raw = self.soft_text.get("1.0", "end-1c")
        self.soft_skills = [s.strip() for s in raw.split("\n") if s.strip()]
        display = "\n".join([f"✓ {s}" for s in self.soft_skills]) if self.soft_skills else "Aucune compétence ajoutée"
        self.soft_list_label.configure(text=display)
    
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
        
        hard_display = "\n".join([f"✓ {s}" for s in self.hard_skills]) if self.hard_skills else "Aucune compétence"
        soft_display = "\n".join([f"✓ {s}" for s in self.soft_skills]) if self.soft_skills else "Aucune compétence"
        
        self.hard_list_label.configure(text=hard_display)
        self.soft_list_label.configure(text=soft_display)
