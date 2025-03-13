import re
from dateutil import parser
from typing import Dict, Optional

SENSITIVE_PATTERNS: Dict[str, str] = {
    "Email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "Phone Number": r"\b(?:\+?\d{1,3})?[-. (]*\d{2,4}[-. )]*\d{3,4}[-. ]*\d{3,4}\b",
    "URL": r"https?://[^\s]+|www\.[^\s]+",
    "IP Address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "Credit Card": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
    "API Key": r"(?i)(api[-_]?(key|token|secret)[\s=:]+['\"`]?[a-z0-9]{32,}['\"`]?)",
    "JWT Token": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "SQL Injection": r"(?:\b(SELECT|UPDATE|DELETE|INSERT|DROP|UNION|ALTER|EXEC)\b.*?['\";]|--)",
    "XSS Attack": r"<script>.*?</script>",
    "SSH Key": r"(?i)-----BEGIN.*?PRIVATE KEY-----.*?-----END.*?PRIVATE KEY-----"
}

def redact_sensitive_info(text: str) -> str:
    if not isinstance(text, str):
        return text
        
    patterns = {label: re.compile(pattern, re.IGNORECASE) 
               for label, pattern in SENSITIVE_PATTERNS.items()}
               
    for label, compiled_pattern in patterns.items():
        text = compiled_pattern.sub(f"[REDACTED_{label}]", text)
    return text

def standardize_dates(text: str) -> str:
    try:
        parsed_date = parser.parse(text, fuzzy=True, default=parser.parse("2000-01-01"))
        if 1900 < parsed_date.year < 2100:
            return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError, OverflowError):
        pass
    return text

def standardize_time(text: str) -> str:
    try:
        parsed_time = parser.parse(text, fuzzy=True)
        if parsed_time.hour < 24 and parsed_time.microsecond == 0:
            return parsed_time.strftime("%H:%M:%S")
    except (ValueError, TypeError, OverflowError):
        pass
    return text

def process_text(text: str) -> str:
    if not text:
        return text
        
    text = redact_sensitive_info(text)
    words = text.split()
    
    processed_words = []
    for word in words:
        if any(char in word for char in "-/"):
            word = standardize_dates(word)
        elif ":" in word:
            word = standardize_time(word)
        processed_words.append(word)
        
    return " ".join(processed_words)