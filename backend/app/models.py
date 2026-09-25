from pydantic import BaseModel
from typing import List, Optional


class ResumeUploadResponse(BaseModel):
    candidate_skills: List[str]
    extracted_text: str


class AnalysisRequest(BaseModel):
    candidate_skills: List[str]
    job_description: str


class AnalysisResponse(BaseModel):
    candidate_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    score: float
    suggestions: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

