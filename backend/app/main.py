from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.resume_analyzer import ResumeAnalyzer

app = Flask(__name__)
# Configure CORS for production
allowed_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "https://ai-resume-analyzer.netlify.app",
    "https://ai-resume-analyzer.vercel.app"
]

# Add environment variable for custom origins
if os.getenv("CORS_ORIGINS"):
    allowed_origins.extend(os.getenv("CORS_ORIGINS").split(","))

CORS(app, origins=allowed_origins, supports_credentials=True)

# Initialize resume analyzer
resume_analyzer = ResumeAnalyzer()


@app.route("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Resume Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "upload_resume": "POST /upload_resume",
            "analyze": "POST /analyze",
            "health": "GET /health"
        }
    }


@app.route("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "AI Resume Analyzer API is running"}


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """
    Upload and extract skills from resume file.
    
    Args:
        file: Resume file (PDF or DOCX)
        
    Returns:
        Extracted skills and text from resume
    """
    try:
        # Validate file type
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if not file.filename:
            return jsonify({"error": "No file provided"}), 400
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.pdf', '.docx']:
            return jsonify({
                "error": "Unsupported file format. Please upload PDF or DOCX files only."
            }), 400
        
        # Read file content
        file_content = file.read()
        
        if len(file_content) == 0:
            return jsonify({"error": "Empty file provided"}), 400
        
        # Extract skills from resume
        candidate_skills, extracted_text = resume_analyzer.extract_skills_from_resume(
            file_content, file_extension
        )
        
        return jsonify({
            "candidate_skills": candidate_skills,
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing resume: {str(e)}"}), 500


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """
    Analyze candidate skills against job description.
    
    Args:
        request: AnalysisRequest containing candidate skills and job description
        
    Returns:
        Analysis results with match score and suggestions
    """
    try:
        # Validate input
        if not request.json.get("candidate_skills"):
            return jsonify({"error": "Candidate skills cannot be empty"}), 400
        
        if not request.json.get("job_description"):
            return jsonify({"error": "Job description cannot be empty"}), 400
        
        # Perform analysis
        analysis_result = resume_analyzer.analyze_match(
            request.json["candidate_skills"], 
            request.json["job_description"]
        )
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({"error": f"Error analyzing resume: {str(e)}"}), 500


@app.route("/skills")
def get_skills():
    """
    Get all available skills organized by category.
    
    Returns:
        Dictionary of skills by category
    """
    try:
        skills = resume_analyzer.get_skills_by_category()
        return {"skills": skills}
    except Exception as e:
        return jsonify({"error": f"Error retrieving skills: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

