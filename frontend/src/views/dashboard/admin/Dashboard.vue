<template>
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Admin Dashboard
      </h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- Card Total User -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total User</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_users }}</template>
              </h3>
            </div>
            <div class="bg-primary-100 dark:bg-primary-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-primary-500 dark:text-primary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Card Total Guru -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total Guru</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_guru }}</template>
              </h3>
            </div>
            <div class="bg-success-100 dark:bg-success-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-success-500 dark:text-success-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Card Total Siswa -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total Siswa</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_siswa }}</template>
              </h3>
            </div>
            <div class="bg-accent-100 dark:bg-accent-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-accent-500 dark:text-accent-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- List Buku dan Sekolah -->
      <div class="mt-6 sm:mt-8 grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- List Buku Terbaru -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">Buku Terbaru</h2>
            <router-link 
              to="/dashboard/admin/buku"
              class="text-sm text-primary-500 hover:text-primary-600 dark:text-primary-400 dark:hover:text-primary-300"
            >
              Lihat Semua
            </router-link>
          </div>
          <div class="space-y-4 max-h-[400px] overflow-y-auto">
            <template v-if="loading">
              <div v-for="n in 5" :key="n" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded">
                <SkeletonLoader class="mr-4" width="40px" height="40px" circle />
                <div class="flex-1">
                  <SkeletonLoader class="mb-2" width="200px" />
                  <SkeletonLoader width="150px" />
                </div>
              </div>
            </template>
            <template v-else>
              <div v-for="buku in stats.latest_books" :key="buku.id" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded">
                <div class="mr-4">
                  <div class="w-10 h-10 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-text-light-primary dark:text-text-dark-primary">{{ buku.nama_buku }}</p>
                  <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                    {{ buku.mata_pelajaran_detail?.nama_mata_pelajaran }}
                  </p>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- List Sekolah -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">Sekolah Bekerja Sama</h2>
          </div>
          <div class="space-y-4 max-h-[400px] overflow-y-auto">
            <template v-if="loading">
              <div v-for="n in 5" :key="n" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded">
                <SkeletonLoader class="mr-4" width="40px" height="40px" circle />
                <div class="flex-1">
                  <SkeletonLoader class="mb-2" width="200px" />
                  <SkeletonLoader width="150px" />
                </div>
              </div>
            </template>
            <template v-else>
              <div v-for="sekolah in stats.latest_schools" :key="sekolah.id" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded">
                <div class="mr-4">
                  <div v-if="sekolah.logo" class="w-10 h-10 rounded-full overflow-hidden bg-white">
                    <img 
                      :src="getFullLogoUrl(sekolah.logo)" 
                      :alt="sekolah.nama_sekolah"
                      class="w-full h-full object-contain"
                      @error="handleImageError"
                    />
                  </div>
                  <div v-else class="w-10 h-10 bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-success-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-text-light-primary dark:text-text-dark-primary">{{ sekolah.nama_sekolah }}</p>
                  <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                    {{ sekolah.alamat }}
                  </p>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Aktivitas Terbaru -->
      <div class="mt-6 sm:mt-8">
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-6 border border-border-light dark:border-border-dark">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary">Aktivitas Terbaru</h2>
          <div class="space-y-4 max-h-[400px] overflow-y-auto">
            <template v-if="loading">
              <div v-for="n in 2" :key="n" class="flex items-center p-4 bg-gray-50 dark:bg-surface-dark rounded">
                <SkeletonLoader class="mr-4" width="40px" height="40px" circle />
                <div class="flex-1">
                  <SkeletonLoader class="mb-2" width="200px" />
                  <SkeletonLoader width="150px" />
                </div>
              </div>
            </template>
            <template v-else>
              <div v-for="activity in stats.latest_activities" :key="activity.id" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded mb-4">
                <div class="bg-primary-100 dark:bg-primary-900/30 p-2 rounded-full mr-4">
                  <svg class="w-4 h-4 text-primary-500 dark:text-primary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-text-light-primary dark:text-text-dark-primary">
                    {{ activity.message }}
                  </p>
                  <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                    {{ activity.time }}
                  </p>
                </div>
              </div>
              <div v-if="stats.latest_activities.length === 0" class="text-center text-gray-500 py-4">
                Tidak ada aktivitas
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/config/api'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()
const loading = ref(true)
const stats = ref({
  total_users: 0,
  total_guru: 0,
  total_siswa: 0,
  latest_activities: [],
  latest_books: [],
  latest_schools: []
})

const fetchStats = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    return
  }
  
  try {
    const response = await api.get('/dashboard/stats/')
    stats.value = response.data
  } catch (error) {
    if (error.response?.status === 401) {
      store.dispatch('logout')
    } else {
      console.error('Error fetching stats:', error)
    }
  } finally {
    loading.value = false
  }
}

watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    if (newPath === '/dashboard/admin') {
      fetchStats()
    }
  }
)

onMounted(() => {
  if (router.currentRoute.value.path === '/dashboard/admin') {
    fetchStats()
  }
})

const closeSidebar = () => {
  store.commit('setSidebarOpen', false)
}

const handleImageError = (event) => {
  const target = event.target
  const parent = target.parentElement
  
  // Hapus gambar yang error
  target.remove()
  
  // Tambahkan ikon default
  parent.innerHTML = `
    <div class="w-full h-full bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center">
      <svg class="w-6 h-6 text-success-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    </div>
  `
}

// Tambahkan fungsi untuk mendapatkan URL lengkap logo
const getFullLogoUrl = (logoUrl) => {
  if (!logoUrl) return null
  
  // Jika URL sudah lengkap (dimulai dengan http atau https), gunakan langsung
  if (logoUrl.startsWith('http')) {
    return logoUrl
  }
  
  // Jika URL relatif, tambahkan baseURL
  return import.meta.env.VITE_API_URL + logoUrl
}
</script>
