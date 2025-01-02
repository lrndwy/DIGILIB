<template>
  <div class="min-h-screen bg-gradient-to-b from-background-light to-surface-light dark:from-background-dark dark:to-surface-dark">
    <!-- Navbar -->
    <nav class="fixed w-full z-50 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md border-b border-gray-200 dark:border-border-dark">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo & Brand -->
          <div class="flex items-center gap-3">
            <img src="@/assets/digilib-logo.png" alt="Logo" class="w-8 h-8" />
            <span class="text-xl font-bold text-text-light-primary dark:text-text-dark-primary">
              Digilib
            </span>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:flex items-center gap-6">
            <a href="#beranda" class="text-text-light-primary dark:text-text-dark-primary hover:text-primary-500">Beranda</a>
            <a href="#fitur" class="text-text-light-primary dark:text-text-dark-primary hover:text-primary-500">Fitur</a>
            <a href="#tentang" class="text-text-light-primary dark:text-text-dark-primary hover:text-primary-500">Tentang</a>
            <a href="#kontak" class="text-text-light-primary dark:text-text-dark-primary hover:text-primary-500">Kontak</a>
          </div>

          <!-- Auth Buttons -->
          <div class="flex items-center gap-4">
            <RouterLink 
              to="/login"
              class="px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors"
            >
              Masuk
            </RouterLink>
            
            <!-- Theme Toggle -->
            <button 
              @click="toggleTheme"
              class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-surface-dark"
            >
              <SunIcon v-if="isDarkMode" class="h-5 w-5 text-yellow-300" />
              <MoonIcon v-else class="h-5 w-5 text-gray-700" />
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section id="beranda" class="pt-32 pb-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-8">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-text-light-primary dark:text-text-dark-primary leading-tight">
              Perpustakaan Digital untuk 
              <span class="text-primary-500">Masa Depan Pendidikan</span>
            </h1>
            <p class="text-lg text-text-light-secondary dark:text-text-dark-secondary">
              Akses ribuan buku informatika dan materi pembelajaran berkualitas untuk setiap jenjang pendidikan. Belajar lebih mudah dan efektif dengan platform digital modern.
            </p>
            <div class="flex flex-wrap gap-4">
              <RouterLink 
                to="/login"
                class="px-6 py-3 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors"
              >
                Mulai Sekarang
              </RouterLink>
              <a 
                href="#fitur"
                class="px-6 py-3 rounded-lg border border-primary-500 text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              >
                Pelajari Lebih Lanjut
              </a>
            </div>
          </div>
          
          <!-- Hero Image -->
          <div class="relative">
            <img 
              src="@/assets/hero-image.jpg" 
              alt="Hero Image"
              class="w-full h-auto rounded-3xl shadow-xl"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="fitur" class="py-20 bg-surface-light dark:bg-surface-dark">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-text-light-primary dark:text-text-dark-primary mb-4">
            Fitur Unggulan
          </h2>
          <p class="text-lg text-text-light-secondary dark:text-text-dark-secondary">
            Nikmati berbagai fitur yang memudahkan proses belajar mengajar
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Feature Cards -->
          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <BookOpenIcon class="w-12 h-12 text-primary-500 mb-4" />
            <h3 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Perpustakaan Digital
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              Akses ribuan buku informatika dan materi pembelajaran sesuai jenjang pendidikan
            </p>
          </div>

          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <UserGroupIcon class="w-12 h-12 text-primary-500 mb-4" />
            <h3 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Kolaborasi Guru
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              Para guru dapat berbagi materi dan bahan ajar dengan mudah
            </p>
          </div>

          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <AcademicCapIcon class="w-12 h-12 text-primary-500 mb-4" />
            <h3 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Pembelajaran Terstruktur
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              Materi pembelajaran yang sesuai dengan kurikulum dan jenjang pendidikan
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="tentang" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- About Image -->
          <div class="relative">
            <img 
              src="@/assets/about-image.jpg" 
              alt="About Image"
              class="w-full h-auto rounded-3xl shadow-xl"
            />
          </div>
          
          <div class="space-y-6">
            <h2 class="text-3xl sm:text-4xl font-bold text-text-light-primary dark:text-text-dark-primary">
              Tentang Digilib
            </h2>
            <p class="text-lg text-text-light-secondary dark:text-text-dark-secondary">
              Digilib adalah platform perpustakaan digital yang dirancang khusus untuk mendukung pendidikan di Indonesia. Kami berkomitmen untuk menyediakan akses ke sumber daya pembelajaran berkualitas tinggi bagi siswa dan guru.
            </p>
            <div class="space-y-4">
              <div class="flex items-start gap-4">
                <div class="p-2 bg-primary-500/10 rounded-lg">
                  <BookOpenIcon class="w-6 h-6 text-primary-500" />
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary">
                    Koleksi Digital Lengkap
                  </h3>
                  <p class="text-text-light-secondary dark:text-text-dark-secondary">
                    Ribuan buku dan materi pembelajaran dalam format digital
                  </p>
                </div>
              </div>
              <div class="flex items-start gap-4">
                <div class="p-2 bg-primary-500/10 rounded-lg">
                  <AcademicCapIcon class="w-6 h-6 text-primary-500" />
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary">
                    Kurikulum Terstruktur
                  </h3>
                  <p class="text-text-light-secondary dark:text-text-dark-secondary">
                    Materi pembelajaran sesuai dengan kurikulum nasional
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Koleksi Buku Terbaru -->
    <section class="py-20 bg-surface-light dark:bg-surface-dark">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-text-light-primary dark:text-text-dark-primary mb-4">
            Koleksi Buku Terbaru
          </h2>
          <p class="text-lg text-text-light-secondary dark:text-text-dark-secondary">
            Temukan berbagai buku pembelajaran berkualitas
          </p>
        </div>

        <!-- Carousel -->
        <div class="relative">
          <!-- Prev Button -->
          <button 
            @click="prevSlide"
            class="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-white/80 dark:bg-background-dark/80 shadow-lg hover:bg-white dark:hover:bg-background-dark"
          >
            <ChevronLeftIcon class="w-6 h-6 text-text-light-primary dark:text-text-dark-primary" />
          </button>

          <!-- Carousel Container -->
          <div class="overflow-hidden">
            <div 
              class="flex transition-transform duration-500 ease-in-out"
              :style="{ transform: `translateX(-${currentSlide * (100 / itemsPerSlide)}%)` }"
            >
              <div 
                v-for="buku in bukuList" 
                :key="buku.id"
                class="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 flex-shrink-0 px-4"
              >
                <div class="bg-white dark:bg-background-dark rounded-xl shadow-lg overflow-hidden mb-6">
                  <!-- Cover Buku -->
                  <div class="aspect-[3/4] relative">
                    <template v-if="buku.file_buku.endsWith('.pdf')">
                      <PDFCover :file-url="buku.file_buku" />
                    </template>
                    <template v-else>
                      <div class="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                        <DocumentTextIcon class="w-16 h-16 text-gray-400" />
                      </div>
                    </template>
                  </div>
                  
                  <!-- Info Buku -->
                  <div class="p-4">
                    <h3 class="font-semibold text-text-light-primary dark:text-text-dark-primary mb-1 truncate">
                      {{ buku.nama_buku }}
                    </h3>
                    <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary mb-2">
                      {{ buku.penerbit }}
                    </p>
                    <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                      {{ buku.mata_pelajaran_detail?.nama_mata_pelajaran }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Next Button -->
          <button 
            @click="nextSlide"
            class="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-white/80 dark:bg-background-dark/80 shadow-lg hover:bg-white dark:hover:bg-background-dark"
          >
            <ChevronRightIcon class="w-6 h-6 text-text-light-primary dark:text-text-dark-primary" />
          </button>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="kontak" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-text-light-primary dark:text-text-dark-primary mb-4">
            Hubungi Kami
          </h2>
          <p class="text-lg text-text-light-secondary dark:text-text-dark-secondary max-w-2xl mx-auto">
            Punya pertanyaan atau ingin berkolaborasi? Jangan ragu untuk menghubungi kami
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Email -->
          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg text-center">
            <div class="w-12 h-12 bg-primary-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <EnvelopeIcon class="w-6 h-6 text-primary-500" />
            </div>
            <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Email
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              support@Digilib
            </p>
          </div>

          <!-- Phone -->
          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg text-center">
            <div class="w-12 h-12 bg-primary-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <PhoneIcon class="w-6 h-6 text-primary-500" />
            </div>
            <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Telepon
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              +62 812 3456 7890
            </p>
          </div>

          <!-- Location -->
          <div class="p-6 bg-white dark:bg-background-dark rounded-xl shadow-lg text-center">
            <div class="w-12 h-12 bg-primary-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <MapPinIcon class="w-6 h-6 text-primary-500" />
            </div>
            <h3 class="text-lg font-semibold text-text-light-primary dark:text-text-dark-primary mb-2">
              Alamat
            </h3>
            <p class="text-text-light-secondary dark:text-text-dark-secondary">
              Jakarta, Indonesia
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-4 bg-surface-light dark:bg-surface-dark">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div class="p-6">
            <div class="text-4xl font-bold text-primary-500 mb-2">
              {{ stats.books.toLocaleString() }}+
            </div>
            <div class="text-text-light-secondary dark:text-text-dark-secondary">Buku Digital</div>
          </div>
          <div class="p-6">
            <div class="text-4xl font-bold text-primary-500 mb-2">
              {{ stats.schools.toLocaleString() }}+
            </div>
            <div class="text-text-light-secondary dark:text-text-dark-secondary">Sekolah Mitra</div>
          </div>
          <div class="p-6">
            <div class="text-4xl font-bold text-primary-500 mb-2">
              {{ stats.users.toLocaleString() }}+
            </div>
            <div class="text-text-light-secondary dark:text-text-dark-secondary">Pengguna Aktif</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-primary-500">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-white mb-8">
          Bergabung dengan Digilib Sekarang
        </h2>
        <p class="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
          Hubungi kami untuk informasi kerjasama dan menjadi bagian dari revolusi pendidikan digital
        </p>
        <a 
          href="https://api.whatsapp.com/send/?phone=6285158084431&text=Chat+Us+Now%21&type=phone_number&app_absent=0"
          class="inline-block px-8 py-4 bg-white text-primary-500 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
        >
          Hubungi Kami
      </a>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-background-dark text-text-dark-secondary py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center gap-3 mb-4">
              <img src="@/assets/digilib-logo.png" alt="Logo" class="w-8 h-8" />
              <span class="text-xl font-bold text-white">Digilib</span>
            </div>
            <p class="text-sm">
              Platform perpustakaan digital untuk masa depan pendidikan Indonesia
            </p>
          </div>
          
          <!-- Footer Links -->
          <div>
            <h3 class="text-white font-semibold mb-4">Layanan</h3>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-white transition-colors">Perpustakaan Digital</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Manajemen Materi</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Kerjasama Sekolah</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-white font-semibold mb-4">Perusahaan</h3>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-white transition-colors">Tentang Kami</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Karir</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-white font-semibold mb-4">Kontak</h3>
            <ul class="space-y-2">
              <li>support@Digilib</li>
              <li>+62 812 3456 7890</li>
              <li>Jakarta, Indonesia</li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-border-dark mt-12 pt-8 text-center text-sm">
          © 2024 Digilib. All rights reserved.
        </div>
      </div>
    </footer>


  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { 
  SunIcon, 
  MoonIcon,
  BookOpenIcon,
  UserGroupIcon,
  AcademicCapIcon,
  EnvelopeIcon,
  PhoneIcon,
  MapPinIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'
import PDFCover from '@/components/PDFCover.vue'
import api from '@/config/api'

const isDarkMode = ref(false)
const stats = ref({
  books: 0,
  schools: 0,
  users: 0
})

const animateValue = (start, end, duration, target) => {
  const range = end - start
  const increment = end > start ? 1 : -1
  const stepTime = Math.abs(Math.floor(duration / range))
  
  let current = start
  const timer = setInterval(() => {
    current += increment
    stats.value[target] = current
    if (current === end) {
      clearInterval(timer)
    }
  }, stepTime)
}

const startCounters = () => {
  animateValue(0, 1000, 2000, 'books')
  animateValue(0, 50, 1500, 'schools')
  animateValue(0, 10000, 2500, 'users')
}

onMounted(() => {
  // Mulai animasi ketika komponen dimount
  startCounters()
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark')
}

// State untuk carousel
const bukuList = ref([])
const currentSlide = ref(0)
const itemsPerSlide = ref(4) // Jumlah item yang ditampilkan per slide

// Fungsi untuk mengambil data buku
const fetchBuku = async () => {
  try {
    const response = await api.get('/buku/public/')
    // Filter buku yang sekolahnya null atau kosong
    bukuList.value = response.data.filter(buku => !buku.sekolah)
  } catch (error) {
    console.error('Error fetching buku:', error)
  }
}

// Fungsi navigasi carousel
const nextSlide = () => {
  const maxSlide = Math.ceil(bukuList.value.length / itemsPerSlide.value) - 1
  currentSlide.value = currentSlide.value >= maxSlide ? 0 : currentSlide.value + 1
}

const prevSlide = () => {
  const maxSlide = Math.ceil(bukuList.value.length / itemsPerSlide.value) - 1
  currentSlide.value = currentSlide.value <= 0 ? maxSlide : currentSlide.value - 1
}

// Responsive itemsPerSlide
const updateItemsPerSlide = () => {
  if (window.innerWidth < 640) {
    itemsPerSlide.value = 1
  } else if (window.innerWidth < 768) {
    itemsPerSlide.value = 2
  } else if (window.innerWidth < 1024) {
    itemsPerSlide.value = 3
  } else {
    itemsPerSlide.value = 4
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchBuku()
  updateItemsPerSlide()
  window.addEventListener('resize', updateItemsPerSlide)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateItemsPerSlide)
})
</script>

<style>
/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 10px;
  background-color: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.5);
}

/* Untuk Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.3) transparent;
}
</style>
