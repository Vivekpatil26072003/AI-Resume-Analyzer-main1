import os
import io
from typing import Optional
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file content.
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        Extracted text as string
    """
    try:
        # Create a file-like object from bytes
        pdf_file = io.BytesIO(file_content)
        
        # Extract text using pdfminer
        output = io.StringIO()
        extract_text_to_fp(pdf_file, output, laparams=LAParams())
        text = output.getvalue()
        output.close()
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from DOCX file content.
    
    Args:
        file_content: DOCX file content as bytes
        
    Returns:
        Extracted text as string
    """
    try:
        # Create a file-like object from bytes
        docx_file = io.BytesIO(file_content)
        
        # Load document
        doc = Document(docx_file)
        
        # Extract text from all paragraphs
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())
        
        return '\n'.join(text_parts)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_file(file_content: bytes, file_extension: str) -> str:
    """
    Extract text from file based on its extension.
    
    Args:
        file_content: File content as bytes
        file_extension: File extension (e.g., '.pdf', '.docx')
        
    Returns:
        Extracted text as string
    """
    file_extension = file_extension.lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_content)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: .pdf, .docx")

