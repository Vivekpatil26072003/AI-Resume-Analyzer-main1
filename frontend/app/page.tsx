'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload, FileText, Send } from 'lucide-react';
import FileUpload from '@/components/FileUpload';
import { uploadResume, analyzeResume, AnalysisRequest } from '@/lib/api';

export default function HomePage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [extractedSkills, setExtractedSkills] = useState<string[]>([]);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a resume file');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // First, upload and extract skills from resume
      const uploadResponse = await uploadResume(selectedFile);
      setExtractedSkills(uploadResponse.candidate_skills);

      // Then analyze the skills against job description
      const analysisRequest: AnalysisRequest = {
        candidate_skills: uploadResponse.candidate_skills,
        job_description: jobDescription
      };

      const analysisResponse = await analyzeResume(analysisRequest);

      // Store results in session storage and navigate to results page
      sessionStorage.setItem('analysisResults', JSON.stringify(analysisResponse));
      sessionStorage.setItem('extractedSkills', JSON.stringify(uploadResponse.candidate_skills));
      sessionStorage.setItem('jobDescription', jobDescription);
      sessionStorage.setItem('fileName', selectedFile.name);

      router.push('/result');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred during analysis');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Resume Analyzer
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your resume and compare it against job descriptions to get personalized insights and improvement suggestions.
          </p>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Resume Upload Section */}
            <div className="card">
              <div className="flex items-center mb-6">
                <Upload className="w-6 h-6 text-primary-600 mr-3" />
                <h2 className="text-2xl font-semibold text-gray-900">Upload Resume</h2>
              </div>
              
              <FileUpload onFileSelect={handleFileSelect} />
              
              {extractedSkills.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">Extracted Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {extractedSkills.map((skill, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Job Description Section */}
            <div className="card">
              <div className="flex items-center mb-6">
                <FileText className="w-6 h-6 text-primary-600 mr-3" />
                <h2 className="text-2xl font-semibold text-gray-900">Job Description</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="jobDescription" className="block text-sm font-medium text-gray-700 mb-2">
                    Paste the job description here
                  </label>
                  <textarea
                    id="jobDescription"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Enter the job description to analyze against your resume..."
                    className="input-field h-48 resize-none"
                    rows={8}
                  />
                </div>

                <div className="text-sm text-gray-500">
                  <p>• The AI will extract required skills from the job description</p>
                  <p>• Compare them with skills found in your resume</p>
                  <p>• Provide a match score and improvement suggestions</p>
                </div>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* Analyze Button */}
          <div className="mt-8 text-center">
            <button
              onClick={handleAnalyze}
              disabled={isLoading || !selectedFile || !jobDescription.trim()}
              className="btn-primary text-lg px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5 mr-2" />
                  Analyze Resume
                </>
              )}
            </button>
          </div>

          {/* Features */}
          <div className="mt-16 grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Upload className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Easy Upload</h3>
              <p className="text-gray-600">Upload PDF or DOCX resumes with drag & drop support</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Analysis</h3>
              <p className="text-gray-600">AI-powered skill extraction and matching analysis</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Send className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Actionable Insights</h3>
              <p className="text-gray-600">Get detailed feedback and improvement suggestions</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}




