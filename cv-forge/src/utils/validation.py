"""
Validation module for CV Forge
Input validation and error handling utilities
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation messages"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"


@dataclass
class ValidationMessage:
    """Represents a validation message"""
    field: str
    message: str
    severity: ValidationSeverity
    code: str = ""


class ResumeValidator:
    """Validate resume data for completeness and correctness"""

    # Email regex pattern
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Phone regex pattern (supports multiple formats)
    PHONE_PATTERN = r'^(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    
    # Required fields
    REQUIRED_FIELDS = ['name', 'contact', 'summary', 'skills', 'experience', 'education']
    
    # Recommended minimum lengths
    MIN_SUMMARY_LENGTH = 50
    MIN_EXPERIENCE_LENGTH = 100
    MIN_SKILLS_COUNT = 3

    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, str]:
        """
        Validate email format
        
        Args:
            email: Email string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        email = email.strip()
        if not re.match(cls.EMAIL_PATTERN, email):
            return False, "Invalid email format"
        
        return True, ""

    @classmethod
    def validate_phone(cls, phone: str) -> Tuple[bool, str]:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone:
            return True, ""  # Phone is optional
        
        phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        if phone and not re.match(r'^\+?\d{7,15}$', phone):
            return False, "Invalid phone number format"
        
        return True, ""

    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, str]:
        """
        Validate name field
        
        Args:
            name: Name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Name is required"
        
        name = name.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if len(name) > 100:
            return False, "Name is too long"
        
        # Check for at least first and last name
        parts = name.split()
        if len(parts) < 2:
            return True, ""  # Warning level, not error
        
        return True, ""

    @classmethod
    def validate_contact(cls, contact: str) -> List[ValidationMessage]:
        """
        Validate contact information
        
        Args:
            contact: Contact information string
            
        Returns:
            List of validation messages
        """
        messages = []
        
        if not contact or not contact.strip():
            messages.append(ValidationMessage(
                field='contact',
                message='Contact information is required',
                severity=ValidationSeverity.ERROR,
                code='CONTACT_REQUIRED'
            ))
            return messages
        
        # Check for email
        emails = re.findall(cls.EMAIL_PATTERN, contact)
        if not emails:
            messages.append(ValidationMessage(
                field='contact',
                message='Add an email address to your contact info',
                severity=ValidationSeverity.WARNING,
                code='NO_EMAIL'
            ))
        
        # Check for phone
        phone_match = re.search(cls.PHONE_PATTERN, contact)
        if not phone_match:
            messages.append(ValidationMessage(
                field='contact',
                message='Consider adding a phone number',
                severity=ValidationSeverity.INFO,
                code='NO_PHONE'
            ))
        
        return messages

    @classmethod
    def validate_summary(cls, summary: str) -> List[ValidationMessage]:
        """
        Validate professional summary
        
        Args:
            summary: Summary text
            
        Returns:
            List of validation messages
        """
        messages = []
        
        if not summary or not summary.strip():
            messages.append(ValidationMessage(
                field='summary',
                message='Professional summary is required',
                severity=ValidationSeverity.ERROR,
                code='SUMMARY_REQUIRED'
            ))
            return messages
        
        word_count = len(summary.split())
        if word_count < 10:
            messages.append(ValidationMessage(
                field='summary',
                message='Summary is too short. Add more detail about your experience.',
                severity=ValidationSeverity.WARNING,
                code='SUMMARY_SHORT'
            ))
        
        if word_count > 100:
            messages.append(ValidationMessage(
                field='summary',
                message='Summary is quite long. Consider condensing to 3-5 sentences.',
                severity=ValidationSeverity.INFO,
                code='SUMMARY_LONG'
            ))
        
        return messages

    @classmethod
    def validate_skills(cls, skills: str) -> List[ValidationMessage]:
        """
        Validate skills section
        
        Args:
            skills: Skills text
            
        Returns:
            List of validation messages
        """
        messages = []
        
        if not skills or not skills.strip():
            messages.append(ValidationMessage(
                field='skills',
                message='Skills section is required',
                severity=ValidationSeverity.ERROR,
                code='SKILLS_REQUIRED'
            ))
            return messages
        
        # Count skills (comma or newline separated)
        skill_list = [s.strip() for s in re.split(r'[,\n]', skills) if s.strip()]
        
        if len(skill_list) < cls.MIN_SKILLS_COUNT:
            messages.append(ValidationMessage(
                field='skills',
                message=f'Add more skills (currently {len(skill_list)}, recommended: {cls.MIN_SKILLS_COUNT}+)',
                severity=ValidationSeverity.WARNING,
                code='SKILLS_FEW'
            ))
        
        return messages

    @classmethod
    def validate_experience(cls, experience: str) -> List[ValidationMessage]:
        """
        Validate experience section
        
        Args:
            experience: Experience text
            
        Returns:
            List of validation messages
        """
        messages = []
        
        if not experience or not experience.strip():
            messages.append(ValidationMessage(
                field='experience',
                message='Professional experience is required',
                severity=ValidationSeverity.ERROR,
                code='EXPERIENCE_REQUIRED'
            ))
            return messages
        
        char_count = len(experience)
        if char_count < cls.MIN_EXPERIENCE_LENGTH:
            messages.append(ValidationMessage(
                field='experience',
                message='Experience section is brief. Add more details about your roles.',
                severity=ValidationSeverity.WARNING,
                code='EXPERIENCE_BRIEF'
            ))
        
        # Check for bullet points or structured format
        if not any(c in experience for c in ['•', '-', '*', '►']):
            messages.append(ValidationMessage(
                field='experience',
                message='Consider using bullet points for better readability',
                severity=ValidationSeverity.INFO,
                code='NO_BULLETS'
            ))
        
        return messages

    @classmethod
    def validate_education(cls, education: str) -> List[ValidationMessage]:
        """
        Validate education section
        
        Args:
            education: Education text
            
        Returns:
            List of validation messages
        """
        messages = []
        
        if not education or not education.strip():
            messages.append(ValidationMessage(
                field='education',
                message='Education section is required',
                severity=ValidationSeverity.ERROR,
                code='EDUCATION_REQUIRED'
            ))
            return messages
        
        # Check for degree keywords
        degree_keywords = ['bachelor', 'master', 'phd', 'bs', 'ms', 'mba', 'degree', 'university', 'college']
        has_degree = any(kw in education.lower() for kw in degree_keywords)
        
        if not has_degree:
            messages.append(ValidationMessage(
                field='education',
                message='Consider adding degree and institution details',
                severity=ValidationSeverity.INFO,
                code='EDUCATION_INCOMPLETE'
            ))
        
        return messages

    @classmethod
    def validate_all(cls, resume_data: Dict) -> List[ValidationMessage]:
        """
        Perform complete validation on resume data
        
        Args:
            resume_data: Dictionary containing all resume fields
            
        Returns:
            List of all validation messages
        """
        all_messages = []
        
        # Validate name
        is_valid, error = cls.validate_name(resume_data.get('name', ''))
        if not is_valid:
            all_messages.append(ValidationMessage(
                field='name',
                message=error,
                severity=ValidationSeverity.ERROR,
                code='NAME_INVALID'
            ))
        
        # Validate contact
        all_messages.extend(cls.validate_contact(resume_data.get('contact', '')))
        
        # Validate summary
        all_messages.extend(cls.validate_summary(resume_data.get('summary', '')))
        
        # Validate skills
        all_messages.extend(cls.validate_skills(resume_data.get('skills', '')))
        
        # Validate experience
        all_messages.extend(cls.validate_experience(resume_data.get('experience', '')))
        
        # Validate education
        all_messages.extend(cls.validate_education(resume_data.get('education', '')))
        
        return all_messages

    @classmethod
    def get_validation_summary(cls, messages: List[ValidationMessage]) -> Dict:
        """
        Get summary of validation results
        
        Args:
            messages: List of validation messages
            
        Returns:
            Dictionary with validation summary
        """
        summary = {
            'is_valid': True,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'success': False,
            'messages_by_field': {}
        }
        
        for msg in messages:
            if msg.severity == ValidationSeverity.ERROR:
                summary['error_count'] += 1
                summary['is_valid'] = False
            elif msg.severity == ValidationSeverity.WARNING:
                summary['warning_count'] += 1
            elif msg.severity == ValidationSeverity.INFO:
                summary['info_count'] += 1
            
            if msg.field not in summary['messages_by_field']:
                summary['messages_by_field'][msg.field] = []
            summary['messages_by_field'][msg.field].append(msg)
        
        if summary['error_count'] == 0 and summary['warning_count'] == 0:
            summary['success'] = True
        
        return summary

    @classmethod
    def can_export(cls, resume_data: Dict) -> Tuple[bool, str]:
        """
        Check if resume can be exported
        
        Args:
            resume_data: Dictionary containing resume fields
            
        Returns:
            Tuple of (can_export, reason)
        """
        # Critical checks
        if not resume_data.get('name', '').strip():
            return False, "Name is required"
        
        if not resume_data.get('contact', '').strip():
            return False, "Contact information is required"
        
        return True, ""


class InputSanitizer:
    """Sanitize and clean input data"""

    @classmethod
    def sanitize_text(cls, text: str, max_length: int = 5000) -> str:
        """
        Sanitize text input
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove control characters except newlines and tabs
        text = ''.join(c for c in text if c.isprintable() or c in '\n\t')
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Trim length
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0]
        
        return text.strip()

    @classmethod
    def sanitize_name(cls, name: str) -> str:
        """
        Sanitize name input
        
        Args:
            name: Input name
            
        Returns:
            Sanitized name
        """
        if not name:
            return ""
        
        # Remove special characters except spaces and hyphens
        name = re.sub(r'[^\w\s\-]', '', name)
        
        # Normalize spaces
        name = ' '.join(name.split())
        
        # Title case
        name = name.title()
        
        return name[:100]

    @classmethod
    def sanitize_email(cls, email: str) -> str:
        """
        Sanitize email input
        
        Args:
            email: Input email
            
        Returns:
            Sanitized email
        """
        if not email:
            return ""
        
        # Lowercase and strip
        email = email.lower().strip()
        
        # Remove spaces
        email = email.replace(' ', '')
        
        return email[:254]

    @classmethod
    def sanitize_phone(cls, phone: str) -> str:
        """
        Sanitize phone number
        
        Args:
            phone: Input phone
            
        Returns:
            Sanitized phone
        """
        if not phone:
            return ""
        
        # Keep only digits and + sign
        phone = re.sub(r'[^\d+]', '', phone)
        
        return phone[:20]
