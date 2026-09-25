from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
import logging
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.resume_analyzer import ResumeAnalyzer

app = Flask(__name__)
logger = logging.getLogger(__name__)

try:
    max_file_size = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))
except ValueError:
    max_file_size = 10 * 1024 * 1024

app.config["MAX_CONTENT_LENGTH"] = max_file_size

allowed_file_types = {
    file_type.strip().lower()
    for file_type in os.getenv("ALLOWED_FILE_TYPES", ".pdf,.docx").split(",")
    if file_type.strip()
}

# Configure CORS for production
allowed_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://resume-ai-an.netlify.app",
    "https://ai-resume-analyzer.netlify.app",
    "https://ai-resume-analyzer.vercel.app"
]

# Add environment variable for custom origins
if os.getenv("CORS_ORIGINS"):
    allowed_origins.extend(
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "").split(",")
        if origin.strip()
    )

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


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    return jsonify({"error": "Uploaded file is too large"}), 413


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
        if file_extension not in allowed_file_types:
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
        candidate_name = resume_analyzer.extract_candidate_name(extracted_text)
        
        return jsonify({
            "candidate_name": candidate_name,
            "candidate_skills": candidate_skills,
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        })
        
    except Exception:
        logger.exception("Error processing resume upload")
        return jsonify({"error": "Error processing resume"}), 500


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
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Request body must be valid JSON"}), 400

        # Validate input
        if not payload.get("candidate_skills"):
            return jsonify({"error": "Candidate skills cannot be empty"}), 400
        
        if not payload.get("job_description"):
            return jsonify({"error": "Job description cannot be empty"}), 400
        
        # Perform analysis
        analysis_result = resume_analyzer.analyze_match(
            payload["candidate_skills"],
            payload["job_description"]
        )
        
        return jsonify(analysis_result)
        
    except Exception:
        logger.exception("Error analyzing resume")
        return jsonify({"error": "Error analyzing resume"}), 500


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
    except Exception:
        logger.exception("Error retrieving skills")
        return jsonify({"error": "Error retrieving skills"}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    app.run(host=host, port=port, debug=debug)

