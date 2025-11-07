/**
 * API client for CCGT backend.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const API_KEY = import.meta.env.VITE_API_KEY || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    ...(API_KEY && { Authorization: `Bearer ${API_KEY}` }),
  },
});

export interface EvaluateRequest {
  text: string;
  options?: {
    visualize?: boolean;
  };
}

export interface DisruptionItem {
  from_idx: number;
  to_idx: number;
  reason: string;
  score: number;
}

export interface GraphNode {
  id: number;
  text_snippet: string;
  entropy?: number;
  importance_score?: number;
  embedding_dim_reduced?: number[];
}

export interface GraphEdge {
  source: number;
  target: number;
  weight: number;
  discourse_marker?: string;
  reason?: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface EvaluateResponse {
  coherence_score: number;
  coherence_percent: number;
  disruption_report: DisruptionItem[];
  graph?: GraphData;
}

export const evaluateText = async (
  text: string,
  visualize: boolean = true
): Promise<EvaluateResponse> => {
  const response = await api.post<EvaluateResponse>('/api/v1/evaluate', {
    text,
    options: { visualize },
  });
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/api/v1/health');
  return response.data;
};

export const submitContact = async (params: { name: string; email: string; organization: string; message: string; }) => {
  const form = new FormData();
  form.append('name', params.name);
  form.append('email', params.email);
  form.append('organization', params.organization);
  form.append('message', params.message);
  
  // Use a separate axios instance without default Content-Type for FormData
  // axios will automatically set multipart/form-data with boundary
  const response = await axios.post(`${API_BASE_URL}/api/v1/contact`, form, {
    headers: {
      ...(API_KEY && { Authorization: `Bearer ${API_KEY}` }),
      // Don't set Content-Type - let axios/browser set it with boundary
    },
  });
  
  // axios automatically throws for non-2xx status codes, so if we get here, it's a success
  return response.data;
};

