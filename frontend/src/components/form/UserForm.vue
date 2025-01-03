<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <!-- Header Section -->
    <!-- <div class="border-b border-border-light dark:border-border-dark pb-4 mb-6">
      <h2 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">
        {{ user ? 'Edit User' : 'Tambah User Baru' }}
      </h2>
    </div> -->

    <div class="flex flex-wrap gap-6 text-left">
      <!-- Username Field - full width -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Username <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.username" 
          type="text" 
          required
          placeholder="Masukkan username"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>
      
      <!-- Email Field - full width -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Email <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.email" 
          type="email" 
          required
          placeholder="contoh@email.com"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>
      
      <!-- Password Section - full width -->
      <div class="w-full" v-if="!user">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Password <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.password" 
          type="password" 
          required
          placeholder="Masukkan password"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>
      
      <!-- Change Password Section - full width -->
      <div class="w-full" v-if="user">
        <div class="mb-4">
          <Checkbox v-model="changePassword">
            Ganti Password
          </Checkbox>
        </div>
        
        <div v-if="changePassword">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Password Baru <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.password" 
            type="password" 
            required
            placeholder="Masukkan password baru"
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>
      </div>
      
      <!-- Role Selection - setengah width pada layar lebih besar -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Role <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.role"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="admin">Admin</option>
          <option value="guru">Guru</option>
          <option value="siswa">Siswa</option>
        </select>
      </div>
      
      <!-- Active Status - setengah width pada layar lebih besar -->
      <div class="w-full flex items-center">
        <Checkbox 
          v-model="formData.is_active"
          :true-value="'true'"
          :false-value="'false'"
        >
          Status Aktif
        </Checkbox>
      </div>
    </div>

    <div class="w-full">
      <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
        Alamat <span class="text-red-500">*</span>
      </label>
      <textarea 
        v-model="formData.address"
        required
        placeholder="Masukkan alamat"
        class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
      ></textarea>
    </div>

    <div class="w-full">
      <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
        Tanggal Lahir <span class="text-red-500">*</span>
      </label>
      <input 
        v-model="formData.tanggal_lahir"
        type="date"
        required
        class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
      >
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
          {{ user ? 'Update' : 'Simpan' }}
        </template>
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FwbButton } from 'flowbite-vue'
import Checkbox from '@/components/Checkbox.vue'

const props = defineProps({
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel', 'error'])
const changePassword = ref(false)
const isLoading = ref(false)

const formData = ref({
  username: '',
  email: '',
  password: '',
  role: 'siswa',
  is_active: 'true',
  address: '',
  tanggal_lahir: '',
})

onMounted(() => {
  if (props.user) {
    const userData = { ...props.user }
    delete userData.password
    
    userData.is_active = userData.is_active ? 'true' : 'false'
    
    formData.value = userData
  }
})

const handleSubmit = async () => {
  // Validasi form
  if (!formData.value.username || !formData.value.email) {
    emit('error', {
      type: 'error',
      title: 'Validasi Error',
      message: 'Username dan email harus diisi'
    })
    return
  }

  if (!props.user && !formData.value.password) {
    emit('error', {
      type: 'error',
      title: 'Validasi Error',
      message: 'Password harus diisi untuk user baru'
    })
    return
  }

  isLoading.value = true

  try {
    const submitData = {
      username: formData.value.username,
      email: formData.value.email,
      role: formData.value.role,
      is_active: formData.value.is_active === 'true',
      address: formData.value.address || '',
      tanggal_lahir: formData.value.tanggal_lahir || null
    }
    
    if (!props.user || (props.user && changePassword.value)) {
      submitData.password = formData.value.password
    }
    
    if (submitData.tanggal_lahir) {
      submitData.tanggal_lahir = new Date(submitData.tanggal_lahir)
        .toISOString()
        .split('T')[0]
    }
    
    emit('submit', submitData)
  } finally {
    isLoading.value = false
  }
}
</script>
