<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <div class="flex flex-wrap gap-6 text-left">
      <!-- User Selection Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          User <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.user" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Pilih User</option>
          <option v-for="user in filteredUsers" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
      </div>

      <!-- Nama Siswa Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Nama Siswa <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.nama_siswa" 
          type="text" 
          required
          placeholder="Masukkan nama siswa"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

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
          <option v-for="jenjang in jenjangList" :key="jenjang.id" :value="jenjang.id">
            {{ jenjang.nama_jenjang }}
          </option>
        </select>
      </div>

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
          <option v-for="kelas in filteredKelasList" :key="kelas.id" :value="kelas.id">
            {{ kelas.nama_kelas }}
          </option>
        </select>
      </div>

      <!-- Sekolah Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Sekolah <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.sekolah" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Pilih Sekolah</option>
          <option v-for="sekolah in sekolahList" :key="sekolah.id" :value="sekolah.id">
            {{ sekolah.nama_sekolah }}
          </option>
        </select>
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
        class="w-fit flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        {{ siswa ? 'Update' : 'Simpan' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'
import { useNotifications } from '@/composables/useNotifications'

const { notify } = useNotifications()

const props = defineProps({
  siswa: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])
const users = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const filteredUsers = computed(() => {
  if (props.siswa) {
    return [...users.value, {
      id: props.siswa.user,
      username: props.siswa.user_detail.username
    }]
  }
  return users.value.filter(user => user.role === 'siswa')
})

const filteredKelasList = computed(() => {
  if (!formData.value.jenjang) return []
  return kelasList.value.filter(k => k.jenjang === formData.value.jenjang)
})

const formData = ref({
  user: '',
  nama_siswa: '',
  kelas: '',
  jenjang: '',
  sekolah: ''
})

const handleJenjangChange = async () => {
  if (formData.value.jenjang) {
    try {
      const response = await api.get('/kelas/by_jenjang/', {
        params: {
          jenjang_id: formData.value.jenjang
        }
      })
      
      kelasList.value = response.data
      formData.value.kelas = '' // Reset pilihan kelas ketika jenjang berubah
      
    } catch (error) {
      notify({
        type: 'error',
        title: 'Gagal',
        message: 'Gagal mengambil data kelas'
      })
      console.error('Error fetching kelas:', error)
    }
  } else {
    kelasList.value = []
    formData.value.kelas = ''
  }
}

const fetchData = async () => {
  try {
    const [usersRes, jenjangRes, sekolahRes] = await Promise.all([
      api.get('/available-users/?role=siswa'),
      api.get('/jenjang/'),
      api.get('/sekolah/')
    ])
    
    users.value = usersRes.data
    jenjangList.value = jenjangRes.data
    sekolahList.value = sekolahRes.data

    if (props.siswa) {
      formData.value = {
        user: props.siswa.user,
        nama_siswa: props.siswa.nama_siswa,
        kelas: props.siswa.kelas,
        jenjang: props.siswa.jenjang,
        sekolah: props.siswa.sekolah
      }
      await handleJenjangChange()
    }
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data'
    })
    console.error('Error fetching data:', error)
  }
}

onMounted(fetchData)

watch(() => formData.value.jenjang, handleJenjangChange)

const handleSubmit = () => {
  if (!formData.value.user || !formData.value.nama_siswa || !formData.value.kelas || 
      !formData.value.jenjang || !formData.value.sekolah) {
    notify({
      type: 'warning',
      title: 'Peringatan',
      message: 'Semua field harus diisi'
    })
    return
  }
  emit('submit', formData.value)
}
</script>
