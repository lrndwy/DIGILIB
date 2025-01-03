<template>
  <BaseModal v-model="showLogoutModal">
    <template #header>
      Konfirmasi Logout
    </template>
    
    <template #body>
      <p>Apakah Anda yakin ingin keluar dari aplikasi?</p>
    </template>
    
    <template #footer>
      <button
        @click="showLogoutModal = false"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        Batal
      </button>
      <button
        @click="confirmLogout"
        class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Ya, Logout
      </button>
    </template>
  </BaseModal>

  <!-- Sidebar -->
  <div 
    class="fixed left-0 z-40 w-64 pt-5 bg-background-light dark:bg-surface-dark transform transition-transform duration-150 ease-in-out lg:translate-x-0 top-0 h-screen overflow-y-auto flex flex-col justify-between"
    :class="[isOpen ? 'translate-x-0' : '-translate-x-full']"
  >
    <nav class="mt-2 px-3 lg:px-4 space-y-1">
      <div class="flex p-2 gap-2 items-center mb-2">
        <img src="@/assets/digilib-logo.png" alt="Logo" class="w-8 h-8">
        <div class="flex flex-col ml-2">
          <span class="text-black dark:text-text-dark-primary rounded-md text-md font-bold truncate max-w-[200px] lg:max-w-none">
            Diginusa Library
          </span>
          <p class="text-xs text-gray-500 dark:text-text-dark-secondary">
            Perpustakaan Digital
          </p>
        </div>
      </div>
      <div class="border-t border-gray-400 pb-2"></div>
      <!-- Menu items dengan padding yang disesuaikan -->
      <router-link 
        :to="`/dashboard/${userRole}`"
        :class="[
          $route.path === `/dashboard/${userRole}`
            ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
            : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        ]"
        @click="closeSidebarOnMobile"
      >
        <component 
          :is="DashboardIcon"
          :class="[
            $route.path === `/dashboard/${userRole}`
              ? 'text-secondary-700 dark:text-white'
              : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
            'mr-3 h-6 w-6'
          ]"
          aria-hidden="true"
        />
        Dashboard
      </router-link>

      <!-- Menu Admin -->
      <template v-if="userRole === 'admin'">
        <div v-for="menu in adminMenus" :key="menu.name" class="mb-2">
          <!-- Menu Header -->
          <button
            @click="toggleMenu(menu)"
            class="w-full flex items-center justify-between px-2 py-2 text-sm font-medium rounded-md transition-colors duration-150"
            :class="{
              'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white': isActiveMenu(menu),
              'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark': !isActiveMenu(menu)
            }"
          >
            <div class="flex items-center">
              <component
                :is="menu.icon"
                class="h-5 w-5 mr-3"
                :class="{
                  'text-secondary-700 dark:text-white': isActiveMenu(menu),
                  'text-gray-400': !isActiveMenu(menu)
                }"
              />
              {{ menu.name }}
            </div>
            <ChevronRightIcon
              class="h-4 w-4 transition-transform duration-200"
              :class="{
                'rotate-90': menu.isOpen,
                'text-secondary-700': isActiveMenu(menu),
                'text-gray-400': !isActiveMenu(menu)
              }"
            />
          </button>

          <!-- Submenu Items dengan transition -->
          <transition
            enter-active-class="transition-all duration-300 ease-out"
            leave-active-class="transition-all duration-300 ease-in"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-[500px]"
            leave-from-class="opacity-100 max-h-[500px]"
            leave-to-class="opacity-0 max-h-0"
          >
            <div
              v-show="menu.isOpen"
              class="overflow-hidden"
            >
              <div class="mt-1 ml-3 space-y-1">
                <router-link
                  v-for="subMenu in menu.subMenus"
                  :key="subMenu.path"
                  :to="subMenu.path"
                  class="flex items-center px-2 py-2 text-sm rounded-md transition-colors duration-150"
                  :class="{
                    'bg-secondary-50 dark:bg-surface-dark text-secondary-900 dark:text-white': isActivePath(subMenu.path),
                    'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-surface-dark': !isActivePath(subMenu.path)
                  }"
                  @click="closeSidebarOnMobile"
                >
                  <component
                    :is="subMenu.icon"
                    class="h-4 w-4 mr-3"
                    :class="{
                      'text-secondary-700 dark:text-white': isActivePath(subMenu.path),
                      'text-gray-400': !isActivePath(subMenu.path)
                    }"
                  />
                  {{ subMenu.name }}
                </router-link>
              </div>
            </div>
          </transition>
        </div>

        <!-- Tambahkan menu Buku secara langsung -->
        <router-link 
          to="/dashboard/admin/buku"
          :class="[
            $route.path === '/dashboard/admin/buku'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <BookOpenIcon
            :class="[
              $route.path === '/dashboard/admin/buku'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Buku
        </router-link>

        <!-- Tambahkan menu perangkat kurikulum -->
        <router-link 
          to="/dashboard/admin/perangkat-kurikulum"
          :class="[
            $route.path === '/dashboard/admin/perangkat-kurikulum'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <DocumentTextIcon
            :class="[
              $route.path === '/dashboard/admin/perangkat-kurikulum'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Perangkat Kurikulum
        </router-link>

        <!-- Tambahkan menu Materi -->
        <router-link 
          to="/dashboard/admin/materi"
          :class="[
            $route.path === '/dashboard/admin/materi'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <FolderIcon
            :class="[
              $route.path === '/dashboard/admin/materi'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Materi
        </router-link>
      </template>

      <!-- Menu Guru -->
      <template v-if="userRole === 'guru'">
        <!-- Tambahkan menu Buku -->
        <router-link 
          v-if="userData?.crud_buku"
          to="/dashboard/guru/buku"
          :class="[
            $route.path === '/dashboard/guru/buku'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <BookOpenIcon
            :class="[
              $route.path === '/dashboard/guru/buku'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Buku
        </router-link>

        <!-- Tambahkan menu Materi -->
        <router-link 
          v-if="userData?.crud_materi"
          to="/dashboard/guru/materi"
          :class="[
            $route.path === '/dashboard/guru/materi'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <FolderIcon
            :class="[
              $route.path === '/dashboard/guru/materi'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Materi
        </router-link>

        <!-- Tambahkan menu Perangkat Kurikulum -->
        <router-link 
          to="/dashboard/guru/perangkat-kurikulum"
          :class="[
            $route.path === '/dashboard/guru/perangkat-kurikulum'
              ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
              : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
            'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
          ]"
          @click="closeSidebarOnMobile"
        >
          <DocumentTextIcon
            :class="[
              $route.path === '/dashboard/guru/perangkat-kurikulum'
                ? 'text-secondary-700 dark:text-white'
                : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
              'mr-3 h-6 w-6'
            ]"
            aria-hidden="true"
          />
          Perangkat Kurikulum
        </router-link>
      </template>


    </nav>

    

    <div class="p-6 mb-4">
      <!-- Logo sekolah -->
      <div class="flex flex-col items-center mb-10" v-if="userRole === 'siswa'">
        <img
          v-if="userData.sekolah_detail?.logo"
          :src="getFullLogoUrl"
          :alt="userData.sekolah_detail?.nama_sekolah"
          class="w-full h-12 object-contain"
          @error="e => e.target.src = '/school-logo-default.png'"
        />
        <div class="flex flex-col mt-3">
          <span class="text-text-light-secondary dark:text-text-dark-secondary">{{ userData.sekolah_detail?.nama_sekolah }}</span>
        </div>
      </div>
      <div class="flex flex-col items-center mb-10" v-if="userRole === 'guru'">
        <img
          v-if="userData.sekolah_detail?.logo"
          :src="getFullLogoUrl"
          :alt="userData.sekolah_detail?.nama_sekolah"
          class="w-full h-12 object-contain"
          @error="e => e.target.src = '/school-logo-default.png'"
        />
        <div class="flex flex-col mt-3">
          <span class="text-text-light-secondary dark:text-text-dark-secondary">{{ userData.sekolah_detail?.nama_sekolah }}</span>
        </div>
      </div>
      <router-link 
        to="/profile"
        :class="[
          $route.path === '/profile'
            ? 'bg-secondary-100 dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary'
            : 'text-text-light-secondary dark:text-text-dark-secondary hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-text-light-primary dark:hover:text-text-dark-primary',
          'group flex items-center border border-gray-200 justify-between px-2 py-2 text-sm font-medium rounded-md'
        ]"
        @click="closeSidebarOnMobile"
      >
      <div class="flex items-center">
        <img 
          :src="userData.foto_profil_url || '/user-profile.jpg'"
          :alt="userData.username"
          @error="e => e.target.src = '/user-profile.jpg'"
          class="w-8 h-8 rounded-full mr-3 object-cover"
        />
        <div class="flex flex-col">
          <span class="text-text-light-primary dark:text-text-dark-primary break-words max-w-[150px]">{{ userData.username }}</span>
          <span class="text-text-light-secondary dark:text-text-dark-secondary">{{ userData.role }}</span>
        </div>
      </div>
     

        
      </router-link>
      <div class="border-t border-gray-400 pb-2 mt-4"></div>
      <button
        @click="showLogoutModal = true"
        class="mt-2 w-full flex items-center justify-between px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 hover:text-gray-900 dark:hover:text-white bg-white dark:bg-surface-dark hover:bg-gray-100 dark:hover:bg-background-dark rounded-md shadow-sm group"
      >
        <div class="flex items-center">
          <ArrowRightOnRectangleIcon class="w-5 h-5 mr-2 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300" />
          <span>Logout</span>
        </div>
        <ChevronRightIcon class="w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-gray-600 dark:group-hover:text-gray-300" />
      </button>
    </div>
  </div>

  <!-- Overlay untuk mobile -->
  <div 
    v-if="isOpen" 
    class="fixed inset-0 bg-gray-600 bg-opacity-50 transition-opacity lg:hidden z-30" 
    @click="handleCloseSidebar"
  ></div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick, onUnmounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import BaseModal from './BaseModal.vue'
