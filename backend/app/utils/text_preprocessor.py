import re
import nltk
from typing import List
# import spacy  # Commented out spaCy for now

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load spaCy model - commented out for now
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     # If model is not available, we'll use basic preprocessing
#     nlp = None
nlp = None  # Disabled spaCy for now


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing special characters and extra whitespace.
    
    Args:
        text: Input text string
        
    Returns:
        Cleaned text string
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def remove_stopwords(text: str) -> str:
    """
    Remove common stopwords from text.
    
    Args:
        text: Input text string
        
    Returns:
        Text with stopwords removed
    """
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Get English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    return ' '.join(filtered_tokens)


def extract_entities(text: str) -> List[str]:
    """
    Extract named entities from text using spaCy.
    
    Args:
        text: Input text string
        
    Returns:
        List of extracted entities
    """
    if nlp is None:
        # Fallback: extract potential entities using regex patterns
        entities = []
        # Look for capitalized words that might be entities
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 2:
                entities.append(word.strip())
        return entities[:10]  # Limit to first 10 potential entities
    
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'WORK_OF_ART']:
            entities.append(ent.text.strip())
    
    return entities


def preprocess_text(text: str) -> str:
    """
    Complete text preprocessing pipeline.
    
    Args:
        text: Input text string
        
    Returns:
        Preprocessed text string
    """
    # Clean text
    text = clean_text(text)
    
    # Remove stopwords
    text = remove_stopwords(text)
    
    return text


def extract_skills_from_text(text: str, skills_database: dict) -> List[str]:
    """
    Extract skills from text using the skills database.
    
    Args:
        text: Input text string
        skills_database: Dictionary containing skills by category
        
    Returns:
        List of found skills
    """
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Create a set of all skills from the database
    all_skills = set()
    for category, skills in skills_database.items():
        all_skills.update([skill.lower() for skill in skills])
    
    # Tokenize processed text
    tokens = word_tokenize(processed_text)
    
    # Find matching skills
    found_skills = []
    for token in tokens:
        if token.lower() in all_skills:
            # Find the original case from the database
            for category, skills in skills_database.items():
                for skill in skills:
                    if skill.lower() == token.lower():
                        found_skills.append(skill)
                        break
    
    # Remove duplicates while preserving order
    unique_skills = []
    for skill in found_skills:
        if skill not in unique_skills:
            unique_skills.append(skill)
    
    return unique_skills

