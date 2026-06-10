import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/accounts/auth/refresh/`, {
            refresh: refreshToken,
          })

          localStorage.setItem('access_token', response.data.access)
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

// Auth APIs
export const authAPI = {
  requestOTP: (phoneNumber) =>
    apiClient.post('/accounts/auth/request-otp/', { phone_number: phoneNumber }),

  verifyOTP: (phoneNumber, code) =>
    apiClient.post('/accounts/auth/verify-otp/', {
      phone_number: phoneNumber,
      code: code,
    }),

  logout: (refreshToken) =>
    apiClient.post('/accounts/auth/logout/', { refresh: refreshToken }),

  refreshToken: (refreshToken) =>
    apiClient.post('/accounts/auth/refresh/', { refresh: refreshToken }),

  getProfile: () => apiClient.get('/accounts/profile/'),

  updateProfile: (data) => apiClient.put('/accounts/profile/', data),
}

// Homework APIs
export const homeworkAPI = {
  listHomework: (params) => apiClient.get('/homework/', { params }),

  getHomework: (id) => apiClient.get(`/homework/${id}/`),

  createHomework: (data) => apiClient.post('/homework/', data),

  updateHomework: (id, data) => apiClient.put(`/homework/${id}/`, data),

  deleteHomework: (id) => apiClient.delete(`/homework/${id}/`),

  submitHomework: (homeworkId, data) =>
    apiClient.post(`/homework/${homeworkId}/submit/`, data),

  getSubmissions: (params) => apiClient.get('/submissions/', { params }),

  gradeSubmission: (submissionId, data) =>
    apiClient.put(`/submissions/${submissionId}/grade/`, data),
}

// Subject APIs
export const subjectAPI = {
  listSubjects: () => apiClient.get('/subjects/'),

  createSubject: (data) => apiClient.post('/subjects/', data),
}

// School APIs
export const schoolAPI = {
  listSchools: () => apiClient.get('/schools/'),

  getSchool: (id) => apiClient.get(`/schools/${id}/`),
}

// Class APIs
export const classAPI = {
  listClasses: (params) => apiClient.get('/classes/', { params }),

  getClass: (id) => apiClient.get(`/classes/${id}/`),
}

export default apiClient
