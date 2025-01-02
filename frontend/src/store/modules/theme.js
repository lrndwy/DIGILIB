export default {
  state: {
    darkMode: localStorage.getItem('darkMode') === 'true'
  },
  mutations: {
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode
      localStorage.setItem('darkMode', state.darkMode)
      
      // Toggle kelas dark pada element html
      if (state.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  },
  actions: {
    initializeTheme({ state }) {
      if (state.darkMode) {
        document.documentElement.classList.add('dark')
      }
    }
  }
} 
