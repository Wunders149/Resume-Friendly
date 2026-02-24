"""
Resume data model for CV-Forge.
ATS-friendly structure with clean, scannable sections.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Education:
    """Education entry: Diploma – Institution – Dates"""
    diploma: str = ""
    institution: str = ""
    dates: str = ""


@dataclass
class Certification:
    """Certification entry: Name – Organization – Year"""
    name: str = ""
    organization: str = ""
    year: str = ""


@dataclass
class Experience:
    """Experience entry: Position – Company – City – Dates – Bullets"""
    position: str = ""
    company: str = ""
    city: str = ""
    start_date: str = ""  # MM/YYYY
    end_date: str = ""    # MM/YYYY or "Present"
    bullets: List[str] = field(default_factory=list)


@dataclass
class Resume:
    """
    Complete resume model following ATS-friendly structure.
    
    Sections:
    1. Header (contact info)
    2. Profile/Summary
    3. Education
    4. Certifications
    5. Experience
    6. Skills (Hard & Soft)
    """
    # Personal Info
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    address: str = ""
    
    # Profile Summary
    profile: str = ""
    
    # Sections
    education: List[Education] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    experiences: List[Experience] = field(default_factory=list)
    
    # Skills
    skills_hard: List[str] = field(default_factory=list)
    skills_soft: List[str] = field(default_factory=list)
    
    @property
    def full_name(self) -> str:
        """Return full name in uppercase format (ATS-friendly)."""
        return f"{self.first_name.strip()} {self.last_name.strip()}".upper()
    
    def to_dict(self) -> dict:
        """Convert resume to dictionary for JSON serialization."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "linkedin": self.linkedin,
            "address": self.address,
            "profile": self.profile,
            "education": [
                {"diploma": e.diploma, "institution": e.institution, "dates": e.dates}
                for e in self.education
            ],
            "certifications": [
                {"name": c.name, "organization": c.organization, "year": c.year}
                for c in self.certifications
            ],
            "experiences": [
                {
                    "position": exp.position,
                    "company": exp.company,
                    "city": exp.city,
                    "start_date": exp.start_date,
                    "end_date": exp.end_date,
                    "bullets": exp.bullets,
                }
                for exp in self.experiences
            ],
            "skills_hard": self.skills_hard,
            "skills_soft": self.skills_soft,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Resume":
        """Create Resume instance from dictionary."""
        resume = cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            linkedin=data.get("linkedin", ""),
            address=data.get("address", ""),
            profile=data.get("profile", ""),
        )
        
        for edu in data.get("education", []):
            resume.education.append(Education(**edu))
        
        for cert in data.get("certifications", []):
            resume.certifications.append(Certification(**cert))
        
        for exp in data.get("experiences", []):
            resume.experiences.append(Experience(**exp))
        
        resume.skills_hard = data.get("skills_hard", [])
        resume.skills_soft = data.get("skills_soft", [])
        
        return resume
