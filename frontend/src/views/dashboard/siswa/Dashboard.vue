<template>
  <TransitionWrapper>
    <div class="p-8">
      <!-- Header Section dengan Stats -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-text-light-primary dark:text-text-dark-primary mb-4">
          Dashboard Siswa
        </h1>
      </div>

      <!-- Info Siswa Card -->
      <div class="bg-gradient-to-r from-blue-500 to-blue-700 dark:from-blue-700 dark:to-blue-900 p-4 sm:p-6 md:p-8 rounded-xl shadow-lg mb-8 text-white">
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <div class="p-3 sm:p-4 bg-white/20 rounded-full">
            <img 
              :src="fullProfileUrl"
              :alt="dashboardData?.siswa?.nama_siswa"
              class="w-16 h-16 sm:w-12 sm:h-12 rounded-full object-cover"
              @error="e => e.target.src = '/user-profile.jpg'"
            />
          </div>
          <div class="text-center sm:text-left">
            <h2 class="text-xl sm:text-2xl font-bold">
              {{ dashboardData?.siswa?.nama_siswa }}
            </h2>
            <p class="mt-1 text-blue-100 text-sm sm:text-base">
              Kelas {{ dashboardData?.siswa?.kelas?.nama_kelas }} - 
              {{ dashboardData?.siswa?.jenjang?.nama_jenjang }}
            </p>
          </div>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="mb-6 flex flex-wrap gap-4">
        <div class="relative flex-1 min-w-[200px]">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari buku atau materi..."
            class="w-full px-4 py-2 pr-10 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
          />
          <MagnifyingGlassIcon class="w-5 h-5 absolute right-3 top-2.5 text-gray-400" />
        </div>
        
        <select
          v-model="selectedMapel"
          class="px-4 py-2 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
        >
          <option value="">Semua Mata Pelajaran</option>
          <option v-for="mapel in mapelList" :key="mapel.id" :value="mapel.id">
            {{ mapel.nama_mata_pelajaran }}
          </option>
        </select>
      </div>

      <!-- Buku Section -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary lg:text-3xl mx-4">
          Buku Terbaru
        </h2>
        <Swiper
          :modules="[SwiperAutoplay, SwiperPagination]"
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
          <template v-if="filteredBuku.length === 0">
            <div class="w-full py-8 text-center text-text-light-secondary dark:text-text-dark-secondary">
              <DocumentTextIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p>Tidak ada buku yang tersedia</p>
            </div>
          </template>
          <template v-else>
            <SwiperSlide v-for="buku in filteredBuku" :key="buku.id" class="pb-8 pt-2 px-2">
              <div 
                class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
                @click="showDetail({...buku, type: 'buku'})"
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

      <!-- Materi Section -->
      <div class="mb-4">
        <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary lg:text-3xl mx-4">
          Materi Terbaru
        </h2>
        <Swiper
          :modules="[SwiperAutoplay, SwiperPagination]"
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
          <template v-if="filteredMateri.length === 0">
            <div class="w-full py-8 text-center text-text-light-secondary dark:text-text-dark-secondary">
              <DocumentTextIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p>Tidak ada materi yang tersedia</p>
            </div>
          </template>
          <template v-else>
            <SwiperSlide v-for="materi in filteredMateri" :key="materi.id" class="pb-8 pt-2 px-2">
              <div 
                class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
                @click="showDetail({...materi, type: 'materi'})"
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
                  <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary mt-1">
                    Guru: {{ materi.guru_detail?.username }}
                  </p>
                </div>
              </div>
            </SwiperSlide>
          </template>
        </Swiper>
      </div>

      <!-- Modal Detail -->
      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            {{ selectedItem?.type === 'buku' ? 'Detail Buku' : 'Detail Materi' }}
          </div>
        </template>
        <template #body>
          <div v-if="selectedItem" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <!-- Cover -->
              <div class="w-full flex justify-center mb-4">
                <div class="w-32 h-48">
                  <template v-if="selectedItem.file_buku || selectedItem.file_materi">
                    <PDFCover :file-url="selectedItem.file_buku || selectedItem.file_materi" />
                  </template>
                  <template v-else>
                    <div class="w-full h-full bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                      <DocumentTextIcon class="w-12 h-12 text-gray-400" />
                    </div>
                  </template>
                </div>
              </div>

              <!-- Informasi -->
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Nama:</div>
                <div class="w-1/2">{{ selectedItem.type === 'buku' ? selectedItem.nama_buku : selectedItem.nama_materi }}</div>
              </div>

              <div class="w-full flex">
                <div class="w-1/2 font-medium">Mata Pelajaran:</div>
                <div class="w-1/2">{{ selectedItem.mata_pelajaran_detail?.nama_mata_pelajaran }}</div>
              </div>

              <div v-if="selectedItem.type === 'materi'" class="w-full flex">
                <div class="w-1/2 font-medium">Guru:</div>
                <div class="w-1/2">{{ selectedItem.guru_detail?.username }}</div>
              </div>
            </div>

            <!-- Tombol Baca -->
            <div class="flex justify-center mt-6">
              <button
                @click="readItem(selectedItem, selectedItem.type)"
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2"
              >
                <BookOpenIcon class="w-5 h-5" />
                Baca {{ selectedItem.type === 'buku' ? 'Buku' : 'Materi' }}
              </button>
            </div>
          </div>
        </template>
      </BaseModal>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import { DocumentTextIcon, BookOpenIcon, UserIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import PDFCover from '@/components/PDFCover.vue'
import api from '@/config/api'
import { useRouter } from 'vue-router'
import BaseModal from '@/components/BaseModal.vue'

const store = useStore()
const dashboardData = ref(null)
const SwiperAutoplay = Autoplay
const SwiperPagination = Pagination
const router = useRouter()

// Tambahkan state
const showDetailModal = ref(false)
const selectedItem = ref(null)
const searchQuery = ref('')
const selectedMapel = ref('')
const mapelList = ref([])

// Computed untuk filtering
const filteredBuku = computed(() => {
  let result = dashboardData.value?.buku || []
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(buku => 
      buku.nama_buku.toLowerCase().includes(query)
    )
  }
  
  if (selectedMapel.value) {
    result = result.filter(buku => 
      buku.mata_pelajaran_detail?.id === selectedMapel.value
    )
  }
  
  return result
})