import {
  UserIcon,
  AcademicCapIcon,
  UserGroupIcon,
  BuildingOfficeIcon,
  HomeIcon as DashboardIcon,
  ArrowRightOnRectangleIcon,
  ChevronRightIcon,
  PhotoIcon,
  UsersIcon,
  BookOpenIcon,
  BuildingLibraryIcon,
  AcademicCapIcon as GraduationIcon,
  BuildingOffice2Icon,
  DocumentTextIcon,
  FolderIcon
} from '@heroicons/vue/24/outline'
import api from '@/config/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

// Inisialisasi formData dengan nilai default yang valid
const formData = ref({
  foto_profil: '/user-profile.jpg',
  nama_pengguna: 'Guest'
})



const emit = defineEmits(['close-sidebar'])

const store = useStore()
const userRole = computed(() => store.getters.userRole)

const adminMenus = ref([
  {
    name: 'Manajemen User',
    icon: UsersIcon,
    isDropdown: true,
    isOpen: false,
    subMenus: [
      {
        name: 'User',
        path: '/dashboard/admin/users',
        icon: UsersIcon
      },
      {
        name: 'Guru',
        path: '/dashboard/admin/guru',
        icon: UserIcon
      },
      {
        name: 'Siswa',
        path: '/dashboard/admin/siswa',
        icon: AcademicCapIcon
      }
    ]
  },
  {
    name: 'Atribut',
    icon: BuildingLibraryIcon,
    isDropdown: true,
    isOpen: false,
    subMenus: [
      {
        name: 'Sekolah',
        path: '/dashboard/admin/atribut/sekolah',
        icon: BuildingLibraryIcon
      },
      {
        name: 'Jenjang',
        path: '/dashboard/admin/atribut/jenjang',
        icon: GraduationIcon
      },
      {
        name: 'Kelas',
        path: '/dashboard/admin/atribut/kelas',
        icon: BuildingOffice2Icon
      },
      {
        name: 'Mata Pelajaran',
        path: '/dashboard/admin/atribut/mata_pelajaran',
        icon: BookOpenIcon
      }
    ]
  },
])

