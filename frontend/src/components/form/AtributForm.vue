<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="flex flex-wrap gap-6">
      <!-- Form Sekolah -->
      <template v-if="type === 'sekolah'">
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Nama Sekolah <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama_sekolah"
            type="text"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
          />
        </div>
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Logo Sekolah
          </label>
          <!-- Area Drop Zone -->
          <div 
            @dragover.prevent
            @drop.prevent="handleDrop"
            class="relative border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
            :class="isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600'"
            @dragenter="isDragging = true"
            @dragleave="isDragging = false"
            @click="$refs.fileInput.click()"
          >
            <!-- Preview Area -->
            <div v-if="previewUrl || currentLogo" class="mb-4">
              <img 
                :src="previewUrl || currentLogo" 
                alt="Logo Preview"
                class="mx-auto w-32 h-32 object-contain rounded-lg"
              />
            </div>
            
            <!-- Upload Icon & Text -->
            <div v-else class="text-center">
              <svg 
                class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" 
                stroke="currentColor" 
                fill="none" 
                viewBox="0 0 48 48"
              >
                <path 
                  d="M24 8l-8 8h6v16h4V16h6l-8-8z M4 44h40V24H32v4h8v12H8V28h8v-4H4v20z" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
              <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Klik untuk upload atau drag and drop
              </p>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-500">
                PNG, JPG, GIF (max. 2MB)
              </p>
            </div>

            <!-- Hidden File Input -->
            <input
              ref="fileInput"
              type="file"
              @change="handleFileChange"
              accept="image/*"
              class="hidden"
            />
          </div>

          <!-- File Name Display -->
          <div 
            v-if="isFile(formData.logo_sekolah)" 
            class="mt-2 flex items-center justify-between p-2 bg-gray-50 dark:bg-surface-dark rounded-lg"
          >
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
              </svg>
              <span class="text-sm text-gray-500 dark:text-gray-400">
                {{ formData.logo_sekolah.name }}
              </span>
            </div>
            <button 
              @click.prevent="removeFile" 
              class="text-red-500 hover:text-red-700"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </template>

      <!-- Form Jenjang -->
      <template v-if="type === 'jenjang'">
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Nama Jenjang <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama_jenjang"
            type="text"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
          />
        </div>
      </template>

      <!-- Form Kelas -->
      <template v-if="type === 'kelas'">
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Jenjang <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.jenjang"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
          >
            <option value="">Pilih Jenjang</option>
            <option v-for="jenjang in jenjangList" :key="jenjang.id" :value="jenjang.id">
              {{ jenjang.nama_jenjang }}
            </option>
          </select>
        </div>
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Nama Kelas <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama_kelas"
            type="text"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
          />
        </div>
      </template>

      <!-- Form Mata Pelajaran -->
      <template v-if="type === 'mata_pelajaran'">
        <div class="w-full">
          <label class="block text-sm font-medium mb-2">
            Nama Mata Pelajaran <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama_mata_pelajaran"
            type="text"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
          />
        </div>
      </template>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-end space-x-2 pt-6 border-t border-border-light dark:border-border-dark">
      <FwbButton 
        type="button"
        color="dark"
        class="px-4 py-2"
        @click="$emit('cancel')"
      >
        Batal
      </FwbButton>
      <FwbButton 
        type="submit"
        color="dark"
        class="px-4 py-2"
      >
        {{ initialData ? 'Update' : 'Simpan' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  initialData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])
const fileInput = ref(null)
const isDragging = ref(false)
const previewUrl = ref(null)
const formData = ref({})
const jenjangList = ref([])

const currentLogo = computed(() => {
  if (props.type === 'sekolah' && props.initialData?.logo_sekolah) {
    return props.initialData.logo_sekolah
  }
  return null
})

const fetchJenjang = async () => {
  try {
    const response = await api.get('/jenjang/')
    jenjangList.value = response.data
  } catch (error) {
    console.error('Error fetching jenjang:', error)
  }
}

onMounted(() => {
  if (props.initialData) {
    const { logo_sekolah, ...rest } = props.initialData
    formData.value = { ...rest }
  }
  
  if (props.type === 'kelas') {
    fetchJenjang()
  }
})

const isFile = (value) => {
  return value && 
    typeof value === 'object' && 
    'name' in value && 
    'size' in value && 
    'type' in value && 
    value instanceof File
}

const handleFileChange = (event) => {
  const file = event.target.files?.[0] || event.dataTransfer?.files?.[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) { // 2MB limit
      alert('File terlalu besar. Maksimal ukuran file adalah 2MB')
      return
    }
    formData.value.logo_sekolah = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  handleFileChange(event)
}

const removeFile = () => {
  formData.value.logo_sekolah = null
  previewUrl.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleSubmit = () => {
  const data = new FormData()
  
  switch (props.type) {
    case 'sekolah':
      data.append('nama_sekolah', formData.value.nama_sekolah)
      if (isFile(formData.value.logo_sekolah)) {
        data.append('logo_sekolah', formData.value.logo_sekolah)
      }
      break
    case 'jenjang':
      data.append('nama_jenjang', formData.value.nama_jenjang)
      break
    case 'kelas':
      data.append('nama_kelas', formData.value.nama_kelas)
      data.append('jenjang', formData.value.jenjang)
      break
    case 'mata_pelajaran':
      data.append('nama_mata_pelajaran', formData.value.nama_mata_pelajaran)
      break
  }

  emit('submit', data)
}
</script> 