const filteredMateri = computed(() => {
  let result = dashboardData.value?.materi || []
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(materi => 
      materi.nama_materi.toLowerCase().includes(query)
    )
  }
  
  if (selectedMapel.value) {
    result = result.filter(materi => 
      materi.mata_pelajaran_detail?.id === selectedMapel.value
    )
  }
  
  return result
})

const fullProfileUrl = computed(() => {
  // Jika tidak ada foto profil, gunakan default
  if (!dashboardData.value?.siswa?.foto_profil_url) {
    return '/user-profile.jpg'
  }
  
  // Jika URL sudah lengkap (dimulai dengan http atau https), gunakan langsung
  if (dashboardData.value.siswa.foto_profil_url.startsWith('http')) {
    return dashboardData.value.siswa.foto_profil_url
  }
  
  // Jika URL relatif, tambahkan baseURL
  return `${import.meta.env.VITE_API_URL}${dashboardData.value.siswa.foto_profil_url}`
})

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/siswa/dashboard_statistics/')
    if (response.data?.siswa) {
      dashboardData.value = response.data
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal memuat data dashboard'
    })
  }
}

// Fungsi untuk menampilkan detail
const showDetail = (item) => {
  selectedItem.value = item
  showDetailModal.value = true
}

// Fungsi untuk membaca buku/materi
const readItem = (item, type) => {
  router.push({
    name: type === 'buku' ? 'BukuViewer' : 'MateriViewer',
    params: {
      [type === 'buku' ? 'bookId' : 'materiId']: item.id,
      title: encodeURIComponent(type === 'buku' ? item.nama_buku : item.nama_materi)
    }
  })
}

// Fetch data mapel
const fetchMapelList = async () => {
  try {
    const response = await api.get('/mata-pelajaran/')
    mapelList.value = response.data
  } catch (error) {
    console.error('Error fetching mapel:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    fetchDashboardData(),
    fetchMapelList()
  ])
})
</script>
