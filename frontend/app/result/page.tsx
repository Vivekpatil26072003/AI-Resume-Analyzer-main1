'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, CheckCircle, XCircle, Lightbulb, FileText } from 'lucide-react';
import ScoreCard from '@/components/ScoreCard';
import SkillBadge from '@/components/SkillBadge';
import { AnalysisResponse } from '@/lib/api';

export default function ResultPage() {
  const router = useRouter();
  const [analysisResults, setAnalysisResults] = useState<AnalysisResponse | null>(null);
  const [extractedSkills, setExtractedSkills] = useState<string[]>([]);
  const [jobDescription, setJobDescription] = useState('');
  const [fileName, setFileName] = useState('');

  useEffect(() => {
    // Retrieve data from session storage
    const storedResults = sessionStorage.getItem('analysisResults');
    const storedSkills = sessionStorage.getItem('extractedSkills');
    const storedJD = sessionStorage.getItem('jobDescription');
    const storedFileName = sessionStorage.getItem('fileName');

    if (!storedResults) {
      router.push('/');
      return;
    }

    try {
      setAnalysisResults(JSON.parse(storedResults));
      setExtractedSkills(JSON.parse(storedSkills || '[]'));
      setJobDescription(storedJD || '');
      setFileName(storedFileName || '');
    } catch (error) {
      console.error('Error parsing stored data:', error);
      router.push('/');
    }
  }, [router]);

  const handleNewAnalysis = () => {
    // Clear session storage and go back to home
    sessionStorage.clear();
    router.push('/');
  };

  if (!analysisResults) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h1>
              <p className="text-gray-600">
                Resume: <span className="font-medium">{fileName}</span>
              </p>
            </div>
            <button
              onClick={handleNewAnalysis}
              className="btn-secondary flex items-center"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              New Analysis
            </button>
          </div>

          {/* Score Card */}
          <div className="mb-8">
            <ScoreCard score={analysisResults.score} />
          </div>

          {/* Main Content Grid */}
          <div className="grid lg:grid-cols-2 gap-8 mb-8">
            {/* Skills Analysis */}
            <div className="space-y-6">
              {/* Candidate Skills */}
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-blue-600" />
                  Your Skills
                </h3>
                <div className="flex flex-wrap gap-2">
                  {analysisResults.candidate_skills.length > 0 ? (
                    analysisResults.candidate_skills.map((skill, index) => (
                      <SkillBadge key={index} skill={skill} variant="default" />
                    ))
                  ) : (
                    <p className="text-gray-500">No skills detected in your resume</p>
                  )}
                </div>
              </div>

              {/* Matched Skills */}
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                  Matched Skills
                </h3>
                <div className="flex flex-wrap gap-2">
                  {analysisResults.matched_skills.length > 0 ? (
                    analysisResults.matched_skills.map((skill, index) => (
                      <SkillBadge key={index} skill={skill} variant="matched" />
                    ))
                  ) : (
                    <p className="text-gray-500">No skills matched with the job requirements</p>
                  )}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <XCircle className="w-5 h-5 mr-2 text-red-600" />
                  Missing Skills
                </h3>
                <div className="flex flex-wrap gap-2">
                  {analysisResults.missing_skills.length > 0 ? (
                    analysisResults.missing_skills.map((skill, index) => (
                      <SkillBadge key={index} skill={skill} variant="missing" />
                    ))
                  ) : (
                    <p className="text-green-600 font-medium">All required skills are present! 🎉</p>
                  )}
                </div>
              </div>
            </div>

            {/* Suggestions and Job Description */}
            <div className="space-y-6">
              {/* Suggestions */}
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <Lightbulb className="w-5 h-5 mr-2 text-yellow-600" />
                  Improvement Suggestions
                </h3>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-gray-800 leading-relaxed">
                    {analysisResults.suggestions}
                  </p>
                </div>
              </div>

              {/* Job Description */}
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Job Description</h3>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
                    {jobDescription}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Analysis */}
          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Detailed Analysis</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {analysisResults.candidate_skills.length}
                </div>
                <p className="text-gray-600">Skills Found in Resume</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {analysisResults.matched_skills.length}
                </div>
                <p className="text-gray-600">Skills Matched</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-red-600 mb-2">
                  {analysisResults.missing_skills.length}
                </div>
                <p className="text-gray-600">Skills Missing</p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-8 text-center space-x-4">
            <button
              onClick={handleNewAnalysis}
              className="btn-primary"
            >
              Analyze Another Resume
            </button>
            <button
              onClick={() => window.print()}
              className="btn-secondary"
            >
              Print Results
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}




