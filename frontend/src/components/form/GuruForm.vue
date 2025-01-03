<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <div class="flex flex-wrap gap-6 text-left">
      <!-- User Selection -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          User <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.user" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          :class="{ 'border-red-500': errors.user }"
        >
          <option value="">Pilih User</option>
          <option v-for="user in filteredUsers" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
        <p v-if="errors.user" class="mt-1 text-sm text-red-500">{{ errors.user }}</p>
      </div>

      <!-- Nama Guru -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          Nama Guru <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.nama_guru" 
          type="text" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          :class="{ 'border-red-500': errors.nama_guru }"
        >
        <p v-if="errors.nama_guru" class="mt-1 text-sm text-red-500">{{ errors.nama_guru }}</p>
      </div>

      <!-- Mata Pelajaran -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          Mata Pelajaran <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.nama_mata_pelajaran" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          :class="{ 'border-red-500': errors.nama_mata_pelajaran }"
        >
          <option value="">Pilih Mata Pelajaran</option>
          <option v-for="mapel in mapelList" :key="mapel.id" :value="mapel.id">
            {{ mapel.nama_mata_pelajaran }}
          </option>
        </select>
        <p v-if="errors.nama_mata_pelajaran" class="mt-1 text-sm text-red-500">{{ errors.nama_mata_pelajaran }}</p>
      </div>

      <!-- Jenjang -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          Jenjang <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.jenjang" 
          required
          @change="handleJenjangChange"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          :class="{ 'border-red-500': errors.jenjang }"
        >
          <option value="">Pilih Jenjang</option>
          <option v-for="jenjang in jenjangList" :key="jenjang.id" :value="jenjang.id">
            {{ jenjang.nama_jenjang }}
          </option>
        </select>
        <p v-if="errors.jenjang" class="mt-1 text-sm text-red-500">{{ errors.jenjang }}</p>
      </div>

      <!-- Multiple Select Kelas -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          Kelas <span class="text-red-500">*</span>
        </label>
        
        <!-- Checkbox List -->
        <div class="border border-border-light dark:border-border-dark rounded-lg p-4">
          <div v-if="!filteredKelasOptions.length" class="text-gray-500 dark:text-gray-400">
            Pilih jenjang terlebih dahulu untuk melihat daftar kelas
          </div>
          
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <Checkbox
              v-for="kelas in filteredKelasOptions"
              :key="kelas.id"
              v-model="formData.kelas"
              :value="kelas.id"
            >
              {{ kelas.nama_kelas }}
            </Checkbox>
          </div>
        </div>

        <p v-if="errors.kelas" class="mt-1 text-sm text-red-500">{{ errors.kelas }}</p>
      </div>

      <!-- Sekolah -->
      <div class="w-full relative">
        <label class="block text-sm font-medium mb-2">
          Sekolah <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.sekolah" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          :class="{ 'border-red-500': errors.sekolah }"
        >
          <option value="">Pilih Sekolah</option>
          <option v-for="sekolah in sekolahList" :key="sekolah.id" :value="sekolah.id">
            {{ sekolah.nama_sekolah }}
          </option>
        </select>
        <p v-if="errors.sekolah" class="mt-1 text-sm text-red-500">{{ errors.sekolah }}</p>
      </div>
    </div>

    <!-- CRUD Buku -->
    <div class="w-full flex gap-6">
      <div class="flex-1">
        <label class="flex items-center space-x-2">
          <Checkbox
            v-model="formData.crud_buku"
            :true-value="true"
            :false-value="false"
          >
            Izinkan CRUD Buku
          </Checkbox>
        </label>
      </div>

      <!-- CRUD Materi -->
      <div class="flex-1">
        <label class="flex items-center space-x-2">
          <Checkbox
            v-model="formData.crud_materi"
            :true-value="true"
            :false-value="false"
          >
            Izinkan CRUD Materi
          </Checkbox>
        </label>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-row justify-end space-x-2 pt-6 border-t border-border-light dark:border-border-dark">
      <FwbButton 
        type="button"
        color="dark"
        class="w-fit flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
        @click="$emit('cancel')"
      >
        Batal
      </FwbButton>
      <FwbButton 
        type="submit"
        color="dark"
        :disabled="isLoading"
        class="w-fit flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        <template v-if="isLoading">
          <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          Memproses...
        </template>
        <template v-else>
          {{ guru ? 'Update' : 'Simpan' }}
        </template>
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import api from '@/config/api'
import { FwbButton } from 'flowbite-vue'
import Checkbox from '@/components/Checkbox.vue'

const props = defineProps({
  guru: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])
const users = ref([])
const mapelList = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const filteredUsers = computed(() => {
  if (props.guru) {
    // Jika mode edit, tambahkan user yang sedang diedit ke daftar
    return [...users.value, {
      id: props.guru.user,
      username: props.guru.user_detail.username
    }]
  }
  return users.value
})

const formData = ref({
  user: '',
  nama_guru: '',
  nama_mata_pelajaran: '',
  kelas: [],
  jenjang: '',
  sekolah: '',
  crud_buku: false,
  crud_materi: false
})

const filteredKelasOptions = computed(() => {
  if (!formData.value.jenjang) return []
  return kelasList.value.filter(k => k.jenjang === formData.value.jenjang)
})

// Pindahkan inisialisasi errors ke atas sebelum digunakan
const errors = ref({
  user: '',
  nama_guru: '',
  nama_mata_pelajaran: '',
  kelas: '',
  jenjang: '',
  sekolah: ''
})

