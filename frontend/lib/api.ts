import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || (
  process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : undefined
);

const api = axios.create({
  baseURL: API_BASE_URL,
});

function ensureApiConfigured(): void {
  if (!API_BASE_URL) {
    throw new Error('NEXT_PUBLIC_API_URL is not configured for this deployment');
  }
}

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
  candidate_name: string;
  candidate_skills: string[];
  extracted_text: string;
}

export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  ensureApiConfigured();
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<ResumeUploadResponse>('/upload_resume', formData);

  return response.data;
}

export async function analyzeResume(
  request: AnalysisRequest
): Promise<AnalysisResponse> {
  ensureApiConfigured();
  const response = await api.post<AnalysisResponse>('/analyze', request);
  return response.data;
}

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const requestUrl = `${error.config?.baseURL || ''}${error.config?.url || ''}`;
    const status = error.response?.status;
    const responseMessage = error.response?.data?.error || error.response?.data?.detail;

    console.error('Resume Analyzer API request failed', {
      url: requestUrl,
      status,
      message: error.message,
    });

    if (status) {
      return responseMessage
        ? `Request failed (${status}): ${responseMessage}`
        : `Request failed with HTTP ${status}`;
    }

    return 'Unable to reach the resume analysis backend. Check the backend URL and CORS configuration.';
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An error occurred during analysis';
}
