<template>
  <TransitionWrapper>
    <div class="p-8">
      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-text-light-primary dark:text-text-dark-primary mb-4">
          Dashboard Guru
        </h1>
      </div>

      <!-- Welcome Card -->
      <div class="bg-gradient-to-r from-blue-500 to-blue-700 dark:from-blue-700 dark:to-blue-900 p-4 sm:p-8 rounded-xl shadow-lg mb-8 text-white">
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <div class="p-3 sm:p-4 bg-white/20 rounded-full">
            <img 
              :src="fullProfileUrl"
              :alt="userInfo?.username"
              class="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover"
              @error="e => e.target.src = '/user-profile.jpg'"
            />
          </div>
          <div class="text-center sm:text-left">
            <h2 class="text-xl sm:text-2xl font-bold">
              {{ userInfo?.username || 'Selamat Datang' }} {{ statistics.nama_guru }}
            </h2>
            <p class="mt-1 text-sm sm:text-base text-blue-100">
              Guru {{ statistics.guru_nama_mata_pelajaran }}
            </p>
          </div>
        </div>
      </div>

      <!-- Statistik Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Buku Card -->
        <div class="bg-white dark:bg-surface-dark rounded-xl shadow-lg p-6 border border-border-light dark:border-border-dark transition-all hover:shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary">Total Buku</h3>
              <p class="text-3xl font-bold mt-2 text-text-light-primary dark:text-text-dark-primary">
                {{ statistics.totalBuku }}
              </p>
            </div>
            <div class="p-4 bg-blue-100 dark:bg-blue-900 rounded-full">
              <BookOpenIcon class="w-8 h-8 text-blue-600 dark:text-blue-300" />
            </div>
          </div>

        </div>

        <!-- Materi Card -->
        <div class="bg-white dark:bg-surface-dark rounded-xl shadow-lg p-6 border border-border-light dark:border-border-dark transition-all hover:shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary">Total Materi</h3>
              <p class="text-3xl font-bold mt-2 text-text-light-primary dark:text-text-dark-primary">
                {{ statistics.totalMateri }}
              </p>
            </div>
            <div class="p-4 bg-purple-100 dark:bg-purple-900 rounded-full">
              <DocumentTextIcon class="w-8 h-8 text-purple-600 dark:text-purple-300" />
            </div>
          </div>

        </div>

        <!-- Perangkat Card -->
        <div class="bg-white dark:bg-surface-dark rounded-xl shadow-lg p-6 border border-border-light dark:border-border-dark transition-all hover:shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary">Total Perangkat</h3>
              <p class="text-3xl font-bold mt-2 text-text-light-primary dark:text-text-dark-primary">
                {{ statistics.totalPerangkat }}
              </p>
            </div>
            <div class="p-4 bg-green-100 dark:bg-green-900 rounded-full">
              <ClipboardDocumentListIcon class="w-8 h-8 text-green-600 dark:text-green-300" />
            </div>
          </div>

        </div>
      </div>

      <!-- Carousel Sections -->
      <div class="space-y-8">
        <!-- Buku Terbaru -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary lg:text-3xl mx-4">
            Buku Terbaru
          </h2>
          <Swiper
            :modules="[Autoplay, Pagination]"
            :slides-per-view="1"
            :space-between="20"
            :autoplay="{ delay: 3000 }"
            :pagination="{ clickable: true }"
            :breakpoints="{
              '640': { slidesPerView: 2 },
              '768': { slidesPerView: 3 },
              '1024': { slidesPerView: 4 }
            }"
          >
            <template v-if="recentBuku.length === 0">
              <div class="w-full py-8 text-center text-text-light-secondary dark:text-text-dark-secondary">
                <DocumentTextIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p>Tidak ada buku yang tersedia</p>
              </div>
            </template>
            <template v-else>
              <SwiperSlide v-for="buku in recentBuku" :key="buku.id" class="pb-8 pt-2 px-2">
                <div 
                  class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
                  @click="viewBuku(buku)"
                >
                  <div class="aspect-[3/4] relative">
                    <template v-if="buku.file_buku">
                      <PDFCover :file-url="buku.file_buku" />
                    </template>
                    <template v-else>
                      <div class="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <DocumentTextIcon class="w-16 h-16 text-gray-400" />
                      </div>
                    </template>
                  </div>
                  <div class="p-4">
                    <h3 class="font-medium text-text-light-primary dark:text-text-dark-primary mb-2 line-clamp-2">
                      {{ buku.nama_buku }}
                    </h3>
                    <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                      {{ buku.mata_pelajaran_detail?.nama_mata_pelajaran }}
                    </p>
                  </div>
                </div>
              </SwiperSlide>
            </template>
          </Swiper>
        </div>

        <!-- Materi Terbaru -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary lg:text-3xl mx-4">
            Materi Terbaru
          </h2>
          <Swiper
            :modules="[Autoplay, Pagination]"
            :slides-per-view="1"
            :space-between="20"
            :autoplay="{ delay: 3500 }"
            :pagination="{ clickable: true }"
            :breakpoints="{
              '640': { slidesPerView: 2 },
              '768': { slidesPerView: 3 },
              '1024': { slidesPerView: 4 }
            }"
          >
            <template v-if="recentMateri.length === 0">
              <div class="w-full py-8 text-center text-text-light-secondary dark:text-text-dark-secondary">
                <DocumentTextIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p>Tidak ada materi yang tersedia</p>
              </div>
            </template>
            <template v-else>
              <SwiperSlide v-for="materi in recentMateri" :key="materi.id" class="pb-8 pt-2 px-2">
                <div 
                  class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
                  @click="viewMateri(materi)"
                >
                  <div class="aspect-[3/4] relative">
                    <template v-if="materi.file_materi">
                      <PDFCover :file-url="materi.file_materi" />
                    </template>
                    <template v-else>
                      <div class="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <DocumentTextIcon class="w-16 h-16 text-gray-400" />
                      </div>
                    </template>
                  </div>
                  <div class="p-4">
                    <h3 class="font-medium text-text-light-primary dark:text-text-dark-primary mb-2 line-clamp-2">
                      {{ materi.nama_materi }}
                    </h3>
                    <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                      {{ materi.mata_pelajaran_detail?.nama_mata_pelajaran }}
                    </p>
                  </div>
                </div>
              </SwiperSlide>
            </template>
          </Swiper>
        </div>

        <!-- Perangkat Terbaru -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary lg:text-3xl mx-4">
            Perangkat Terbaru
          </h2>
          <Swiper
            :modules="[Autoplay, Pagination]"
            :slides-per-view="1"
            :space-between="20"
            :autoplay="{ delay: 4000 }"
            :pagination="{ clickable: true }"
            :breakpoints="{
              '640': { slidesPerView: 2 },
              '768': { slidesPerView: 3 },
              '1024': { slidesPerView: 4 }
            }"
          >
            <template v-if="recentPerangkat.length === 0">
              <div class="w-full py-8 text-center text-text-light-secondary dark:text-text-dark-secondary">
                <ClipboardDocumentListIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p>Tidak ada perangkat yang tersedia</p>
              </div>
            </template>
            <template v-else>
              <SwiperSlide v-for="perangkat in recentPerangkat" :key="perangkat.id" class="pb-8 pt-2 px-2">
                <div 
                  class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 h-full"
                  @click="viewPerangkat(perangkat)"
                >
                  <div class="p-6">
                    <div class="flex items-center justify-between mb-4">
                      <div class="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                        <ClipboardDocumentListIcon class="w-8 h-8 text-green-600 dark:text-green-400" />
                      </div>
                    </div>
                    <h3 class="font-medium text-text-light-primary dark:text-text-dark-primary mb-3 line-clamp-2 text-lg">
                      {{ perangkat.nama_perangkat_kurikulum }}
                    </h3>
                    <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                      {{ perangkat.mata_pelajaran_detail?.nama_mata_pelajaran }}
                    </p>
                    <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
                      <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                        Dibuat: {{ new Date(perangkat.created_at).toLocaleDateString() }}
                      </p>
                    </div>
                  </div>
                </div>
              </SwiperSlide>
            </template>
          </Swiper>
        </div>
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import { 
  BookOpenIcon, 
  DocumentTextIcon, 
  ClipboardDocumentListIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  ChevronRightIcon 
} from '@heroicons/vue/24/outline'
import api from '@/config/api'
import { useRouter } from 'vue-router'
import PDFCover from '@/components/PDFCover.vue'