const handleJenjangChange = async () => {
  if (formData.value.jenjang) {
    try {
      const response = await api.get('/guru/kelas-by-jenjang/', {
        params: {
          jenjang_id: formData.value.jenjang
        }
      })
      
      if (props.guru) {
        // Filter kelas yang sesuai dengan jenjang yang dipilih
        const existingKelas = props.guru.kelas_detail.filter(k => k.jenjang === formData.value.jenjang)
        
        // Gabungkan kelas yang sudah ada dengan kelas baru
        const newKelas = response.data.filter(k => !existingKelas.some(ek => ek.id === k.id))
        kelasList.value = [...existingKelas, ...newKelas]
        
        // Hanya reset kelas jika jenjang berbeda dengan data guru yang sedang diedit
        if (formData.value.jenjang !== props.guru.jenjang) {
          formData.value.kelas = []
        }
      } else {
        kelasList.value = response.data
        formData.value.kelas = [] // Reset hanya jika bukan mode edit
      }
    } catch (error) {
      console.error('Error fetching kelas:', error)
    }
  } else {
    kelasList.value = []
    formData.value.kelas = []
  }
}

const fetchData = async () => {
  try {
    const [usersRes, mapelRes, jenjangRes, sekolahRes] = await Promise.all([
      api.get('/available-users/?role=guru'),
      api.get('/mata-pelajaran/'),
      api.get('/jenjang/'),
      api.get('/sekolah/')
    ])
    
    users.value = usersRes.data
    mapelList.value = mapelRes.data
    jenjangList.value = jenjangRes.data
    sekolahList.value = sekolahRes.data

    if (props.guru) {
      // Set formData dengan data guru yang sedang diedit
      formData.value = {
        user: props.guru.user,
        nama_guru: props.guru.nama_guru,
        nama_mata_pelajaran: props.guru.nama_mata_pelajaran,
        kelas: props.guru.kelas_detail.map(k => k.id),
        jenjang: props.guru.jenjang,
        sekolah: props.guru.sekolah,
        crud_buku: props.guru.crud_buku,
        crud_materi: props.guru.crud_materi
      }
      
      // Set kelasList dengan data kelas yang sedang digunakan
      kelasList.value = [...props.guru.kelas_detail]
      
      // Ambil data kelas tambahan sesuai jenjang
      await handleJenjangChange()
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const dropdownRef = ref(null)

const handleClickOutside = (event) => {
  const target = event.target
  if (dropdownRef.value && !dropdownRef.value.contains(target) && !target.closest('[data-dropdown-trigger]')) {
    isOpen.value = false
  }
}

onMounted(() => {
  fetchData()
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

watch(() => formData.value.jenjang, handleJenjangChange)

const resetErrors = () => {
  errors.value = {
    user: '',
    nama_guru: '',
    nama_mata_pelajaran: '',
    kelas: '',
    jenjang: '',
    sekolah: ''
  }
}

const isLoading = ref(false)

const handleSubmit = async () => {
  resetErrors()
  let hasError = false

  if (!formData.value.user) {
    errors.value.user = 'User harus dipilih'
    hasError = true
  }
  
  if (!formData.value.nama_guru) {
    errors.value.nama_guru = 'Nama guru harus diisi'
    hasError = true
  }
  
  if (!formData.value.nama_mata_pelajaran) {
    errors.value.nama_mata_pelajaran = 'Mata pelajaran harus dipilih'
    hasError = true
  }
  
  if (formData.value.kelas.length === 0) {
    errors.value.kelas = 'Minimal pilih satu kelas'
    hasError = true
  }
  
  if (!formData.value.jenjang) {
    errors.value.jenjang = 'Jenjang harus dipilih'
    hasError = true
  }
  
  if (!formData.value.sekolah) {
    errors.value.sekolah = 'Sekolah harus dipilih'
    hasError = true
  }

  if (hasError) {
    return
  }

  isLoading.value = true
  try {
    emit('submit', formData.value)
  } finally {
    isLoading.value = false
  }
}

// Tambahkan watch untuk setiap field
watch(() => formData.value.user, (newValue) => {
  if (newValue) {
    errors.value.user = ''
  }
})

watch(() => formData.value.nama_guru, (newValue) => {
  if (newValue) {
    errors.value.nama_guru = ''
  }
})

watch(() => formData.value.nama_mata_pelajaran, (newValue) => {
  if (newValue) {
    errors.value.nama_mata_pelajaran = ''
  }
})

watch(() => formData.value.kelas, (newValue) => {
  if (newValue.length > 0) {
    errors.value.kelas = ''
  }
})

watch(() => formData.value.jenjang, (newValue) => {
  if (newValue) {
    errors.value.jenjang = ''
  }
})

watch(() => formData.value.sekolah, (newValue) => {
  if (newValue) {
    errors.value.sekolah = ''
  }
})
</script>

<style>
.multiselect-modern {
  --ms-tag-bg: #e5e7eb;
  --ms-tag-color: #374151;
  --ms-ring-color: #6b7280;
  --ms-option-bg-selected: #9ca3af;
}

.multiselect-tag {
  background: var(--ms-tag-bg);
  color: var(--ms-tag-color);
  padding: 4px 8px;
  border-radius: 4px;
  margin: 2px;
  display: inline-flex;
  align-items: center;
}

.multiselect-tag-remove {
  margin-left: 4px;
  cursor: pointer;
  font-style: normal;
  font-weight: bold;
}
</style>
