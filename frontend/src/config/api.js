import axios from 'axios'
import { useStore } from 'vuex'
import router from '@/router'

// Buat instance axios dengan konfigurasi dasar
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL.replace('http://', 'https://') + '/api',
  withCredentials: true,
  // Nonaktifkan logging di production
  ...(import.meta.env.PROD && {
    // Tambahkan konfigurasi untuk mematikan logging
    silent: true,
    headers: {
      'X-Requested-With': null,
      'Content-Type': null,
      'Authorization': null,
      'Accept': null,
      'X-CSRFToken': null,
    }
  })
})

// Tambahkan interceptor untuk mematikan console di production
if (import.meta.env.PROD) {
  const noop = () => {}
  console.log = noop
  console.error = noop
  console.warn = noop
  console.info = noop
  console.debug = noop
  
  api.interceptors.request.use((config) => {
    config.logging = false
    config.silent = true
    return config
  })

  api.interceptors.response.use((response) => {
    return response
  })
}

// Sisanya tetap sama
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
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
      const store = useStore()
      await store.dispatch('logout')
      router.push('/login')
      return Promise.reject(error)
    }
    return Promise.reject(error)
  }
)

export default api

