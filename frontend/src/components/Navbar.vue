<template>
  <nav class="p-2 lg:rounded-t-2xl bg-white dark:bg-background-dark text-black dark:text-text-dark-primary">
    <div class="">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <button 
            @click="$emit('toggle-sidebar')" 
            class="text-black p-2 rounded-md hover:bg-gray-200 focus:outline-none lg:hidden dark:text-text-dark-primary dark:hover:bg-surface-dark"
          >
            <span class="sr-only">Open sidebar</span>
            <svg 
              class="h-6 w-6" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M4 6h16M4 12h16M4 18h16" 
              />
            </svg>
          </button>
          <div class="flex items-center">
            <div class="block">
              <div class="ml-4 flex items-baseline">
                <nav class="flex" aria-label="Breadcrumb">
                  <ol class="inline-flex items-center space-x-1 md:space-x-3">
                    <li class="inline-flex items-center">
                      <router-link 
                        :to="`/dashboard/${userRole}`"
                        class="inline-flex items-center text-sm font-medium text-gray-700 dark:text-text-dark-primary"
                      >
                        <HomeIcon class="w-4 h-4 mr-2"/>
                        Dashboard
                      </router-link>
                    </li>
                    <li v-if="currentPath.includes('admin') || currentPath.includes('profile')">
                      <div class="flex items-center">
                        <ChevronRightIcon class="w-4 h-4 text-gray-400"/>
                        <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2 dark:text-text-dark-primary">
                          {{ getBreadcrumbText }}
                        </span>
                      </div>
                    </li>
                  </ol>
                </nav>
              </div>
            </div>
          </div>
        </div>
        <button 
          @click="toggleTheme"
          class="p-2 mr-3 rounded-full hover:bg-gray-200 dark:hover:bg-surface-dark"
        >
          <SunIcon v-if="isDarkMode" class="h-6 w-6 text-yellow-300 transition-transform duration-300 transform rotate-0" />
          <MoonIcon v-else class="h-6 w-6 text-gray-700 transition-transform duration-300 transform rotate-0" />
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { HomeIcon, ChevronRightIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const store = useStore()
const router = useRouter()
const route = useRoute()
const user = computed(() => store.state.user)
const userRole = computed(() => store.getters.userRole)
const currentPath = computed(() => route.path)
const isDarkMode = computed(() => store.state.theme.darkMode)

const getBreadcrumbText = computed(() => {
  const path = route.path
  if (path.includes('users')) return 'Manajemen User'
  if (path.includes('guru')) return 'Manajemen Guru'
  if (path.includes('siswa')) return 'Manajemen Siswa'
  if (path.includes('profile')) return 'Profile'
  return ''
})

const handleLogout = async () => {
  await store.dispatch('logout')
  router.push('/login')
}

const toggleTheme = () => {
  store.commit('toggleDarkMode')
}

const emit = defineEmits(['toggle-sidebar'])

const toggleSidebar = () => {
  emit('toggle-sidebar')
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
</style>
