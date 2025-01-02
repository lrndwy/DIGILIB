<template>
  <TransitionGroup
    tag="div"
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
    class="fixed z-50 inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6"
  >
    <div
      v-for="notification in notifications"
      :key="notification.id"
      class="w-full flex flex-col items-center space-y-4 sm:items-end"
    >
      <div
        class="max-w-sm w-full bg-white dark:bg-background-dark shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5"
        :class="{
          'ring-success-500/30 dark:ring-success-400/30': notification.type === 'success',
          'ring-error-500/30 dark:ring-error-400/30': notification.type === 'error',
          'ring-warning-500/30 dark:ring-warning-400/30': notification.type === 'warning',
          'ring-info-500/30 dark:ring-info-400/30': notification.type === 'info'
        }"
      >
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <CheckCircleIcon v-if="notification.type === 'success'" class="h-6 w-6 text-success-500 dark:text-success-400" />
              <XCircleIcon v-if="notification.type === 'error'" class="h-6 w-6 text-error-500 dark:text-error-400" />
              <ExclamationTriangleIcon v-if="notification.type === 'warning'" class="h-6 w-6 text-warning-500 dark:text-warning-400" />
              <InformationCircleIcon v-if="notification.type === 'info'" class="h-6 w-6 text-info-500 dark:text-info-400" />
            </div>
            <div class="ml-3 w-0 flex-1">
              <p class="text-sm font-medium text-text-light-primary dark:text-text-dark-primary">
                {{ notification.title }}
              </p>
              <p class="mt-1 text-sm text-text-light-secondary dark:text-text-dark-secondary">
                {{ notification.message }}
              </p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button
                @click="removeNotification(notification.id)"
                class="rounded-md inline-flex text-text-light-secondary dark:text-text-dark-secondary hover:text-text-light-primary dark:hover:text-text-dark-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <span class="sr-only">Tutup</span>
                <XMarkIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
        <!-- Progress bar -->
        <div 
          v-if="notification.duration !== Infinity"
          class="h-1 bg-primary-100 dark:bg-primary-900/30 rounded-b-lg overflow-hidden"
        >
          <div
            class="h-full transition-all duration-300 ease-linear rounded-b-lg"
            :class="{
              'bg-success-500 dark:bg-success-400': notification.type === 'success',
              'bg-error-500 dark:bg-error-400': notification.type === 'error',
              'bg-warning-500 dark:bg-warning-400': notification.type === 'warning',
              'bg-info-500 dark:bg-info-400': notification.type === 'info'
            }"
            :style="{ width: `${notification.progress}%` }"
          ></div>
        </div>
      </div>
    </div>
  </TransitionGroup>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { CheckCircleIcon, XCircleIcon, ExclamationTriangleIcon, InformationCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const notifications = ref([])
let notificationId = 0

const addNotification = ({ type = 'info', title, message, duration = 5000 }) => {
  const id = notificationId++
  const notification = {
    id,
    type,
    title,
    message,
    duration,
    progress: 100,
    timer: null
  }

  notifications.value.push(notification)

  if (duration !== Infinity) {
    const startTime = Date.now()
    const animate = () => {
      const elapsed = Date.now() - startTime
      const remaining = duration - elapsed
      
      if (remaining <= 0) {
        removeNotification(id)
        return
      }

      notification.progress = (remaining / duration) * 100
      notification.timer = requestAnimationFrame(animate)
    }

    notification.timer = requestAnimationFrame(animate)
  }

  return id
}

const removeNotification = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification && notification.timer) {
    cancelAnimationFrame(notification.timer)
  }
  notifications.value = notifications.value.filter(n => n.id !== id)
}

// Membersihkan semua timer saat komponen di-unmount
onUnmounted(() => {
  notifications.value.forEach(notification => {
    if (notification.timer) {
      cancelAnimationFrame(notification.timer)
    }
  })
})

// Expose methods untuk digunakan di luar komponen
defineExpose({
  addNotification,
  removeNotification
})
</script> 
