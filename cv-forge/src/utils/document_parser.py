"""
Document parser module for reading PDF and Word documents
Enhanced with improved section detection using regex patterns
"""
import os
import re
from docx import Document
import pdfplumber
from typing import Dict, Optional, List, Tuple


class DocumentParser:
    """Parse PDF and Word documents with intelligent section detection"""

    # Enhanced section detection patterns
    SECTION_PATTERNS = {
        'contact': [
            r'^contact\s*(info)?\s*$',
            r'^contact\s*details\s*$',
            r'^personal\s*info\s*$',
            r'^personal\s*details\s*$',
        ],
        'summary': [
            r'^(professional\s*)?summary\s*$',
            r'^objective\s*$',
            r'^profile\s*$',
            r'^about\s*(me)?\s*$',
            r'^career\s*objective\s*$',
            r'^professional\s*profile\s*$',
        ],
        'skills': [
            r'^(key\s*)?skills\s*$',
            r'^competencies\s*$',
            r'^technical\s*skills\s*$',
            r'^core\s*competencies\s*$',
            r'^expertise\s*$',
            r'^languages\s*&\s*frameworks\s*$',
        ],
        'experience': [
            r'^(professional\s*|work\s*)?experience\s*$',
            r'^work\s*history\s*$',
            r'^employment\s*history\s*$',
            r'^professional\s*experience\s*$',
            r'^career\s*history\s*$',
            r'^work\s*experience\s*$',
        ],
        'education': [
            r'^education\s*$',
            r'^educational\s*background\s*$',
            r'^academic\s*qualifications\s*$',
            r'^degrees?\s*$',
            r'^universit(y|ies)\s*$',
            r'^academic\s*background\s*$',
        ],
        'certifications': [
            r'^certifications?\s*$',
            r'^licenses?\s*$',
            r'^professional\s*certifications?\s*$',
            r'^credentials?\s*$',
            r'^certificates?\s*$',
        ],
        'projects': [
            r'^projects?\s*$',
            r'^portfolio\s*$',
            r'^key\s*projects?\s*$',
            r'^academic\s*projects?\s*$',
            r'^personal\s*projects?\s*$',
        ],
        'languages': [
            r'^languages?\s*$',
            r'^language\s*skills\s*$',
            r'^spoken\s*languages?\s*$',
        ],
        'references': [
            r'^references?\s*$',
            r'^referees?\s*$',
            r'^references?\s*available\s*upon\s*request\s*$',
        ],
    }

    # Name detection patterns
    NAME_PATTERNS = [
        r'^([A-Z][a-z]+\s+[A-Z][a-z]+)$',  # First Last
        r'^([A-Z][a-z]+\s+[A-Z]\.?\s*[A-Z][a-z]+)$',  # First M. Last
        r'^([A-Z]\.?\s*[A-Z][a-z]+)$',  # Initial Last
    ]

    # Contact info patterns (using non-capturing groups)
    CONTACT_PATTERNS = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        'linkedin': r'linkedin\.com/in/[a-zA-Z0-9_-]+',
        'website': r'(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/\S*)?',
    }

    @staticmethod
    def parse_pdf(pdf_path: str) -> str:
        """
        Extract text from PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text from PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")

        return text.strip()

    @staticmethod
    def parse_docx(docx_path: str) -> str:
        """
        Extract text from Word document

        Args:
            docx_path: Path to Word document

        Returns:
            Extracted text from document
        """
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"Word document not found: {docx_path}")

        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Error reading Word document: {str(e)}")

        return text.strip()

    @staticmethod
    def parse_document(file_path: str) -> str:
        """
        Parse document based on file extension

        Args:
            file_path: Path to document file

        Returns:
            Extracted text from document
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.pdf':
            return DocumentParser.parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return DocumentParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @classmethod
    def extract_sections(cls, text: str) -> Dict[str, str]:
        """
        Extract resume sections from text using enhanced pattern matching

        Args:
            text: Raw text from document

        Returns:
            Dictionary with resume sections
        """
        sections = {
            'contact': '',
            'summary': '',
            'skills': '',
            'experience': '',
            'education': '',
            'certifications': '',
            'projects': '',
            'languages': '',
            'references': '',
        }

        if not text:
            return sections

        lines = text.split('\n')
        current_section = None
        section_start_line = 0
        
        # First pass: identify section headers
        section_boundaries = []  # List of (line_index, section_name)
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()
            
            # Skip empty lines
            if not line_stripped:
                continue
            
            # Check for section headers
            for section_name, patterns in cls.SECTION_PATTERNS.items():
                for pattern in patterns:
                    if re.match(pattern, line_lower, re.IGNORECASE):
                        section_boundaries.append((i, section_name))
                        break
                else:
                    continue
                break
        
        # Second pass: extract content between section boundaries
        for idx, (line_idx, section_name) in enumerate(section_boundaries):
            # Determine end line (next section or end of document)
            if idx + 1 < len(section_boundaries):
                end_line = section_boundaries[idx + 1][0]
            else:
                end_line = len(lines)
            
            # Extract content for this section
            section_content = []
            for j in range(line_idx + 1, end_line):
                section_content.append(lines[j])
            
            sections[section_name] = '\n'.join(section_content).strip()
        
        # If no sections found, try heuristic approach
        if all(not v for v in sections.values()):
            sections = cls._heuristic_extraction(text, lines)
        
        # Extract contact info from entire text if not found
        if not sections['contact']:
            sections['contact'] = cls._extract_contact_info(text)
        
        return sections

    @classmethod
    def _heuristic_extraction(cls, text: str, lines: List[str]) -> Dict[str, str]:
        """
        Fallback heuristic extraction when no clear section headers found
        """
        sections = {
            'contact': '',
            'summary': '',
            'skills': '',
            'experience': '',
            'education': '',
            'certifications': '',
            'projects': '',
            'languages': '',
            'references': '',
        }
        
        # Look for patterns that indicate content type
        in_experience = False
        in_education = False
        in_skills = False
        
        experience_content = []
        education_content = []
        skills_content = []
        summary_content = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            if not line_stripped:
                continue
            
            # Detect experience by company-like patterns
            if re.search(r'@\s*\w+|at\s+\w+|^\d{4}\s*[-–]\s*(\d{4}|present)', line, re.IGNORECASE):
                in_experience = True
                in_education = False
                in_skills = False
            
            # Detect education by degree patterns
            if re.search(r'(bachelor|master|phd|bsc|msc|mba|degree)', line, re.IGNORECASE):
                in_education = True
                in_experience = False
                in_skills = False
            
            # Detect skills by comma-separated or bullet patterns
            if re.search(r'^\s*[-•*]\s*\w+\s*[,;]', line) or len(line_stripped.split(', ')) > 3:
                in_skills = True
                in_experience = False
                in_education = False
            
            # Categorize content
            if in_experience:
                experience_content.append(line)
            elif in_education:
                education_content.append(line)
            elif in_skills:
                skills_content.append(line)
            elif i < 5 and len(line_stripped) < 100:
                # Early short lines might be summary/contact
                summary_content.append(line)
        
        sections['experience'] = '\n'.join(experience_content[:20])
        sections['education'] = '\n'.join(education_content[:10])
        sections['skills'] = '\n'.join(skills_content[:10])
        sections['summary'] = '\n'.join(summary_content[:5])
        
        return sections

    @classmethod
    def _extract_contact_info(cls, text: str) -> str:
        """
        Extract contact information from text using regex patterns
        """
        contact_parts = []

        # Extract email
        emails = re.findall(cls.CONTACT_PATTERNS['email'], text)
        for email in emails[:2]:
            if isinstance(email, tuple):
                contact_parts.append(email[0])
            else:
                contact_parts.append(email)

        # Extract phone
        phones = re.findall(cls.CONTACT_PATTERNS['phone'], text)
        for phone in phones[:2]:
            if isinstance(phone, tuple):
                contact_parts.append(phone[0])
            else:
                contact_parts.append(phone)

        # Extract LinkedIn
        linkedins = re.findall(cls.CONTACT_PATTERNS['linkedin'], text)
        for linkedin in linkedins[:1]:
            if isinstance(linkedin, tuple):
                contact_parts.append(linkedin[0])
            else:
                contact_parts.append(linkedin)

        # Extract websites
        websites = re.findall(cls.CONTACT_PATTERNS['website'], text)
        for website in websites[:1]:
            if isinstance(website, tuple):
                contact_parts.append(website[0])
            else:
                contact_parts.append(website)

        return ' | '.join(contact_parts) if contact_parts else ''

    @classmethod
    def extract_name(cls, text: str) -> str:
        """
        Attempt to extract name from text
        
        Args:
            text: Raw text from document
            
        Returns:
            Extracted name or empty string
        """
        if not text:
            return ''
        
        lines = text.split('\n')
        
        # First non-empty line is often the name
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and len(line_stripped) < 50:
                # Check if it looks like a name
                for pattern in cls.NAME_PATTERNS:
                    if re.match(pattern, line_stripped):
                        return line_stripped
                # Return first short line even if pattern doesn't match
                return line_stripped
        
        return ''

    @classmethod
    def detect_format(cls, text: str) -> Dict[str, any]:
        """
        Detect resume format and provide suggestions
        
        Args:
            text: Raw text from document
            
        Returns:
            Dictionary with format analysis
        """
        analysis = {
            'has_sections': False,
            'section_count': 0,
            'has_contact': False,
            'has_summary': False,
            'has_experience': False,
            'has_education': False,
            'has_skills': False,
            'word_count': 0,
            'suggestions': []
        }
        
        if not text:
            analysis['suggestions'].append("Resume appears to be empty")
            return analysis
        
        sections = cls.extract_sections(text)
        
        analysis['has_sections'] = any(sections.values())
        analysis['section_count'] = sum(1 for v in sections.values() if v)
        analysis['has_contact'] = bool(sections.get('contact'))
        analysis['has_summary'] = bool(sections.get('summary'))
        analysis['has_experience'] = bool(sections.get('experience'))
        analysis['has_education'] = bool(sections.get('education'))
        analysis['has_skills'] = bool(sections.get('skills'))
        analysis['word_count'] = len(text.split())
        
        # Generate suggestions
        if not analysis['has_contact']:
            analysis['suggestions'].append("Add contact information (email, phone)")
        if not analysis['has_summary']:
            analysis['suggestions'].append("Add a professional summary")
        if not analysis['has_skills']:
            analysis['suggestions'].append("Add a skills section")
        if not analysis['has_experience']:
            analysis['suggestions'].append("Add work experience")
        if not analysis['has_education']:
            analysis['suggestions'].append("Add education details")
        if analysis['word_count'] < 200:
            analysis['suggestions'].append("Consider adding more detail to your resume")
        elif analysis['word_count'] > 1000:
            analysis['suggestions'].append("Consider condensing your resume to 1-2 pages")
        
        return analysis
