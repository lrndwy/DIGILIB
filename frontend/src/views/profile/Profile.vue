<template>
  <div>
    <TransitionWrapper>
      <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6 p-8">
        <div class="flex flex-col items-center mb-8">
          <div class="relative">
            <img 
              :src="formData.foto_profil_url || '/user-profile.jpg'" 
              class="w-32 h-32 rounded-full object-cover border-4 border-white dark:border-gray-800 shadow-lg"
              alt="Foto profil"
              @error="e => e.target.src = '/user-profile.jpg'"
            />
          </div>
          <h2 class="mt-4 text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">
            {{ formData.username }}
          </h2>
          <p class="text-text-light-secondary dark:text-text-dark-secondary">
            {{ formData.role }}
          </p>
        </div>

        <h1 class="text-2xl sm:text-3xl font-bold mb-8 text-text-light-primary dark:text-text-dark-primary">
          Profil
        </h1>

        <div class="flex flex-wrap gap-6">
          <!-- Username Field (Readonly) -->
          <div class="w-full">
            <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
              Username
            </label>
            <input 
              v-model="formData.username" 
              type="text" 
              readonly
              disabled
              class="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-border-light dark:border-border-dark rounded-lg"
            >
          </div>

          <!-- Nama Field -->
          <div class="w-full" v-if="formData.role !== 'admin'">
            <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
              Nama
            </label>
            <input 
              v-model="formData.nama"
              type="text"
              readonly
              disabled
              class="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-border-light dark:border-border-dark rounded-lg"
            >
          </div>

          <!-- Email Field -->
          <div class="w-full">
            <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
              Email <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="formData.email" 
              type="email" 
              required
              class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
          </div>

          <!-- Password Change Toggle -->
          <div class="w-full">
            <div class="flex items-center gap-2 mb-4">
              <Toggle v-model="showPasswordChange">
                Ubah Password
              </Toggle>
            </div>

            <Transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-2"
            >
              <div v-if="showPasswordChange" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium mb-2">Password Baru</label>
                  <input 
                    v-model="formData.password"
                    type="password"
                    class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border rounded-lg"
                  >
                </div>
              </div>
            </Transition>
          </div>

          <!-- Foto Profil -->
          <div class="w-full">
            <div class="flex items-center gap-2 mb-4">
              <Toggle v-model="showProfilePhotoChange">
                Ubah Foto Profil
              </Toggle>
            </div>

            <Transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-95"
            >
              <div v-if="showProfilePhotoChange">
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
                  <div v-if="formData.foto_profil_url" class="mb-4">
                    <img 
                      :src="formData.foto_profil_url"
                      class="mx-auto w-32 h-32 rounded-full object-cover"
                      alt="Preview foto profil"
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
                      JPG, PNG (max. 2MB)
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
                  v-if="formData.foto_profil" 
                  class="mt-2 flex items-center justify-between p-2 bg-gray-50 dark:bg-surface-dark rounded-lg"
                >
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-2 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
                    </svg>
                    <span class="text-sm text-gray-500 dark:text-gray-400">
                      {{ formData.foto_profil.name }}
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
            </Transition>
          </div>

          <!-- Fields untuk Guru dan Siswa -->
          <template v-if="formData.role === 'guru' || formData.role === 'siswa'">
            <!-- Sekolah Field -->
            <div class="w-full">
              <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
                Sekolah
              </label>
              <input 
                :value="formData.sekolah_detail?.nama_sekolah"
                type="text"
                readonly
                disabled
                class="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-border-light dark:border-border-dark rounded-lg"
              >
            </div>

            <!-- Jenjang Field -->
            <div class="w-full">
              <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
                Jenjang
              </label>
              <input 
                :value="formData.jenjang_detail?.nama_jenjang"
                type="text"
                readonly
                disabled
                class="w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-border-light dark:border-border-dark rounded-lg"
              >
            </div>

            <!-- Kelas Field -->
            <div class="w-full">
              <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
                Kelas
              </label>
              <div class="border border-border-light dark:border-border-dark rounded-lg">
                <!-- List untuk Guru -->
                <template v-if="formData.role === 'guru'">
                  <div class="divide-y divide-border-light dark:divide-border-dark">
                    <div 
                      v-for="kelas in formData.kelas_detail" 
                      :key="kelas.id"
                      class="p-3 flex items-center justify-between bg-white dark:bg-surface-dark first:rounded-t-lg last:rounded-b-lg"
                    >
                      <div class="flex items-center space-x-3">
                        <div class="flex-shrink-0">
                          <BookOpenIcon class="w-5 h-5 text-primary-500" />
                        </div>
                        <div>
                          <p class="font-medium text-text-light-primary dark:text-text-dark-primary">
                            {{ kelas.nama_kelas }}
                          </p>
                        </div>
                      </div>
                      <div class="flex-shrink-0">
                        <CheckCircleIcon class="w-5 h-5 text-green-500" />
                      </div>
                    </div>
                  </div>
                </template>

                <!-- List untuk Siswa -->
                <template v-else>
                  <div class="p-3 flex items-center justify-between bg-white dark:bg-surface-dark rounded-lg">
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <BookOpenIcon class="w-5 h-5 text-primary-500" />
                      </div>
                      <div>
                        <p class="font-medium text-text-light-primary dark:text-text-dark-primary">
                          {{ formData.kelas_detail?.nama_kelas }}
                        </p>
                      </div>
                    </div>
                    <div class="flex-shrink-0">
                      <CheckCircleIcon class="w-5 h-5 text-green-500" />
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </template>

        </div>


        <div class="flex justify-end gap-2 pt-6">
          <FwbButton type="submit" :disabled="isSubmitting">
            <template v-if="isSubmitting">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Menyimpan...
            </template>
            <template v-else>
              Simpan
            </template>
          </FwbButton>
        </div>
      </form>
    </TransitionWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { useNotifications } from '@/composables/useNotifications'
