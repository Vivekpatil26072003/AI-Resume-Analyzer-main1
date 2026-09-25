import json
import os
import sys
from typing import List, Dict, Tuple

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.text_extractor import extract_text_from_file
from utils.text_preprocessor import extract_skills_from_text


class ResumeAnalyzer:
    def __init__(self):
        """Initialize the ResumeAnalyzer with skills database."""
        self.skills_database = self._load_skills_database()
    
    def _load_skills_database(self) -> Dict[str, List[str]]:
        """
        Load skills database from JSON file.
        
        Returns:
            Dictionary containing skills by category
        """
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the data directory
            data_dir = os.path.join(current_dir, '..', '..', 'data')
            skills_file = os.path.join(data_dir, 'skills.json')
            
            with open(skills_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load skills database: {e}")
            # Return a basic skills database as fallback
            return {
                "programming_languages": ["Python", "JavaScript", "Java", "C++", "C#"],
                "web_frameworks": ["React", "Angular", "Vue.js", "Django", "Flask"],
                "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
                "cloud_platforms": ["AWS", "Azure", "Google Cloud"],
                "devops_tools": ["Docker", "Kubernetes", "Jenkins", "Git"]
            }
    
    def extract_skills_from_resume(self, file_content: bytes, file_extension: str) -> Tuple[List[str], str]:
        """
        Extract skills from resume file.
        
        Args:
            file_content: File content as bytes
            file_extension: File extension (e.g., '.pdf', '.docx')
            
        Returns:
            Tuple of (extracted_skills, extracted_text)
        """
        # Extract text from file
        extracted_text = extract_text_from_file(file_content, file_extension)
        
        # Extract skills from text
        extracted_skills = extract_skills_from_text(extracted_text, self.skills_database)
        
        return extracted_skills, extracted_text
    
    def extract_skills_from_jd(self, job_description: str) -> List[str]:
        """
        Extract required skills from job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            List of required skills
        """
        return extract_skills_from_text(job_description, self.skills_database)
    
    def analyze_match(self, candidate_skills: List[str], job_description: str) -> Dict:
        """
        Analyze match between candidate skills and job description.
        
        Args:
            candidate_skills: List of candidate skills
            job_description: Job description text
            
        Returns:
            Dictionary containing analysis results
        """
        # Extract required skills from job description
        required_skills = self.extract_skills_from_jd(job_description)
        
        # Convert to lowercase for comparison
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        # Find matched and missing skills
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills:
            if skill.lower() in candidate_skills_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # Calculate match score
        if len(required_skills) > 0:
            score = (len(matched_skills) / len(required_skills)) * 100
        else:
            score = 0.0
        
        # Generate suggestions
        suggestions = self._generate_suggestions(missing_skills, score)
        
        return {
            "candidate_skills": candidate_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "score": round(score, 2),
            "suggestions": suggestions
        }
    
    def _generate_suggestions(self, missing_skills: List[str], score: float) -> str:
        """
        Generate improvement suggestions based on missing skills and score.
        
        Args:
            missing_skills: List of missing skills
            score: Current match score
            
        Returns:
            Suggestion string
        """
        if score >= 80:
            return "Excellent match! Your skills align very well with the job requirements."
        elif score >= 60:
            if missing_skills:
                return f"Good match! Consider adding {', '.join(missing_skills[:3])} to your resume to improve your score."
            else:
                return "Good match! Your skills meet most of the requirements."
        elif score >= 40:
            if missing_skills:
                return f"Moderate match. Focus on acquiring {', '.join(missing_skills[:3])} to significantly improve your chances."
            else:
                return "Moderate match. Consider expanding your skill set to better align with the job requirements."
        else:
            if missing_skills:
                return f"Low match. Priority skills to develop: {', '.join(missing_skills[:5])}. Consider taking relevant courses or certifications."
            else:
                return "Low match. Consider gaining more experience in the required technologies before applying."
    
    def get_skills_by_category(self) -> Dict[str, List[str]]:
        """
        Get all skills organized by category.
        
        Returns:
            Dictionary of skills by category
        """
        return self.skills_database

