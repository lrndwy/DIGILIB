<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <div class="flex flex-wrap gap-6 text-left">
      <!-- Nama Buku Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Nama Buku <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.nama_buku"
          type="text"
          required
          placeholder="Masukkan nama buku"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        />
      </div>

      <!-- File Buku Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          File Buku <span class="text-red-500">*</span>
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
          <!-- Upload Icon & Text -->
          <div class="text-center">
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
              PDF, DOC, DOCX (max. 10MB)
            </p>
          </div>

          <!-- Hidden File Input -->
          <input
            ref="fileInput"
            type="file"
            @change="handleFileChange"
            accept=".pdf,.doc,.docx"
            class="hidden"
          />
        </div>

        <!-- File Name Display -->
        <div 
          v-if="isFile(formData.file_buku) || currentFile" 
          class="mt-2 flex items-center justify-between p-2 bg-gray-50 dark:bg-surface-dark rounded-lg"
        >
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-2 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
            </svg>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ isFile(formData.file_buku) ? formData.file_buku.name : currentFile.split('/').pop() }}
            </span>
          </div>
          <button 
            v-if="isFile(formData.file_buku)"
            @click.prevent="removeFile" 
            class="text-red-500 hover:text-red-700"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Field lainnya hanya ditampilkan jika bukan guru -->
      <template v-if="!isGuru">
        <!-- Jenjang Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Jenjang <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.jenjang"
            required
            @change="handleJenjangChange"
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
            <option value="">Pilih Jenjang</option>
            <option v-for="item in jenjangList" :key="item.id" :value="item.id">
              {{ item.nama_jenjang }}
            </option>
          </select>
        </div>
      </template>

      <!-- Kelas Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Kelas <span class="text-red-500">*</span>
        </label>
        <select
          v-model="formData.kelas"
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Pilih Kelas</option>
          <option v-for="item in availableKelas" :key="item.id" :value="item.id">
            {{ item.nama_kelas }}
          </option>
        </select>
      </div>

      <!-- Penerbit Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Penerbit <span class="text-red-500">*</span>
        </label>
        <input
          v-model="formData.penerbit"
          type="text"
          required
          placeholder="Masukkan nama penerbit"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        />
      </div>

      <!-- Mata Pelajaran Field -->
      <div v-if="!isGuru" class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Mata Pelajaran <span class="text-red-500">*</span>
        </label>
        <select
          v-model="formData.mata_pelajaran"
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Pilih Mata Pelajaran</option>
          <option v-for="item in mapelList" :key="item.id" :value="item.id">
            {{ item.nama_mata_pelajaran }}
          </option>
        </select>
      </div>

      <!-- Sekolah Field -->
      <div v-if="!isGuru" class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Sekolah
        </label>
        <select
          v-model="selectedSekolah"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Umum</option>
          <option v-for="item in sekolahList" :key="item.id" :value="item.id">
            {{ item.nama_sekolah }}
          </option>
        </select>
      </div>

      <!-- Status Field -->
      <div class="w-full flex items-center">
        <Checkbox
          v-model="formData.status"
          :true-value="'aktif'"
          :false-value="'tidak_aktif'"
        >
          Status Aktif
        </Checkbox>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-row justify-end space-x-2 pt-6 border-t border-border-light dark:border-border-dark">
      <FwbButton 
        type="button"
        color="dark"
        class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
        @click="$emit('cancel')"
      >
        Batal
      </FwbButton>
      <FwbButton 
        type="submit"
        color="dark"
        class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        {{ buku ? 'Simpan' : 'Tambah' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { FwbButton } from 'flowbite-vue'
import Checkbox from '@/components/Checkbox.vue'
import api from '@/config/api'

const props = defineProps({
  buku: {
    type: Object,
    default: null
  },
  guruData: {
    type: Object,
    default: null
  },
  isGuru: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel', 'error'])

const mapelList = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const formData = ref({
  nama_buku: '',
  file_buku: null,
  penerbit: '',
  kelas: '',
  jenjang: '',
  mata_pelajaran: '',
  sekolah: '',
  status: 'aktif'
})

// Inisialisasi form data
if (props.buku) {
  formData.value = {
    nama_buku: props.buku.nama_buku,
    penerbit: props.buku.penerbit,
    kelas: props.buku.kelas,
    jenjang: props.buku.jenjang,
    mata_pelajaran: props.buku.mata_pelajaran,
    sekolah: props.buku.sekolah || '',
    status: props.buku.status
  }
} else if (props.isGuru && props.guruData) {
  // Set nilai default untuk guru
  formData.value.jenjang = props.guruData.jenjang
  formData.value.sekolah = props.guruData.sekolah
  formData.value.mata_pelajaran = props.guruData.nama_mata_pelajaran
}

// Computed untuk mengontrol tampilan field berdasarkan role
const showJenjangField = computed(() => !props.isGuru)
const showSekolahField = computed(() => !props.isGuru)
const availableKelas = computed(() => {
  if (props.isGuru) {
    return props.guruData?.kelas_detail || []
  }
  return kelasList.value
})

const fileInput = ref(null)
const isDragging = ref(false)

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
    // Validasi tipe file
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!validTypes.includes(file.type)) {
      emit('error', {
        type: 'error',
        title: 'Error',
        message: 'Format file tidak valid. Gunakan PDF, DOC, atau DOCX'
      })
      return
    }
    
    // Validasi ukuran file (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      emit('error', {
        type: 'error',
        title: 'Error',
        message: 'Ukuran file terlalu besar. Maksimal 10MB'
      })
      return
    }
    
    formData.value.file_buku = file
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  handleFileChange(event)
}

