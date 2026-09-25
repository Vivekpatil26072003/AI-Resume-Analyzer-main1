# AI Resume Analyzer

A full-stack web application that analyzes resumes against job descriptions to provide skill matching scores and improvement suggestions. Built with modern technologies for optimal performance and user experience.

## 🚀 Features

- **Resume Upload**: Support for PDF and DOCX files with drag-and-drop functionality
- **Job Description Analysis**: Text input for job requirements with real-time processing
- **Skill Matching**: Automatic extraction and comparison of skills using NLP
- **Match Scoring**: Percentage-based matching score with detailed breakdown
- **Improvement Suggestions**: Actionable recommendations for resume enhancement
- **Modern UI**: Responsive design with beautiful, intuitive interface
- **Real-time Processing**: Fast analysis with immediate results

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons

### Backend
- **Flask** - Python web framework
- **NLTK** - Natural language processing
- **pdfminer.six** - PDF text extraction
- **python-docx** - DOCX file processing
- **Flask-CORS** - Cross-origin resource sharing

## 📁 Project Structure

```
AI Resume Analyzer/
├── frontend/                    # Next.js application
│   ├── app/
│   │   ├── page.tsx            # Home page with upload form
│   │   ├── result/page.tsx     # Results page
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── FileUpload.tsx      # File upload component
│   │   ├── SkillBadge.tsx      # Skill badge component
│   │   └── ScoreCard.tsx       # Score display component
│   ├── lib/
│   │   └── api.ts              # API utility functions
│   ├── package.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── tsconfig.json
├── backend/                    # Flask application
│   ├── app/
│   │   ├── main.py            # Flask app entry point
│   │   ├── services/
│   │   │   └── resume_analyzer.py  # Main analysis logic
│   │   └── utils/
│   │       ├── text_extractor.py   # PDF/DOCX text extraction
│   │       └── text_preprocessor.py # Text preprocessing & skill extraction
│   ├── data/
│   │   └── skills.json        # Skills database
│   ├── requirements.txt
│   └── start.py               # Backend startup script
├── setup.py                   # Automated setup script
├── start.bat                  # Windows startup script
├── start.sh                   # Unix startup script
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - Backend runtime
- **Node.js 16+** - Frontend runtime
- **npm** - Package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Run the automated setup:**
   ```bash
   python setup.py
   ```

3. **Start both servers:**
   - **Windows:** Double-click `start.bat` or run `start.bat` in Command Prompt
   - **Unix/Linux/macOS:** Run `./start.sh` in terminal

4. **Open the application:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app/main.py
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📋 API Endpoints

### POST /upload_resume
Upload and extract skills from resume files.

**Request:**
- Content-Type: multipart/form-data
- Body: file (PDF/DOCX)

**Response:**
```json
{
  "candidate_skills": ["Python", "React", "AWS"],
  "extracted_text": "..."
}
```

### POST /analyze
Analyze resume skills against job description.

**Request:**
```json
{
  "candidate_skills": ["Python", "React", "AWS"],
  "job_description": "We need a developer with Python, Java, and Docker skills..."
}
```

**Response:**
```json
{
  "candidate_skills": ["Python", "React", "AWS"],
  "matched_skills": ["Python"],
  "missing_skills": ["Java", "Docker"],
  "score": 33.33,
  "suggestions": "Consider adding Java and Docker to your resume to improve your match score."
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Resume Analyzer API is running"
}
```

## 🎯 Usage

1. **Upload Resume**: Select a PDF or DOCX file containing your resume
2. **Enter Job Description**: Paste the job description text
3. **Analyze**: Click submit to get your match score and analysis
4. **Review Results**: See matched skills, missing skills, and improvement suggestions

## 🔧 Configuration

### Skills Database
The application uses a predefined skills database located in `backend/data/skills.json`. You can customize this file to include domain-specific skills for your use case.

### Environment Variables

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com
```

**Backend (.env):**
```env
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://your-frontend-url.netlify.app
```

### Customization
- **Skills Database:** Edit `backend/data/skills.json` to add/remove skills
- **UI Styling:** Modify `frontend/tailwind.config.js` for custom styling
- **API Endpoints:** Extend `backend/app/main.py` for additional functionality

## 🚀 Deployment

### Quick Deploy (Recommended)

**For Netlify (Frontend):**
1. Connect your GitHub repository to Netlify
2. Build command: `npm run build` (automatically configured in netlify.toml)
3. Publish directory: `out` (automatically configured in netlify.toml)
4. Set environment variable: `NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com`

**For Heroku (Backend):**
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set CORS_ORIGINS=https://your-frontend-url.netlify.app

# Deploy backend
git subtree push --prefix backend heroku main
```

### Manual Deployment

**Backend Deployment:**
- **Heroku** - Easy deployment with Procfile
- **Railway** - Modern Python hosting
- **Render** - Free tier available
- **AWS** - Using Elastic Beanstalk or EC2

**Frontend Deployment:**
- **Netlify** - Static site hosting (configured)
- **Vercel** - Next.js optimized (configured)
- **AWS S3** - Static website hosting
- **GitHub Pages** - Free hosting

> 📋 **See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions and troubleshooting.**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NLTK** for natural language processing capabilities
- **pdfminer.six** for PDF text extraction
- **python-docx** for DOCX file processing
- **TailwindCSS** for the beautiful UI components
- **Next.js** for the amazing React framework

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

---

**Made with ❤️ for better job matching and career growth**
#   a i - r e s u m e - a n a l y z e r 0 1 
 
 #   A I - R e s u m e - A n a l y z e r - m a i n 1  
 #   A I - R e s u m e - A n a l y z e r - m a i n 1  
 