// Perbaiki fungsi untuk menutup sidebar
const handleCloseSidebar = () => {
  emit('close-sidebar')
  isUsersMenuOpen.value = false
  isAtributMenuOpen.value = false
  menuHeight.value = 0
  atributMenuHeight.value = 0
}

// Perbaiki fungsi closeSidebarOnMobile
const closeSidebarOnMobile = () => {
  if (window.innerWidth < 1024) {
    handleCloseSidebar()
  }
}

const router = useRouter()

// Tambahkan state untuk modal
const showLogoutModal = ref(false)

const handleLogout = async () => {
  try {
    // Navigasi ke login terlebih dahulu
    await router.push('/login')
    // Baru logout setelah navigasi selesai
    await store.dispatch('logout')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Tambahkan fungsi confirmLogout
const confirmLogout = async () => {
  await handleLogout()
  showLogoutModal.value = false
}

// Tambahkan state untuk user data
const userData = ref({
  username: '',
  foto_profil_url: '/user-profile.jpg',
  email: ''
})

// Tambahkan fungsi untuk mengambil data profil
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/user/profile/')
    userData.value = response.data
  } catch (error) {
    console.error('Error fetching user profile:', error)
  }
}

// Tambahkan event listener untuk ESC key
onMounted(() => {
  fetchUserProfile()
  
  const handleEscKey = (e) => {
    if (e.key === 'Escape' && props.isOpen) {
      handleCloseSidebar()
    }
  }

  const handleResize = () => {
    if (window.innerWidth < 1024) {
      handleCloseSidebar()
    }
  }
  
  window.addEventListener('keydown', handleEscKey)
  window.addEventListener('resize', handleResize)
  
  onUnmounted(() => {
    window.removeEventListener('keydown', handleEscKey)
    window.removeEventListener('resize', handleResize)
  })
})