const removeFile = () => {
  formData.value.file_buku = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleJenjangChange = async () => {
  if (formData.value.jenjang) {
    try {
      const response = await api.get('/kelas/by_jenjang/', {
        params: {
          jenjang_id: formData.value.jenjang
        }
      })
      kelasList.value = response.data
      
      // Jika bukan mode edit, reset pilihan kelas
      if (!props.buku) {
        formData.value.kelas = ''
      }
    } catch (error) {
      console.error('Error fetching kelas:', error)
    }
  } else {
    kelasList.value = []
    formData.value.kelas = ''
  }
}

const handleSubmit = () => {
  const requiredFields = ['nama_buku', 'penerbit', 'kelas']
  
  if (!props.isGuru) {
    requiredFields.push('jenjang', 'mata_pelajaran')
  }

  const missingFields = requiredFields.filter(field => !formData.value[field])
  
  if (missingFields.length > 0 || (!props.buku && !formData.value.file_buku)) {
    emit('error', {
      type: 'error',
      title: 'Validasi Error',
      message: 'Semua field wajib harus diisi'
    })
    return
  }

  // Buat FormData object untuk mengirim file
  const submitData = new FormData()
  
  // Append semua field ke FormData
  Object.keys(formData.value).forEach(key => {
    if (formData.value[key] !== null && formData.value[key] !== '') {
      submitData.append(key, formData.value[key])
    }
  })

  // Jika guru, tambahkan data dari guruData
  if (props.isGuru && props.guruData) {
    submitData.set('mata_pelajaran', props.guruData.nama_mata_pelajaran)
    submitData.set('jenjang', props.guruData.jenjang)
    submitData.set('sekolah', props.guruData.sekolah)
  }

  emit('submit', submitData)
}

const fetchData = async () => {
  try {
    if (props.isGuru) {
      // Jika guru, gunakan data mata pelajaran dari guruData
      if (props.guruData?.nama_mata_pelajaran_detail) {
        mapelList.value = [props.guruData.nama_mata_pelajaran_detail]
      }
    } else {
      // Jika bukan guru, fetch semua data seperti biasa
      const [mapelRes, jenjangRes, sekolahRes] = await Promise.all([
        api.get('/mata-pelajaran/'),
        api.get('/jenjang/'),
        api.get('/sekolah/')
      ])
      
      mapelList.value = mapelRes.data
      jenjangList.value = jenjangRes.data
      sekolahList.value = sekolahRes.data
    }

    // Jika dalam mode edit, panggil handleJenjangChange untuk memuat data kelas
    if (props.buku) {
      await handleJenjangChange()
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const currentFile = computed(() => {
  if (props.buku?.file_buku) {
    return props.buku.file_buku
  }
  return null
})

// Tambahkan watch untuk jenjang
watch(() => formData.value.jenjang, () => {
  handleJenjangChange()
})

const selectedSekolah = computed({
  get() {
    return formData.value.sekolah || ''  // Return string kosong jika null
  },
  set(value) {
    formData.value.sekolah = value
  }
})

onMounted(() => {
  fetchData()
})
</script> 
