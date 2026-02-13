import axios from 'axios'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Search API
export const searchApi = {
  search: (query: string, maxResults: number = 10) =>
    apiClient.get(`/search?q=${encodeURIComponent(query)}&max_results=${maxResults}`)
}

// Playlist API
export const playlistApi = {
  getAll: () => apiClient.get('/playlists'),
  getById: (id: number) => apiClient.get(`/playlists/${id}`),
  create: (name: string) => apiClient.post('/playlists', { name }),
  delete: (id: number) => apiClient.delete(`/playlists/${id}`),
  addItem: (playlistId: number, videoId: string, title: string, duration?: number) =>
    apiClient.post(`/playlists/${playlistId}/items`, { videoId, title, duration }),
  removeItem: (playlistId: number, videoId: string) =>
    apiClient.delete(`/playlists/${playlistId}/items/${videoId}`)
}

// Recently Played API
export const recentlyPlayedApi = {
  getAll: (limit: number = 20) => apiClient.get(`/recently-played?limit=${limit}`),
  add: (videoId: string, title: string) =>
    apiClient.post('/recently-played', { videoId, title })
}

// Likes API
export const likesApi = {
  getAll: (limit: number = 100) => apiClient.get(`/likes?limit=${limit}`),
  add: (videoId: string, title: string) =>
    apiClient.post('/likes', { videoId, title }),
  remove: (videoId: string) => apiClient.delete(`/likes/${videoId}`),
  isLiked: (videoId: string) => apiClient.get(`/likes/${videoId}`)
}

// Download API
export const downloadApi = {
  download: (videoId: string, quality: string = '192k') =>
    apiClient.post('/download', { videoId, quality })
}

// Auth API
export const authApi = {
  login: (code: string) => apiClient.post('/auth/login', { code }),
  logout: () => apiClient.post('/auth/logout'),
  refresh: () => apiClient.post('/auth/refresh'),
  getUser: () => apiClient.get('/auth/user')
}

export default apiClient