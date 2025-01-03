<template>
  <TransitionWrapper>
    <div 
      class="viewer-container"
      @contextmenu.prevent
    >
      <!-- Toolbar -->
      <div class="toolbar bg-surface-dark/80 backdrop-blur-lg border-b border-border-dark text-text-dark-primary p-4 flex justify-between items-center shadow-lg">
        <div class="flex items-center gap-4">
          <button
            @click="$router.back()"
            class="p-2 hover:bg-background-dark/50 rounded-lg transition-colors duration-200 group"
          >
            <ArrowLeftIcon class="w-5 h-5 text-text-dark-secondary group-hover:text-text-dark-primary transition-colors" />
          </button>
          
          <div class="flex flex-col">
            <h1 class="text-lg font-medium">
              {{ decodeURIComponent(route.params.title) }}
            </h1>
          </div>
        </div>
      </div>

      <!-- PDF Viewer container -->
      <div class="viewer-content">
        <VPdfViewer 
          v-if="pdfUrl" 
          :src="pdfUrl"
          @error="handleError"
          :toolbar-options="{
              newFileOpenable: false,
              downloadable: false,
              printable: false,
              fullscreen: true,
          }" 
        />
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { VPdfViewer, useLicense } from '@vue-pdf-viewer/viewer'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import api from '@/config/api'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const pdfUrl = ref(null)
const error = ref(null)

// Tambahkan license seperti komponen lain
useLicense('8ac115b7-b578-4a6b-af83-84c687aa2daf')

// Fungsi untuk mengambil PDF
const fetchPdfUrl = async () => {
  try {
    const bookId = route.params.bookId
    const response = await api.get(`/buku/${bookId}/stream/`, {
      responseType: 'blob'
    })
    pdfUrl.value = URL.createObjectURL(response.data)
  } catch (err) {
    console.error('Error fetching PDF:', err)
    error.value = 'Gagal memuat PDF'
  }
}

const handleKeyPress = (e) => {
  if (e.keyCode === 44) return false
  if (e.ctrlKey && e.keyCode === 80) return false
  if (e.ctrlKey && e.keyCode === 83) return false
  if (e.ctrlKey && e.keyCode === 85) return false
}

const handleError = (err) => {
  console.error('Error loading PDF:', err)
  error.value = 'Gagal memuat PDF'
}

onMounted(() => {
  fetchPdfUrl()
  document.addEventListener('keydown', handleKeyPress)
  document.addEventListener('contextmenu', (e) => e.preventDefault())
})

onUnmounted(() => {
  if (pdfUrl.value) {
    URL.revokeObjectURL(pdfUrl.value)
  }
  document.removeEventListener('keydown', handleKeyPress)
  document.removeEventListener('contextmenu', (e) => e.preventDefault())
})
</script>

<style scoped>
.viewer-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #2d3748;
  z-index: 9999;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  display: flex;
  flex-direction: column;
}

.viewer-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* Mencegah highlight text */
::selection {
  background: transparent;
  color: inherit;
}

::-moz-selection {
  background: transparent;
  color: inherit;
}
</style>
