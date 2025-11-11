import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: { username: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
};

// Flashcards API
export const flashcardsAPI = {
  getAll: (params?: { skip?: number; limit?: number; category?: string }) =>
    api.get('/flashcards', { params }),
  getById: (id: string) => api.get(`/flashcards/${id}`),
  seed: () => api.post('/flashcards/seed'),
};

// Quiz API
export const quizAPI = {
  getQuestions: (count: number = 20) =>
    api.get('/quiz/questions', { params: { count } }),
  submitQuiz: (data: { answers: Array<{ question_id: string; selected_answer: string }> }) =>
    api.post('/quiz/submit', data),
};

// SRS API
export const srsAPI = {
  getDueCards: () => api.get('/srs/due'),
  getReviewCards: (limit: number = 20) => api.get('/srs/review', { params: { limit } }),
  submitReview: (data: { flashcard_id: string; quality: number }) =>
    api.post('/srs/review', data),
  getStats: () => api.get('/srs/stats'),
};

// Leaderboard API
export const leaderboardAPI = {
  getGlobal: (params?: { limit?: number; timeframe?: string }) =>
    api.get('/leaderboard/global', { params }),
  getWeekly: (limit: number = 100) => api.get('/leaderboard/weekly', { params: { limit } }),
  getFriends: () => api.get('/leaderboard/friends'),
  getMyRank: () => api.get('/leaderboard/my-rank'),
  getTopLearners: (category: string, limit: number = 10) =>
    api.get('/leaderboard/top-learners', { params: { category, limit } }),
};

// Challenges API
export const challengesAPI = {
  getDaily: () => api.get('/challenges/daily'),
  getProgress: () => api.get('/challenges/progress'),
  updateProgress: (challengeId: string, increment: number = 1) =>
    api.post('/challenges/progress/update', null, { params: { challenge_id: challengeId, increment } }),
  getStreak: () => api.get('/challenges/streak'),
  updateStreak: () => api.post('/challenges/streak/update'),
};

// Sessions API
export const sessionsAPI = {
  start: (sessionType: string = 'mixed') =>
    api.post('/sessions/start', null, { params: { session_type: sessionType } }),
  end: (sessionId: string) => api.post(`/sessions/end/${sessionId}`),
  update: (sessionId: string, data: any) =>
    api.post(`/sessions/update/${sessionId}`, null, { params: data }),
  getActive: () => api.get('/sessions/active'),
  getHistory: (limit: number = 30) => api.get('/sessions/history', { params: { limit } }),
  getStats: () => api.get('/sessions/stats'),
};

// Categories API
export const categoriesAPI = {
  getAll: (params?: { difficulty_level?: string; is_active?: boolean }) =>
    api.get('/categories', { params }),
  getById: (id: string) => api.get(`/categories/${id}`),
  getProgress: () => api.get('/categories/progress/all'),
  getStats: (categoryId: string) => api.get(`/categories/stats/${categoryId}`),
  seed: () => api.post('/categories/seed'),
};

// Analytics API
export const analyticsAPI = {
  getDaily: (days: number = 30) => api.get('/analytics/daily', { params: { days } }),
  getWeekly: () => api.get('/analytics/weekly'),
  getMonthly: (month?: string) => api.get('/analytics/monthly', { params: { month } }),
  getHeatmap: (days: number = 365) => api.get('/analytics/heatmap', { params: { days } }),
  getPatterns: () => api.get('/analytics/patterns'),
  getPerformance: () => api.get('/analytics/performance'),
};

// Gamification API
export const gamificationAPI = {
  getAchievements: (showSecret: boolean = false) =>
    api.get('/gamification/achievements', { params: { show_secret: showSecret } }),
  getUnlockedAchievements: () => api.get('/gamification/achievements/unlocked'),
  getProgress: () => api.get('/gamification/achievements/progress'),
  checkAchievements: () => api.post('/gamification/achievements/check'),
  getBadges: () => api.get('/gamification/badges'),
  getTitles: () => api.get('/gamification/titles'),
  getCurrentTitle: () => api.get('/gamification/titles/current'),
  seedAchievements: () => api.post('/gamification/seed/achievements'),
  seedTitles: () => api.post('/gamification/seed/titles'),
};

// Social API
export const socialAPI = {
  // Friends
  getFriends: () => api.get('/social/friends'),
  sendFriendRequest: (userId: string) => api.post(`/social/friends/request/${userId}`),
  getIncomingRequests: () => api.get('/social/friends/requests/incoming'),
  acceptRequest: (requestId: string) => api.post(`/social/friends/requests/${requestId}/accept`),
  rejectRequest: (requestId: string) => api.post(`/social/friends/requests/${requestId}/reject`),
  removeFriend: (friendId: string) => api.delete(`/social/friends/${friendId}`),
  searchUsers: (query: string, limit: number = 20) =>
    api.get('/social/users/search', { params: { query, limit } }),

  // Activity Feed
  getFeed: (limit: number = 50) => api.get('/social/feed', { params: { limit } }),
  createPost: (data: { content: string; post_type?: string; metadata?: any }) =>
    api.post('/social/feed/post', data),
  likePost: (postId: string) => api.post(`/social/feed/post/${postId}/like`),
  commentPost: (postId: string, comment: string) =>
    api.post(`/social/feed/post/${postId}/comment`, null, { params: { comment } }),

  // Study Groups
  getGroups: () => api.get('/social/groups'),
  createGroup: (data: { name: string; description: string; is_private?: boolean; max_members?: number }) =>
    api.post('/social/groups', data),
  joinGroup: (groupId: string) => api.post(`/social/groups/${groupId}/join`),
  leaveGroup: (groupId: string) => api.post(`/social/groups/${groupId}/leave`),
};

// Users API
export const usersAPI = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data: any) => api.put('/users/me', data),
  getProgress: () => api.get('/users/me/progress'),
};

export default api;
