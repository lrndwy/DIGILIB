<template>
  <div class="flex h-screen bg-background-light dark:bg-background-dark">
    <!-- Bagian Kiri - Form Login -->
    <div class="w-full md:w-1/2 bg-surface-light dark:bg-surface-dark">
      <div class="flex items-center justify-center h-screen p-4">
        <div class="w-full max-w-md">
          
            <div class="p-8">
              <!-- Tambahkan tombol kembali di sini -->
              <div class="absolute top-4 left-4">
                <RouterLink
                  to="/"
                  class="flex items-center gap-2 text-text-light-secondary dark:text-text-dark-secondary hover:text-text-light-primary dark:hover:text-text-dark-primary transition-colors"
                >
                  <ArrowLeftIcon class="w-5 h-5" />
                  <span>Kembali ke Beranda</span>
                </RouterLink>
              </div>

              <!-- Header -->
              <div class="mb-8">
                <div class="flex items-center justify-between mb-4">
                  <!-- Logo dan Judul -->
                  <div class="flex items-center gap-3">
                    <img src="@/assets/digilib-logo.png" alt="Logo" class="w-12 h-12" />
                    <div class="flex flex-col">
                      <h2 class="text-3xl font-bold text-text-light-primary dark:text-text-dark-primary">
                        Digilib
                      </h2>
                      <p class="text-center text-text-light-secondary dark:text-text-dark-secondary">
                        Silakan login untuk melanjutkan
                      </p>
                    </div>
                    
                  </div>
                  
                  <!-- Toggle Theme Button -->
                  <button 
                    @click="toggleTheme"
                    class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-surface-dark"
                  >
                    <SunIcon v-if="isDarkMode" class="h-6 w-6 text-yellow-300 transition-transform duration-300 transform rotate-0" />
                    <MoonIcon v-else class="h-6 w-6 text-gray-700 transition-transform duration-300 transform rotate-0" />
                  </button>
                </div>
                
              </div>

              <!-- Form -->
              <form @submit.prevent="handleLogin" class="space-y-6">
                <!-- Username Field -->
                <div class="space-y-2">
                  <label class="text-sm font-medium text-text-light-primary dark:text-text-dark-primary">
                    Username
                  </label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-text-light-secondary dark:text-text-dark-secondary">
                      <UserIcon class="w-5 h-5" />
                    </span>
                    <input
                      v-model="credentials.username"
                      type="text"
                      required
                      class="w-full pl-10 pr-4 py-3 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200 text-text-light-primary dark:text-text-dark-primary placeholder-text-light-disabled dark:placeholder-text-dark-disabled"
                      :class="{'border-red-500/50 focus:ring-red-500/50': error}"
                      placeholder="Masukkan username"
                    >
                  </div>
                </div>

                <!-- Password Field -->
                <div class="space-y-2">
                  <label class="text-sm font-medium text-text-light-primary dark:text-text-dark-primary">
                    Password
                  </label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-text-light-secondary dark:text-text-dark-secondary">
                      <LockClosedIcon class="w-5 h-5" />
                    </span>
                    <input
                      v-model="credentials.password"
                      :type="showPassword ? 'text' : 'password'"
                      required
                      class="w-full pl-10 pr-12 py-3 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200 text-text-light-primary dark:text-text-dark-primary placeholder-text-light-disabled dark:placeholder-text-dark-disabled"
                      :class="{'border-red-500/50 focus:ring-red-500/50': error}"
                      placeholder="Masukkan password"
                    >
                    <button 
                      type="button"
                      @click="togglePassword"
                      class="absolute inset-y-0 right-0 flex items-center pr-3 text-text-light-secondary dark:text-text-dark-secondary hover:text-text-light-primary dark:hover:text-text-dark-primary transition-colors"
                    >
                      <EyeIcon v-if="showPassword" class="w-5 h-5" />
                      <EyeSlashIcon v-else class="w-5 h-5" />
                    </button>
                  </div>
                </div>

                <!-- Error Message -->
                <Transition
                  enter-active-class="transition duration-200 ease-out"
                  enter-from-class="transform -translate-y-1 opacity-0"
                  enter-to-class="transform translate-y-0 opacity-100"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="transform translate-y-0 opacity-100"
                  leave-to-class="transform -translate-y-1 opacity-0"
                >
                  <div v-if="error" class="bg-red-500/10 text-red-500 dark:text-red-400 p-4 rounded-xl text-sm">
                    {{ error }}
                  </div>
                </Transition>

                <!-- Login Button -->
                <button
                  type="submit"
                  :disabled="loading"
                  class="relative w-full py-3 px-6 bg-primary-600 dark:bg-primary-500 text-white rounded-xl font-medium overflow-hidden transition-all duration-300 hover:bg-primary-700 dark:hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div class="relative flex items-center justify-center gap-2">
                    <!-- Loading Spinner -->
                    <svg 
                      v-if="loading" 
                      class="animate-spin w-5 h-5" 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24"
                    >
                      <circle 
                        class="opacity-25" 
                        cx="12" 
                        cy="12" 
                        r="10" 
                        stroke="currentColor" 
                        stroke-width="4"
                      />
                      <path 
                        class="opacity-75" 
                        fill="currentColor" 
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    <span>{{ loading ? 'Memproses...' : 'Login' }}</span>
                  </div>
                </button>
              </form>
            </div>

        </div>
      </div>
    </div>

    <!-- Bagian Kanan - Background Image -->
    <div class="hidden md:block md:w-1/2 relative">
      <div class="absolute inset-0 bg-gradient-to-br from-gray-900/80 to-transparent z-10"></div>
      
      <!-- Tambahkan teks di sini -->
      <div class="absolute inset-x-0 top-1/3 text-start z-20 px-6">
        <div class="flex items-center gap-3">

          <div class="px-9">
            <h1 class="text-3xl md:text-4xl lg:text-7xl font-bold text-white mb-2 md:mb-4 leading-tight">
              Digitalisasi Pendidikan
            </h1>
            <h2 class="text-xl md:text-2xl lg:text-7xl font-semibold text-white/90">
              untuk Bangsa
            </h2>
          </div>

        </div>
      </div>

      <div 
        class="h-full w-full bg-cover bg-center bg-no-repeat"
        :style="{ backgroundImage: `url(${loginImage})` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  UserIcon, 
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
  SunIcon,
  MoonIcon,
  ArrowLeftIcon
} from '@heroicons/vue/24/outline'
import loginImage from '@/assets/login-image.jpeg'