const isUsersMenuOpen = ref(false)
const isAtributMenuOpen = ref(false)

const menuHeight = ref(0)
const atributMenuHeight = ref(0)

const toggleUsersMenu = async () => {
  isAtributMenuOpen.value = false // Tutup menu atribut
  if (!isUsersMenuOpen.value) {
    isUsersMenuOpen.value = true
    await nextTick()
    const dropdownContent = document.querySelector('.users-dropdown')
    if (dropdownContent) {
      menuHeight.value = dropdownContent.scrollHeight
    }
  } else {
    menuHeight.value = 0
    setTimeout(() => {
      isUsersMenuOpen.value = false
    }, 300)
  }
}

const toggleAtributMenu = async () => {
  isUsersMenuOpen.value = false // Tutup menu users
  if (!isAtributMenuOpen.value) {
    isAtributMenuOpen.value = true
    await nextTick()
    const dropdownContent = document.querySelector('.atribut-dropdown')
    if (dropdownContent) {
      atributMenuHeight.value = dropdownContent.scrollHeight
    }
  } else {
    atributMenuHeight.value = 0
    setTimeout(() => {
      isAtributMenuOpen.value = false
    }, 300)
  }
}

const isAnyUserMenuActive = computed(() => {
  return adminMenus.value.some(menu => {
    if (menu.isDropdown) {
      return menu.subMenus.some(subMenu => subMenu.path === router.currentRoute.value.path)
    }
    return menu.path === router.currentRoute.value.path
  })
})

// Tambahkan watch untuk props.isOpen
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    isUsersMenuOpen.value = false
    isAtributMenuOpen.value = false
    menuHeight.value = 0
    atributMenuHeight.value = 0
  }
})

// Tambahkan fungsi helper untuk mengecek active menu
const isMenuActive = (menu) => {
  if (!menu.isDropdown) return false
  return menu.subMenus.some(subMenu => subMenu.path === router.currentRoute.value.path)
}

// Update fungsi toggleDropdown
const toggleDropdown = (menu) => {
  // Tutup menu lain jika ada yang terbuka
  adminMenus.value.forEach(m => {
    if (m !== menu && m.isOpen) {
      m.isOpen = false
    }
  })
  // Toggle menu yang diklik
  menu.isOpen = !menu.isOpen
}

// Tambahkan watch untuk route changes
watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    // Buka dropdown secara otomatis jika submenu active
    adminMenus.value.forEach(menu => {
      if (menu.isDropdown) {
        const hasActiveSubmenu = menu.subMenus.some(subMenu => subMenu.path === newPath)
        if (hasActiveSubmenu) {
          menu.isOpen = true
        }
      }
    })
  },
  { immediate: true }
)

// Fungsi untuk toggle menu
const toggleMenu = (menu) => {
  // Tutup semua menu lain
  adminMenus.value.forEach(m => {
    if (m !== menu) {
      m.isOpen = false
    }
  })
  // Toggle menu yang diklik
  menu.isOpen = !menu.isOpen
}

// Fungsi untuk cek apakah path aktif
const isActivePath = (path) => {
  return router.currentRoute.value.path === path
}

// Fungsi untuk cek apakah menu aktif (termasuk submenu-nya)
const isActiveMenu = (menu) => {
  return menu.subMenus.some(subMenu => isActivePath(subMenu.path)) || menu.isOpen
}

// Watch route changes untuk mengatur menu aktif
watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    adminMenus.value.forEach(menu => {
      const hasActiveSubmenu = menu.subMenus.some(subMenu => subMenu.path === newPath)
      if (hasActiveSubmenu) {
        menu.isOpen = true
      }
    })
  },
  { immediate: true }
)

// Pastikan menu tertutup saat sidebar tertutup di mobile
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    adminMenus.value.forEach(menu => {
      menu.isOpen = false
    })
  }
})

const getFullLogoUrl = computed(() => {
  if (!userData.value?.sekolah_detail?.logo) return ''
  
  // Jika URL sudah lengkap (dimulai dengan http atau https), gunakan langsung
  if (userData.value.sekolah_detail.logo.startsWith('http')) {
    return userData.value.sekolah_detail.logo
  }
  
  // Jika URL relatif, tambahkan baseURL
  return import.meta.env.VITE_API_URL + userData.value.sekolah_detail.logo
})

</script>
<style scoped>
.space-y-1 {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity, max-height;
}

.rotate-90 {
  transform: rotate(90deg);
}

/* Tambahkan style untuk animasi yang lebih smooth */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Style untuk hover effect */
.group:hover .group-hover\:text-secondary-700 {
  transition-property: color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>

