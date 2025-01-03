import axios from 'axios'
import { useStore } from 'vuex'
import router from '@/router'

// Nonaktifkan logging di production
if (import.meta.env.PROD) {
  axios.defaults.headers.common['X-Requested-With'] = null
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api',
  withCredentials: true,
  // Nonaktifkan logging di production
  ...(import.meta.env.PROD && {
    headers: {
      'X-Requested-With': null
    },
    silent: true
  })
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Jangan set Content-Type untuk FormData
    if (!(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json'
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Jika mendapat 401, clear store dan redirect ke login
      const store = useStore()
      await store.dispatch('logout')
      router.push('/login')
      return Promise.reject(error)
    }
    return Promise.reject(error)
  }
)

export default api
