<template>
  <div class="min-h-screen bg-background-light dark:bg-surface-dark text-text-light-primary dark:text-text-dark-primary overflow-x-hidden overflow-y-hidden">
    <div v-if="isAuthenticated && !isBukuViewerRoute && !isPerangkatViewerRoute && !isMateriViewerRoute && !isLandingPageRoute">
      <div class="flex items-center justify-center">
        <Sidebar 
          :is-open="isSidebarOpen" 
          @close-sidebar="closeSidebar"
        />
        
        <div class="flex-1 transition-all duration-200 ease-in-out w-full
                    lg:ml-64 
                    md:p-5
                    flex items-start lg:items-center 
                    min-h-screen
                    overflow-x-auto">
          <main class="rounded-2xl lg:bg-white dark:lg:bg-background-dark lg:h-[calc(100vh-40px)] 
                       relative lg:shadow-lg lg:border-gray-200 dark:lg:border-border-dark 
                       lg:border-[0.5px] h-screen sm:bg-gray-100 
                       sm:shadow-none shadow-none bg-gray-100 dark:bg-surface-dark 
                       md:min-w-[800px] w-full overflow-hidden lg:pt-2 md:pt-0">
            <Navbar @toggle-sidebar="toggleSidebar"/>
            <div class="overflow-y-auto h-[calc(100%-64px)]">
              <RouterView v-slot="{ Component }">
                <TransitionWrapper>
                  <component :is="Component" :key="$route.fullPath" />
                </TransitionWrapper>
              </RouterView>
            </div>
          </main>
        </div>
      </div>
    </div>
    <div v-else-if="isBukuViewerRoute || isPerangkatViewerRoute || isMateriViewerRoute || isLandingPageRoute">
      <RouterView v-slot="{ Component }">
        <component v-if="isLandingPageRoute" :is="Component" :key="$route.fullPath" />
        <TransitionWrapper v-else>
          <component :is="Component" :key="$route.fullPath" />
        </TransitionWrapper>
      </RouterView>
    </div>
    <div v-else>
      <RouterView v-slot="{ Component }">
        <template v-if="$route.name === 'login'">
          <component :is="Component" :key="$route.fullPath" />
        </template>
        <TransitionWrapper v-else>
          <component :is="Component" :key="$route.fullPath" />
        </TransitionWrapper>
      </RouterView>
    </div>
    <Notifications ref="notificationsRef" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, provide } from 'vue'
import { useStore } from 'vuex'
import { RouterView, useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import Notifications from '@/components/Notifications.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'

const store = useStore()
const route = useRoute()
const isAuthenticated = computed(() => store.getters.isAuthenticated)
const isSidebarOpen = ref(false)
const notificationsRef = ref(null)

const isBukuViewerRoute = computed(() => {
  return route.name === 'BukuViewer'
})

const isPerangkatViewerRoute = computed(() => {
  return route.name === 'PerangkatViewer'
})

const isMateriViewerRoute = computed(() => {
  return route.name === 'MateriViewer'
})

const isLandingPageRoute = computed(() => {
  return route.name === 'LandingPage'
})

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

provide('notifications', {
  addNotification: (...args) => notificationsRef.value?.addNotification(...args)
})

onMounted(() => {
  store.dispatch('initializeTheme')
})
</script>