import store from '@/store'
import Checkbox from '@/components/Checkbox.vue'
import Toggle from '@/components/Toggle.vue'
import { BookOpenIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'

const { notify } = useNotifications()
const mapelList = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const showPasswordChange = ref(false)
const showProfilePhotoChange = ref(false)

const formData = ref({
  username: '',
  email: '',
  password: '',
  role: '',
  nama: '',
  nama_mata_pelajaran: '',
  kelas: '',
  jenjang: '',
  sekolah: '',
  nama_guru: '',
  nama_siswa: '',
  foto_profil: null,
  foto_profil_url: null
})

const isDragging = ref(false)
const fileInput = ref(null)

const handleFileChange = (event) => {
  const file = event.target.files?.[0] || event.dataTransfer?.files?.[0]
  if (file) {
    // Validasi ukuran file (max 2MB)
    if (file.size > 2 * 1024 * 1024) {
      notify({
        type: 'error',
        title: 'Error',
        message: 'Ukuran file terlalu besar. Maksimal 2MB'
      })
      return
    }
    
    // Validasi tipe file
    if (!file.type.startsWith('image/')) {
      notify({
        type: 'error',
        title: 'Error',
        message: 'Format file tidak valid. Gunakan gambar (JPG, PNG)'
      })
      return
    }
    
    formData.value.foto_profil = file
    formData.value.foto_profil_url = URL.createObjectURL(file)
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  handleFileChange(event)
}

const removeFile = () => {
  formData.value.foto_profil = null
  formData.value.foto_profil_url = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Fetch semua data yang diperlukan
const fetchData = async () => {
  try {
    const [mapelRes, kelasRes, jenjangRes, sekolahRes] = await Promise.all([
      api.get('/mata-pelajaran/'),
      api.get('/kelas/'),
      api.get('/jenjang/'),
      api.get('/sekolah/')
    ])
    
    mapelList.value = mapelRes.data
    kelasList.value = kelasRes.data
    jenjangList.value = jenjangRes.data
    sekolahList.value = sekolahRes.data
  } catch (error) {
    console.error('Error fetching data:', error)
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat data'
    })
  }
}

onMounted(async () => {
  await fetchData()
  try {
    const response = await api.get('/user/profile/')
    const userData = response.data
    
    // Tambahkan pengecekan dan pengambilan data detail untuk siswa
    if (userData.role === 'siswa') {
      const siswaResponse = await api.get(`/siswa/by-user/${userData.id}/`)
      userData.kelas_detail = siswaResponse.data.kelas_detail
      userData.jenjang_detail = siswaResponse.data.jenjang_detail
      userData.sekolah_detail = siswaResponse.data.sekolah_detail
    }
    
    formData.value = {
      ...userData,
      password: '', // Reset password field
      foto_profil_url: userData.foto_profil_url,
      nama: userData.nama
    }
  } catch (error) {
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat profil'
    })
  }
})

const isSubmitting = ref(false)

const handleSubmit = async () => {
  if (isSubmitting.value) return
  
  isSubmitting.value = true
  try {
    const formDataToSend = new FormData()
    
    // Hanya kirim password jika toggle password aktif
    if (showPasswordChange.value && formData.value.password) {
      formDataToSend.append('password', formData.value.password)
    }
    
    // Hanya kirim foto jika toggle foto aktif
    if (showProfilePhotoChange.value && formData.value.foto_profil) {
      formDataToSend.append('foto_profil', formData.value.foto_profil)
    }
    
    // Append data lainnya
    Object.keys(formData.value).forEach(key => {
      if (
        key !== 'password' && 
        key !== 'foto_profil' && 
        key !== 'foto_profil_url' &&
        key !== 'username' && // Skip username karena readonly
        key !== 'kelas_detail' && // Skip detail objects
        key !== 'jenjang_detail' && 
        key !== 'sekolah_detail' &&
        formData.value[key] !== null && 
        formData.value[key] !== undefined
      ) {
        // Jika nilai adalah objek, ambil ID-nya
        if (typeof formData.value[key] === 'object' && formData.value[key]?.id) {
          formDataToSend.append(key, formData.value[key].id)
        } else {
          formDataToSend.append(key, formData.value[key])
        }
      }
    })

    const response = await api.put('/user/profile/', formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    store.commit('setUser', response.data)
    
    notify({
      type: 'success',
      title: 'Berhasil',
      message: 'Profil berhasil diperbarui'
    })
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat memperbarui profil'
    })
  } finally {
    isSubmitting.value = false
  }
}
</script> 