const store = useStore()

const userInfo = computed(() => {
  return store.state?.auth?.user || 
         store.state?.user || 
         store.state?.userData || 
         null
})

const fullProfileUrl = computed(() => {
  // Cek dari response dashboard terlebih dahulu
  if (statistics.value?.guru_profile) {
    if (statistics.value.guru_profile.startsWith('http')) {
      return statistics.value.guru_profile
    }
    return import.meta.env.VITE_API_URL + statistics.value.guru_profile
  }
  
  // Fallback ke user info jika tidak ada di response dashboard
  if (userInfo.value?.guru_profile) {
    if (userInfo.value.guru_profile.startsWith('http')) {
      return userInfo.value.guru_profile
    }
    return import.meta.env.VITE_API_URL + userInfo.value.guru_profile
  }

  return '/user-profile.jpg'
})

const statistics = ref({
  totalBuku: 0,
  totalMateri: 0,
  totalPerangkat: 0,
  bukuTrend: 0,
  materiTrend: 0,
  perangkatTrend: 0,
  guru_profile: null
})

const recentBuku = ref([])
const recentMateri = ref([])
const recentPerangkat = ref([])
const loading = ref(true)

const router = useRouter()

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/dashboard/guru/dashboard-statistics/')
    statistics.value = {
      ...response.data.statistics,
      guru_profile: response.data.guru_profile,
      nama_guru: response.data.guru_nama,
      username: response.data.guru_username,
      guru_nama_mata_pelajaran: response.data.guru_nama_mata_pelajaran.nama_mata_pelajaran
    }
    recentBuku.value = response.data.recent_buku
    recentMateri.value = response.data.recent_materi
    recentPerangkat.value = response.data.recent_perangkat

  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const viewBuku = (buku) => {
  router.push({
    name: 'BukuViewer',
    params: {
      bookId: buku.id,
      title: encodeURIComponent(buku.nama_buku)
    }
  })
}

const viewMateri = (materi) => {
  router.push({
    name: 'MateriViewer',
    params: {
      materiId: materi.id,
      title: encodeURIComponent(materi.nama_materi)
    }
  })
}

const viewPerangkat = (perangkat) => {
  router.push({
    name: 'PerangkatViewer',
    params: {
      perangkatId: perangkat.id,
      title: encodeURIComponent(perangkat.nama_perangkat_kurikulum)
    }
  })
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style>
.swiper {
  padding: 4px;
}

.swiper-pagination {
  position: relative;
  margin-top: 1rem;
}

.swiper-pagination-bullet {
  background: #cbd5e1;
}

.swiper-pagination-bullet-active {
  background: #3b82f6;
}

.dark .swiper-pagination-bullet {
  background: #475569;
}

.dark .swiper-pagination-bullet-active {
  background: #60a5fa;
}
</style>
