<template>
  <div 
    class="w-full h-full bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 relative flex items-center justify-center"
  >
    <!-- Cover Image -->
    <img
      v-if="coverUrl"
      :src="coverUrl"
      class="w-full h-full object-cover"
      @error="handleImageError"
    />

    <!-- Fallback -->
    <div v-else class="fallback-view">
      <component 
        :is="getFileIcon" 
        class="w-8 h-8 text-gray-400 mb-1"
      />
      <span class="text-xs text-gray-500 uppercase">
        {{ getFileExtension }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { DocumentIcon, DocumentTextIcon, DocumentArrowDownIcon } from '@heroicons/vue/24/outline'
import api from '@/config/api'

const props = defineProps({
  fileUrl: {
    type: String,
    required: true
  }
})

const coverUrl = ref(null)

// Get file path from URL
const getFilePath = computed(() => {
  try {
    const url = new URL(props.fileUrl)
    return url.pathname.split('/media/')[1].replace(/\/+/g, '/')
  } catch {
    return props.fileUrl.split('/media/')[1]?.replace(/\/+/g, '/') || null
  }
})

// Get cover URL
const getCoverUrl = async () => {
  if (!getFilePath.value || !props.fileUrl.toLowerCase().endsWith('.pdf')) {
    coverUrl.value = null
    return
  }

  try {
    const path = getFilePath.value.replace(/^\/+/, '')
    coverUrl.value = `${api.defaults.baseURL}/pdf-cover/${path}`
  } catch (error) {
    console.error('Error getting cover:', error)
    coverUrl.value = null
  }
}

const handleImageError = () => {
  coverUrl.value = null
}

// Get file extension
const getFileExtension = computed(() => {
  return props.fileUrl.split('.').pop()?.toLowerCase() || ''
})

// Get appropriate icon
const getFileIcon = computed(() => {
  switch(getFileExtension.value) {
    case 'pdf':
      return DocumentArrowDownIcon
    case 'doc':
    case 'docx':
      return DocumentTextIcon
    default:
      return DocumentIcon
  }
})

// Watch for fileUrl changes
watch(() => props.fileUrl, () => {
  getCoverUrl()
}, { immediate: true })
</script>


