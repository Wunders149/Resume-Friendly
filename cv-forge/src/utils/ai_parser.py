"""
AI-powered resume parser using LLM APIs
Supports free and paid APIs: Ollama (local), Google Gemini (free tier), 
Hugging Face (free), OpenAI, and LM Studio
"""
import os
import json
import re
from typing import Dict, Optional, List, Any
from pathlib import Path


class AIParser:
    """AI-powered resume parser for intelligent information extraction"""

    # API endpoints
    API_ENDPOINTS = {
        'ollama': 'http://localhost:11434/api/chat',
        'lmstudio': 'http://localhost:1234/v1/chat/completions',
        'gemini': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        'huggingface': 'https://api-inference.huggingface.co/models',
        'openai': 'https://api.openai.com/v1/chat/completions',
    }

    # Default free model on Hugging Face
    DEFAULT_HF_MODEL = 'mistralai/Mistral-7B-Instruct-v0.3'

    # System prompt for resume parsing
    SYSTEM_PROMPT = """You are an expert resume parser. Extract information from the resume text and return it as a JSON object.

Extract the following fields:
- name: The person's full name
- title: Professional title/headline (e.g., "Software Engineer", "Project Manager")
- contact: Contact information (email, phone, location, LinkedIn, website) - combine into one string with | separator
- summary: Professional summary or objective statement
- skills: List of skills (combine into comma-separated string)
- experience: Work experience (format as plain text with job titles, companies, dates, and bullet points)
- education: Education details (degrees, institutions, graduation years)
- certifications: Certifications and licenses
- projects: Notable projects
- languages: Languages spoken
- references: References information

Return ONLY valid JSON. If a field is not found, use an empty string "".

Example output:
{
    "name": "John Doe",
    "title": "Senior Software Engineer",
    "contact": "john@email.com | +1-555-123-4567 | New York, NY | linkedin.com/in/johndoe",
    "summary": "Experienced software engineer with 5+ years...",
    "skills": "Python, Java, React, Node.js, AWS, Docker",
    "experience": "Senior Software Engineer | Tech Corp | 2020-Present\n• Led development of...",
    "education": "B.S. Computer Science | University Name | 2018",
    "certifications": "AWS Certified Solutions Architect",
    "projects": "E-commerce Platform - Built using React and Node.js",
    "languages": "English (Native), Spanish (Fluent)",
    "references": "Available upon request"
}"""

    def __init__(self, api_key: Optional[str] = None, provider: str = 'gemini', 
                 model: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Initialize AI parser

        Args:
            api_key: API key for the service (optional for local models)
            provider: API provider ('gemini', 'huggingface', 'ollama', 'lmstudio', 'openai')
            model: Model name to use
            endpoint: Custom API endpoint (optional)
        """
        self.api_key = api_key or os.environ.get('AI_API_KEY', '')
        self.provider = provider
        self.model = model
        self.endpoint = endpoint or self.API_ENDPOINTS.get(provider, '')
        
        # Set default models for free providers
        if provider == 'gemini' and not model:
            self.model = 'gemini-1.5-flash'
        elif provider == 'huggingface' and not model:
            self.model = self.DEFAULT_HF_MODEL
        elif provider == 'ollama' and not model:
            self.model = 'llama3.2'
        elif provider == 'lmstudio' and not model:
            self.model = 'local-model'
        elif provider == 'openai' and not model:
            self.model = 'gpt-3.5-turbo'
        
        # Try to load config from file
        self._load_config()

    def _load_config(self):
        """Load AI config from file if exists"""
        config_file = Path.home() / '.cvforge' / 'ai_config.json'
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key', self.api_key)
                    self.provider = config.get('provider', self.provider)
                    self.model = config.get('model', self.model)
                    self.endpoint = config.get('endpoint', self.endpoint)
            except Exception:
                pass

    def save_config(self):
        """Save AI config to file"""
        config_file = Path.home() / '.cvforge' / 'ai_config.json'
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'api_key': self.api_key,
            'provider': self.provider,
            'model': self.model,
            'endpoint': self.endpoint
        }
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass

    def parse_resume(self, text: str) -> Dict[str, str]:
        """
        Parse resume text using AI

        Args:
            text: Raw resume text

        Returns:
            Dictionary with extracted resume fields
        """
        if not text or len(text.strip()) < 50:
            return self._empty_result()

        try:
            # Call the appropriate API
            if self.provider == 'ollama':
                result = self._call_ollama(text)
            elif self.provider == 'gemini':
                result = self._call_gemini(text)
            elif self.provider == 'huggingface':
                result = self._call_huggingface(text)
            elif self.provider == 'lmstudio':
                result = self._call_lmstudio(text)
            elif self.provider == 'openai':
                result = self._call_openai(text)
            else:
                result = self._call_custom(text)

            # Parse the JSON response
            return self._parse_ai_response(result)

        except Exception as e:
            print(f"AI parsing error: {str(e)}")
            return self._empty_result()

    def _empty_result(self) -> Dict[str, str]:
        """Return empty result dictionary"""
        return {
            'name': '',
            'title': '',
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

    def _call_gemini(self, text: str) -> str:
        """Call Google Gemini API (free tier)"""
        import requests

        if not self.api_key:
            raise ValueError("Gemini API key required. Get free key at: https://makersuite.google.com/app/apikey")

        url = self.API_ENDPOINTS['gemini'].replace('gemini-1.5-flash', self.model or 'gemini-1.5-flash')
        
        payload = {
            'contents': [{
                'parts': [{
                    'text': f"{self.SYSTEM_PROMPT}\n\nParse this resume:\n\n{text}"
                }]
            }],
            'generationConfig': {
                'temperature': 0.1,
                'maxOutputTokens': 2000
            }
        }

        response = requests.post(url, json=payload, params={'key': self.api_key}, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

    def _call_huggingface(self, text: str) -> str:
        """Call Hugging Face Inference API (free tier)"""
        import requests

        if not self.api_key:
            raise ValueError("Hugging Face API key required. Get free key at: https://huggingface.co/settings/tokens")

        model = self.model or self.DEFAULT_HF_MODEL
        url = f"{self.API_ENDPOINTS['huggingface']}/{model}"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Format prompt for instruction-tuned models
        prompt = f"<s>[INST] {self.SYSTEM_PROMPT}\n\nParse this resume:\n\n{text} [/INST]"
        
        payload = {
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': 1500,
                'temperature': 0.1,
                'return_full_text': False
            }
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        # Handle different response formats
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('generated_text', '')
        elif isinstance(data, dict):
            return data.get('generated_text', '')
        
        return str(data)

    def _call_ollama(self, text: str) -> str:
        """Call Ollama local API (free)"""
        import requests

        payload = {
            'model': self.model or 'llama3.2',
            'messages': [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Parse this resume:\n\n{text}'}
            ],
            'stream': False,
            'options': {
                'temperature': 0.1,
                'num_predict': 2000
            }
        }

        response = requests.post(self.endpoint or self.API_ENDPOINTS['ollama'], json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        return data.get('message', {}).get('content', '')

    def _call_openai(self, text: str) -> str:
        """Call OpenAI API (paid)"""
        import requests

        if not self.api_key:
            raise ValueError("OpenAI API key required")

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model or 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Parse this resume:\n\n{text}'}
            ],
            'temperature': 0.1,
            'max_tokens': 2000
        }

        response = requests.post(self.endpoint or self.API_ENDPOINTS['openai'], headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        return data.get('choices', [{}])[0].get('message', {}).get('content', '')

    def _call_lmstudio(self, text: str) -> str:
        """Call LM Studio local API (free)"""
        import requests

        headers = {
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model or 'local-model',
            'messages': [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Parse this resume:\n\n{text}'}
            ],
            'temperature': 0.1,
            'max_tokens': 2000
        }

        response = requests.post(self.endpoint or self.API_ENDPOINTS['lmstudio'], headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        return data.get('choices', [{}])[0].get('message', {}).get('content', '')

    def _call_custom(self, text: str) -> str:
        """Call custom API endpoint"""
        import requests

        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Parse this resume:\n\n{text}'}
            ],
            'temperature': 0.1,
            'max_tokens': 2000
        }

        response = requests.post(self.endpoint, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Try to extract content from various response formats
        if 'choices' in data:
            return data['choices'][0].get('message', {}).get('content', '')
        elif 'message' in data:
            return data['message'].get('content', '')
        elif 'content' in data:
            return data['content']
        
        return str(data)

    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """Parse AI response to extract JSON"""
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                # Map to expected format
                result = self._empty_result()
                for key in result.keys():
                    value = parsed.get(key, '')
                    if isinstance(value, list):
                        value = ', '.join(str(v) for v in value)
                    result[key] = str(value) if value else ''
                return result
            except json.JSONDecodeError:
                pass

        # Fallback: try to extract fields using regex
        return self._extract_fields_fallback(response)

    def _extract_fields_fallback(self, text: str) -> Dict[str, str]:
        """Fallback field extraction using regex"""
        result = self._empty_result()
        
        # Try to extract common patterns
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        if emails or phones:
            contact_parts = []
            contact_parts.extend(emails[:2])
            contact_parts.extend(phones[:2])
            result['contact'] = ' | '.join(contact_parts)

        # Extract first line as potential name
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) < 50 and not any(c in line for c in ['@', '(', ')', '-']):
                result['name'] = line
                break

        return result

    def is_available(self) -> bool:
        """Check if AI service is available"""
        import requests
        
        try:
            if self.provider == 'ollama':
                # Check if local service is running
                base_url = (self.endpoint or self.API_ENDPOINTS['ollama']).replace('/api/chat', '')
                response = requests.get(base_url, timeout=5)
                return response.status_code == 200
            elif self.provider == 'lmstudio':
                base_url = (self.endpoint or self.API_ENDPOINTS['lmstudio']).replace('/v1/chat/completions', '')
                response = requests.get(base_url, timeout=5)
                return response.status_code == 200
            elif self.provider == 'gemini':
                # Just check if API key exists
                return bool(self.api_key)
            elif self.provider == 'huggingface':
                # Just check if API key exists
                return bool(self.api_key)
            elif self.provider == 'openai':
                return bool(self.api_key)
            else:
                response = requests.get(self.endpoint, timeout=5)
                return response.status_code == 200
        except Exception:
            return False

    def get_available_providers(self) -> List[Dict[str, str]]:
        """Get list of available AI providers"""
        return [
            {
                'id': 'gemini',
                'name': 'Google Gemini (Free)',
                'description': 'Free tier available (1500 requests/day)',
                'default_model': 'gemini-1.5-flash',
                'setup': 'Get API key at: https://makersuite.google.com/app/apikey'
            },
            {
                'id': 'huggingface',
                'name': 'Hugging Face (Free)',
                'description': 'Free inference API',
                'default_model': 'mistralai/Mistral-7B-Instruct-v0.3',
                'setup': 'Get API key at: https://huggingface.co/settings/tokens'
            },
            {
                'id': 'ollama',
                'name': 'Ollama (Local/Free)',
                'description': 'Run AI locally (requires Ollama installed)',
                'default_model': 'llama3.2',
                'setup': 'Install at: https://ollama.ai/ then run: ollama pull llama3.2'
            },
            {
                'id': 'lmstudio',
                'name': 'LM Studio (Local/Free)',
                'description': 'Run AI locally (requires LM Studio)',
                'default_model': 'local-model',
                'setup': 'Install at: https://lmstudio.ai/'
            },
            {
                'id': 'openai',
                'name': 'OpenAI API (Paid)',
                'description': 'Cloud AI (requires API key, paid)',
                'default_model': 'gpt-3.5-turbo',
                'setup': 'Get API key at: https://platform.openai.com/'
            }
        ]
