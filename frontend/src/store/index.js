import { createStore } from 'vuex'
import api from '@/config/api'
import theme from './modules/theme'
import router from '@/router'

const store = createStore({
  modules: {
    theme
  },
  state: {
    user: null,
    token: localStorage.getItem('token') || null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login/', credentials)
        const { token, user } = response.data
        
        commit('setToken', token)
        commit('setUser', user)
        localStorage.setItem('userRole', user.role)
        
        return user
      } catch (error) {
        throw error
      }
    },
    
    async logout({ commit }) {
      try {
        commit('CLEAR_AUTH')
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    userRole: state => state.user?.role || localStorage.getItem('userRole')
  }
})



export default store 