const store = useStore()
const router = useRouter()
const isDarkMode = computed(() => store.state.theme.darkMode)

const credentials = ref({
  username: '',
  password: ''
})

const error = ref('')
const loading = ref(false)
const showPassword = ref(false)
const rememberMe = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const user = await store.dispatch('login', {
      username: credentials.value.username,
      password: credentials.value.password
    })
    
    if (rememberMe.value) {
      localStorage.setItem('remember_credentials', JSON.stringify({
        username: credentials.value.username
      }))
    }
    
    localStorage.setItem('user_id', user.id)
    
    if (user && user.role) {
      router.push(`/dashboard/${user.role}`)
    } else {
      error.value = 'Data pengguna tidak valid'
    }
  } catch (err) {
    error.value = 'Username atau password salah'
  } finally {
    loading.value = false
  }
}

// Load remembered credentials if exists
const loadRememberedCredentials = () => {
  const remembered = localStorage.getItem('remember_credentials')
  if (remembered) {
    const { username } = JSON.parse(remembered)
    credentials.value.username = username
    rememberMe.value = true
  }
}

loadRememberedCredentials()

const toggleTheme = () => {
  store.commit('toggleDarkMode')
}
</script>

<style scoped>
/* Tambahkan animasi rotasi */
.sun-icon-enter-active, .moon-icon-enter-active {
  transition: transform 0.3s ease;
}
.sun-icon-leave-active, .moon-icon-leave-active {
  transition: transform 0.3s ease;
}
.sun-icon-enter, .moon-icon-leave-to {
  transform: rotate(180deg);
}
.moon-icon-enter, .sun-icon-leave-to {
  transform: rotate(-180deg);
}

/* Tambahkan style untuk animasi form */
.form-enter-active {
  transition: all 0.5s ease-out;
}

.form-leave-active {
  transition: all 0.2s ease-in;
}

.form-enter-from,
.form-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
