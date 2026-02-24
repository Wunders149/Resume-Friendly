"""
PDF Exporter for CV-Forge.
Generates ATS-friendly PDF documents using reportlab.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

from models.resume import Resume


class PDFExporter:
    """Export Resume to ATS-friendly PDF format."""
    
    def __init__(self, resume: Resume):
        self.resume = resume
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure styles for ATS-compatible PDF."""
        font_name = 'Helvetica'  # Default fallback
        
        # Normal text style
        self.styles['Normal'].fontName = font_name
        self.styles['Normal'].fontSize = 11
        
        # Section title style
        if 'SectionTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionTitle',
                parent=self.styles['Heading2'],
                fontName=font_name,
                fontSize=12,
                textColor=colors.black,
                spaceBefore=12,
                spaceAfter=6,
                textTransform='uppercase',
            ))
        
        # Header name style
        if 'HeaderName' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='HeaderName',
                parent=self.styles['Heading1'],
                fontName=font_name,
                fontSize=16,
                alignment=1,  # Center
                spaceAfter=6,
            ))
        
        # Contact info style
        if 'ContactInfo' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ContactInfo',
                parent=self.styles['Normal'],
                fontName=font_name,
                fontSize=10,
                alignment=1,  # Center
                spaceAfter=12,
            ))
        
        # Bullet style
        if 'CustomBullet' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBullet',
                parent=self.styles['Normal'],
                fontName=font_name,
                fontSize=11,
                leftIndent=20,
                spaceAfter=3,
            ))
    
    def export(self, filepath: str) -> None:
        """Export the resume to a PDF file."""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                leftMargin=0.75 * inch,
                rightMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch,
            )
            
            story = []
            
            self._build_header(story)
            self._build_profile(story)
            self._build_education(story)
            self._build_certifications(story)
            self._build_experiences(story)
            self._build_skills(story)
            
            doc.build(story)
        except PermissionError:
            raise Exception(f"Accès refusé: Impossible d'écrire le fichier {filepath}")
        except IOError as e:
            raise Exception(f"Erreur d'entrée/sortie: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du PDF: {str(e)}")
    
    def _build_header(self, story: list) -> None:
        """Add resume header with contact information."""
        story.append(Paragraph(self.resume.full_name, self.styles['HeaderName']))
        
        contact_lines = []
        if self.resume.phone:
            contact_lines.append(self.resume.phone)
        if self.resume.email:
            contact_lines.append(self.resume.email)
        if self.resume.linkedin:
            contact_lines.append(self.resume.linkedin)
        if self.resume.address:
            contact_lines.append(self.resume.address)
        
        if contact_lines:
            contact_text = " | ".join(contact_lines)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 0.15 * inch))
    
    def _build_profile(self, story: list) -> None:
        """Add profile/summary section."""
        if not self.resume.profile:
            return
        
        story.append(Paragraph("PROFIL", self.styles['SectionTitle']))
        story.append(Paragraph(self.resume.profile, self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
    
    def _build_education(self, story: list) -> None:
        """Add education section."""
        if not self.resume.education:
            return
        
        story.append(Paragraph("FORMATION", self.styles['SectionTitle']))
        
        for edu in self.resume.education:
            edu_text = f"{edu.diploma} – {edu.institution} – {edu.dates}"
            story.append(Paragraph(edu_text, self.styles['Normal']))
            story.append(Spacer(1, 4))
        
        story.append(Spacer(1, 0.1 * inch))
    
    def _build_certifications(self, story: list) -> None:
        """Add certifications section."""
        if not self.resume.certifications:
            return
        
        story.append(Paragraph("CERTIFICATION", self.styles['SectionTitle']))
        
        for cert in self.resume.certifications:
            cert_text = f"{cert.name} – {cert.organization} – {cert.year}"
            story.append(Paragraph(cert_text, self.styles['Normal']))
            story.append(Spacer(1, 4))
        
        story.append(Spacer(1, 0.1 * inch))
    
    def _build_experiences(self, story: list) -> None:
        """Add experience section."""
        if not self.resume.experiences:
            return
        
        story.append(Paragraph("EXPERIENCES PROFESSIONNELLES", self.styles['SectionTitle']))
        
        for exp in self.resume.experiences:
            dates_range = f"{exp.start_date} – {exp.end_date}"
            exp_header = f"{exp.position} – {exp.company} – {exp.city} – {dates_range}"
            
            job_story = [Paragraph(exp_header, self.styles['Normal'])]
            
            for bullet in exp.bullets:
                job_story.append(Paragraph(f"• {bullet}", self.styles['CustomBullet']))
            
            story.append(KeepTogether(job_story))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 0.1 * inch))
    
    def _build_skills(self, story: list) -> None:
        """Add skills section."""
        has_skills = self.resume.skills_hard or self.resume.skills_soft
        if not has_skills:
            return
        
        story.append(Paragraph("COMPETENCES", self.styles['SectionTitle']))
        
        if self.resume.skills_hard:
            skills_text = "<b>Competences Techniques:</b><br/>"
            skills_text += "<br/>".join([f"• {skill}" for skill in self.resume.skills_hard])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        if self.resume.skills_soft:
            skills_text = "<b>Competences Comportementales:</b><br/>"
            skills_text += "<br/>".join([f"• {skill}" for skill in self.resume.skills_soft])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
