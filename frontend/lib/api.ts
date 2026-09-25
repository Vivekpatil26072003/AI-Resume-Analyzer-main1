import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export interface AnalysisRequest {
  candidate_skills: string[];
  job_description: string;
}

export interface AnalysisResponse {
  candidate_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  score: number;
  suggestions: string;
}

export interface ResumeUploadResponse {
  candidate_skills: string[];
  extracted_text: string;
}

export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<ResumeUploadResponse>('/upload_resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

export async function analyzeResume(
  request: AnalysisRequest
): Promise<AnalysisResponse> {
  const response = await api.post<AnalysisResponse>('/analyze', request);
  return response.data;
}
