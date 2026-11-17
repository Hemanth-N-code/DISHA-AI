// frontend/src/services/api.ts
import {
  User, StudentProfile, CareerDetail, CareerCandidate,
  SkillGapResponse, WhatIfResponse, CompareResponse,
  Roadmap, RoadmapTask, JourneyResponse, ResearchMetrics,
  CetExam, CetDomain, CollegeDetail, CetAnalyzeResponse,
  CutoffTrendResponse, CollegeComparisonResponse, OptionListResponse,
  OptionItem, StudentCetProfile, CareerBranchMappingResponse
} from '../types';

const BASE_URL = '/api/v1';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('disha_token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorBody.detail || 'An unexpected API error occurred');
  }
  return res.json();
}

export const api = {
  // Authentication
  auth: {
    async register(data: { email: string; password: string; full_name: string }) {
      const res = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return handleResponse<{ access_token: string; user_id: number; email: string; full_name: string }>(res);
    },
    async login(data: { email: string; password: string }) {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return handleResponse<{ access_token: string; user_id: number; email: string; full_name: string }>(res);
    },
    async getMe(): Promise<User> {
      const res = await fetch(`${BASE_URL}/auth/me`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<User>(res);
    },
  },

  // Student Profile
  profile: {
    async get(): Promise<StudentProfile> {
      const res = await fetch(`${BASE_URL}/profile`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<StudentProfile>(res);
    },
    async createOrUpdate(profileData: any): Promise<StudentProfile> {
      const res = await fetch(`${BASE_URL}/profile`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(profileData),
      });
      return handleResponse<StudentProfile>(res);
    },
    async update(partialData: any): Promise<StudentProfile> {
      const res = await fetch(`${BASE_URL}/profile`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(partialData),
      });
      return handleResponse<StudentProfile>(res);
    },
  },

  // Careers
  careers: {
    async list(domain?: string, search?: string): Promise<CareerDetail[]> {
      const params = new URLSearchParams();
      if (domain) params.append('domain', domain);
      if (search) params.append('search', search);
      const res = await fetch(`${BASE_URL}/careers?${params.toString()}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CareerDetail[]>(res);
    },
    async getById(id: string): Promise<CareerDetail> {
      const res = await fetch(`${BASE_URL}/careers/${id}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CareerDetail>(res);
    },
    async discover(applyDiversity: boolean = true, domainFilter?: string): Promise<{
      total_careers_in_universe: number;
      domains_represented: string[];
      career_diversity_index: number;
      candidates: CareerCandidate[];
      discovery_strategy: string;
    }> {
      const res = await fetch(`${BASE_URL}/careers/discover`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          apply_diversity: applyDiversity,
          domain_filter: domainFilter,
          limit: 16
        }),
      });
      return handleResponse(res);
    },
    async analyze(id: string): Promise<any> {
      const res = await fetch(`${BASE_URL}/careers/${id}/analyze`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      return handleResponse(res);
    },
    async getGraph(id: string): Promise<any> {
      const res = await fetch(`${BASE_URL}/careers/${id}/graph`, {
        headers: getAuthHeaders(),
      });
      return handleResponse(res);
    },
    async compare(careerIds: string[]): Promise<CompareResponse> {
      const res = await fetch(`${BASE_URL}/careers/compare`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ career_ids: careerIds }),
      });
      return handleResponse<CompareResponse>(res);
    },
  },

  // What-If Analysis
  whatIf: {
    async simulate(params: {
      programming_preference?: string;
      mathematics_preference?: string;
      creativity_level?: string;
      people_interaction_preference?: string;
      added_interests?: string[];
      removed_interests?: string[];
      save_as_permanent?: boolean;
    }): Promise<WhatIfResponse> {
      const res = await fetch(`${BASE_URL}/what-if`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(params),
      });
      return handleResponse<WhatIfResponse>(res);
    },
  },

  // Skill Gap Analysis
  skillGap: {
    async get(careerId: string): Promise<SkillGapResponse> {
      const res = await fetch(`${BASE_URL}/skill-gap/${careerId}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<SkillGapResponse>(res);
    },
  },

  // Roadmap
  roadmap: {
    async generate(careerId: string, horizonMonths: number = 6): Promise<Roadmap> {
      const res = await fetch(`${BASE_URL}/roadmap/generate`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ career_id: careerId, target_horizon_months: horizonMonths }),
      });
      return handleResponse<Roadmap>(res);
    },
    async getActive(careerId: string): Promise<Roadmap> {
      const res = await fetch(`${BASE_URL}/roadmap/${careerId}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<Roadmap>(res);
    },
    async updateTask(taskId: number, status?: string, portfolioArtifact?: string): Promise<RoadmapTask> {
      const res = await fetch(`${BASE_URL}/roadmap/tasks/${taskId}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ status, portfolio_artifact: portfolioArtifact }),
      });
      return handleResponse<RoadmapTask>(res);
    },
  },

  // Memory & Journey
  memory: {
    async getJourney(): Promise<JourneyResponse> {
      const res = await fetch(`${BASE_URL}/memory/journey`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<JourneyResponse>(res);
    },
    async toggleSave(careerId: string, careerName: string): Promise<{ career_id: string; is_saved: boolean }> {
      const res = await fetch(`${BASE_URL}/memory/save-career`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ career_id: careerId, career_name: careerName }),
      });
      return handleResponse(res);
    },
    async rejectCareer(careerId: string, careerName: string, reason: string): Promise<any> {
      const res = await fetch(`${BASE_URL}/memory/reject-career`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ career_id: careerId, career_name: careerName, reason }),
      });
      return handleResponse(res);
    },
  },

  // Chat Assistant
  chat: {
    async send(message: string, careerContextId?: string, history: any[] = []): Promise<{
      reply: string;
      suggested_actions: string[];
      grounded_career_sources: string[];
      what_if_trigger?: any;
    }> {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 35000);
      try {
        const res = await fetch(`${BASE_URL}/chat`, {
          method: 'POST',
          headers: getAuthHeaders(),
          signal: controller.signal,
          body: JSON.stringify({
            message,
            career_context_id: careerContextId,
            conversation_history: history,
          }),
        });
        clearTimeout(timeoutId);
        return handleResponse(res);
      } catch (err: any) {
        clearTimeout(timeoutId);
        if (err.name === 'AbortError') {
          throw new Error('Chat request timed out after 25 seconds. Please check your network and backend server.');
        }
        throw err;
      }
    },
  },

  // Research Metrics
  research: {
    async getMetrics(): Promise<ResearchMetrics> {
      const res = await fetch(`${BASE_URL}/research/metrics`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<ResearchMetrics>(res);
    },
    async logEvent(eventType: string, data: any = {}): Promise<any> {
      const res = await fetch(`${BASE_URL}/research/event`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ event_type: eventType, event_data: data }),
      });
      return handleResponse(res);
    },
    async rateConfidence(stage: 'pre_exploration' | 'post_exploration', score: number): Promise<any> {
      const res = await fetch(`${BASE_URL}/research/confidence`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ stage, confidence_score: score }),
      });
      return handleResponse(res);
    },
    async getInspector(targetUserId?: number): Promise<any> {
      const url = targetUserId ? `${BASE_URL}/research/inspector?target_user_id=${targetUserId}` : `${BASE_URL}/research/inspector`;
      const res = await fetch(url, {
        headers: getAuthHeaders(),
      });
      return handleResponse<any>(res);
    },
  },

  // CET Support Module
  cet: {
    async getExams(): Promise<CetExam[]> {
      const res = await fetch(`${BASE_URL}/cet/exams`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CetExam[]>(res);
    },
    async getDomains(examId: string = 'kcet'): Promise<CetDomain[]> {
      const res = await fetch(`${BASE_URL}/cet/domains?exam_id=${examId}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CetDomain[]>(res);
    },
    async getProfile(): Promise<StudentCetProfile | null> {
      const res = await fetch(`${BASE_URL}/cet/profile`, {
        headers: getAuthHeaders(),
      });
      if (res.status === 404) return null;
      return handleResponse<StudentCetProfile>(res);
    },
    async saveProfile(profileData: any): Promise<StudentCetProfile> {
      const res = await fetch(`${BASE_URL}/cet/profile`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(profileData),
      });
      return handleResponse<StudentCetProfile>(res);
    },
    async analyzeOptions(data: {
      rank: number;
      category?: string;
      domain_id?: string;
      preferred_branches?: string[];
      preferred_locations?: string[];
      preferences?: string[];
      round_num?: number;
      sort_by?: string;
    }): Promise<CetAnalyzeResponse> {
      const res = await fetch(`${BASE_URL}/cet/analyze`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
      });
      return handleResponse<CetAnalyzeResponse>(res);
    },
    async getColleges(city?: string, collegeType?: string): Promise<CollegeDetail[]> {
      const params = new URLSearchParams();
      if (city) params.append('city', city);
      if (collegeType) params.append('college_type', collegeType);
      const res = await fetch(`${BASE_URL}/cet/colleges?${params.toString()}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CollegeDetail[]>(res);
    },
    async getCollegeDetail(collegeId: string): Promise<CollegeDetail> {
      const res = await fetch(`${BASE_URL}/cet/colleges/${collegeId}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CollegeDetail>(res);
    },
    async getCutoffTrend(collegeId: string, branch: string = 'CS', category: string = 'GM', roundNum: number = 1): Promise<CutoffTrendResponse> {
      const res = await fetch(`${BASE_URL}/cet/college/${collegeId}/trend?branch=${branch}&category=${category}&round_num=${roundNum}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CutoffTrendResponse>(res);
    },
    async compareColleges(data: { college_ids: string[]; branch_code: string; category?: string }): Promise<CollegeComparisonResponse> {
      const res = await fetch(`${BASE_URL}/cet/compare`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
      });
      return handleResponse<CollegeComparisonResponse>(res);
    },
    async getOptionList(): Promise<OptionListResponse> {
      const res = await fetch(`${BASE_URL}/cet/option-list`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<OptionListResponse>(res);
    },
    async addOptionItem(data: { college_branch_id: number; historical_category?: string; student_notes?: string }): Promise<OptionItem> {
      const res = await fetch(`${BASE_URL}/cet/option-list/item`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
      });
      return handleResponse<OptionItem>(res);
    },
    async removeOptionItem(itemId: number): Promise<{ message: string }> {
      const res = await fetch(`${BASE_URL}/cet/option-list/item/${itemId}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      return handleResponse<{ message: string }>(res);
    },
    async reorderOptionList(orderedItemIds: number[]): Promise<OptionListResponse> {
      const res = await fetch(`${BASE_URL}/cet/option-list/reorder`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ ordered_item_ids: orderedItemIds }),
      });
      return handleResponse<OptionListResponse>(res);
    },
    async getCareerBranches(careerId: string): Promise<CareerBranchMappingResponse> {
      const res = await fetch(`${BASE_URL}/cet/career-branches/${careerId}`, {
        headers: getAuthHeaders(),
      });
      return handleResponse<CareerBranchMappingResponse>(res);
    },
    async logEvent(eventType: string, data: any = {}): Promise<any> {
      const res = await fetch(`${BASE_URL}/cet/log-event`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ event_type: eventType, event_data: data }),
      });
      return handleResponse(res);
    },
  },
};
