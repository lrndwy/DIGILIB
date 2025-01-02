<template>
  <Notifications ref="notificationsRef" />
  <TransitionWrapper>
    <div class="p-8 w-full">
        <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
          Manajemen User
        </h1>
      
          <!-- Bagian atas table (Search, Filter, Tambah Users)-->
          <div class="flex flex-wrap items-center gap-2 mb-6">
            <div class="flex-1">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Cari username atau email..."
                class="w-full px-4 py-2 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
              />
            </div>
            
            <div class="relative" ref="filterDropdownRef">
              <fwb-tooltip>
                <template #trigger>
                  <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="toggleFilterDropdown">
                    <FunnelIcon class="w-6 h-6" />
                    <span v-if="activeFiltersCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {{ activeFiltersCount }}
                    </span>
                  </FwbButton>
                </template>
                <template #content>
                  Filter
                </template>
              </fwb-tooltip>
              
              <Transition
                enter-active-class="transition duration-200 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-200 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0"
              >
                <div v-if="showFilterDropdown" 
                     class="absolute right-0 mt-2 w-72 bg-white dark:bg-surface-dark rounded-lg shadow-lg border border-gray-200 dark:border-border-dark p-4 z-50">
                  <div class="flex justify-between items-center mb-4 pb-2 border-b border-border-light dark:border-border-dark">
                    <h3 class="font-medium">Filter</h3>
                    <button
                      v-if="activeFiltersCount > 0"
                      @click="resetFilters"
                      class="text-sm text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300"
                    >
                      Reset Filter
                    </button>
                  </div>
                  <div class="space-y-4">
                    <div>
                      <div class="font-medium mb-2">Role</div>
                      <div class="flex flex-col space-y-2">
                        <Checkbox 
                          v-for="role in roles" 
                          :key="role"
                          v-model="selectedFilters.roles"
                          :value="role"
                        >
                          {{ role.charAt(0).toUpperCase() + role.slice(1) }}
                        </Checkbox>
                      </div>
                    </div>
                    
                    <div>
                      <div class="font-medium mb-2">Status</div>
                      <div class="flex flex-col space-y-2">
                        <Checkbox
                          v-model="selectedFilters.status"
                          value="active"
                        >
                          Aktif
                        </Checkbox>
                        <Checkbox
                          v-model="selectedFilters.status"
                          value="inactive"
                        >
                          Nonaktif
                        </Checkbox>
                      </div>
                    </div>
                  </div>
                </div>
              </Transition>
            </div>

            <fwb-tooltip>
              <template #trigger>
                <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="showModal">
                  <PlusIcon class="w-6 h-6" />
                </FwbButton>
              </template>
              <template #content>
                Tambah User
              </template>
            </fwb-tooltip>
          </div>
          
          <!-- Bagian Table -->
          <div class="overflow-x-auto rounded-lg lg:border lg:border-gray-200 dark:border-border-dark">
            <div class="inline-block min-w-full align-middle">
              <!-- Tampilan desktop -->
              <table class="hidden md:table min-w-full divide-y divide-gray-200 dark:divide-border-dark">
                <thead class="bg-surface-light dark:bg-surface-dark">
                  <tr>
                    <th class="px-6 py-3 text-left">
                      <Checkbox
                        v-model="selectAll"
                        @change="toggleSelectAll"
                      />
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Username
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Email
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Role
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Status
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Aksi
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-background-dark divide-y divide-border-light dark:divide-border-dark">
                  <template v-if="loading">
                    <tr v-for="n in 5" :key="n" class="hover:bg-gray-50 dark:hover:bg-surface-dark">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="100px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="150px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="100px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="80px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                    </tr>
                  </template>
                  
                  <template v-else>
                    <tr v-for="user in paginatedUsers" :key="user.id" 
                        class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                        @click="showUserDetail(user)">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <Checkbox
                          v-model="selectedUserIds"
                          :value="user.id"
                          @click.stop
                        />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ user.username }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ user.email }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ user.role }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span 
                          :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                          class="px-2 py-1 text-xs rounded-full"
                        >
                          {{ user.is_active ? 'Aktif' : 'Nonaktif' }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="editUser(user)"
                            >
                              <PencilIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Edit User
                          </template>
                        </fwb-tooltip>
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="deleteUser(user.id)"
                            >
                              <TrashIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Hapus User
                          </template>
                        </fwb-tooltip>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
              <!-- Tampilan mobile -->
              <div class="block md:hidden">
                <template v-if="loading">
                  <div v-for="n in 5" :key="n" class="bg-white dark:bg-surface-dark p-4 mb-4 rounded-lg shadow">
                    <div class="space-y-3">
                      <SkeletonLoader width="100px" />
                      <SkeletonLoader width="150px" />
                      <SkeletonLoader width="100px" />
                      <SkeletonLoader width="80px" />
                    </div>
                  </div>
                </template>
                
                <template v-else>
                  <div v-for="user in paginatedUsers" :key="user.id" 
                      class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow cursor-pointer"
                      @click="showUserDetail(user)">
                    <div class="space-y-2">
                      <div class="flex justify-between items-center">
                        <div class="font-medium">
                          {{ user.username }}
                        </div>
                        <span 
                          :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                          class="px-2 py-1 text-xs rounded-full"
                        >
                          {{ user.is_active ? 'Aktif' : 'Nonaktif' }}
                        </span>
                      </div>
                      <div class="text-gray-600">
                        {{ user.email }}
                      </div>
                      <div class="text-sm text-gray-500">
                        Role: {{ user.role }}
                      </div>
                      <div class="flex space-x-2 pt-2">
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="editUser(user)"
                            >
                              <PencilIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Edit User
                          </template>
                        </fwb-tooltip>
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton 
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="deleteUser(user.id)"
                            >
                              <TrashIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Hapus User
                          </template>
                        </fwb-tooltip>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
              
            </div>        
          </div>

          <!-- Modal dengan ukuran responsif -->
          <BaseModal v-model="showAddModal">
            <template #header>
              <div class="flex items-center">
                {{ selectedUser ? 'Edit User' : 'Tambah User' }}
              </div>
            </template>
            <template #body>
              <UserForm 
                :user="selectedUser"
                @submit="saveUser"
                @cancel="closeModal"
              />
            </template>
          </BaseModal>

          <!-- Tambahkan modal konfirmasi di bawah modal yang sudah ada -->
          <BaseModal v-model="showDeleteModal">
            <template #header>
              <div class="flex items-center">
                Konfirmasi Hapus
              </div>
            </template>
            <template #body>
              <p v-if="userToDelete">
                Apakah Anda yakin ingin menghapus user ini?
              </p>
              <p v-else>
                Apakah Anda yakin ingin menghapus {{ selectedUserIds.length }} user yang dipilih?
              </p>
            </template>
            <template #footer>
              
                <FwbButton 
                  type="button"
                  color="dark"
                  class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                  @click="showDeleteModal = false"
                >
                  Batal
                </FwbButton>
                <FwbButton 
                  type="button"
                  color="dark"
                  class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                  @click="confirmDelete"
                >
                  Hapus
                </FwbButton>
              
            </template>
          </BaseModal>

          <!-- Tambahkan modal detail user setelah modal delete -->
          <BaseModal v-model="showDetailModal">
            <template #header>
              <div class="flex items-center">
                Detail User
              </div>
            </template>
            <template #body>
              <div v-if="selectedUserDetail" class="space-y-4">
                <!-- Foto Profil -->
                <div class="flex justify-center">
                  <img 
                    :src="selectedUserDetail.foto_profil_url || '/user-profile.jpg'" 
                    alt="Foto Profil"
                    class="w-32 h-32 rounded-full border border-border-light dark:border-border-dark object-cover"
                    @error="e => e.target.src = '/user-profile.jpg'"
                  >
                </div>

                <div class="flex flex-wrap justify-center gap-4">
                  <!-- Username -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Username:</div>
                    <div class="w-1/2">{{ selectedUserDetail.username }}</div>
                  </div>
                  
                  <!-- Email -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Email:</div>
                    <div class="w-1/2">{{ selectedUserDetail.email }}</div>
                  </div>
                  
                  <!-- Role -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Role:</div>
                    <div class="w-1/2">{{ selectedUserDetail.role }}</div>
                  </div>
                  
                  <!-- Status -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Status:</div>
                    <div class="w-1/2">
                      <span 
                        :class="selectedUserDetail.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                        class="px-2 py-1 text-xs rounded-full"
                      >
                        {{ selectedUserDetail.is_active ? 'Aktif' : 'Nonaktif' }}
                      </span>
                    </div>
                  </div>

                  <!-- Alamat -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Alamat:</div>
                    <div class="w-1/2">{{ selectedUserDetail.address || '-' }}</div>
                  </div>

                  <!-- Tanggal Lahir -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Tanggal Lahir:</div>
                    <div class="w-1/2">
                      {{ selectedUserDetail.tanggal_lahir ? new Date(selectedUserDetail.tanggal_lahir).toLocaleDateString('id-ID') : '-' }}
                    </div>
                  </div>

                  <!-- Nomor Telepon -->
                  <div class="w-full flex">
                    <div class="w-1/2 font-medium">Nomor Telepon:</div>
                    <div class="w-1/2">{{ selectedUserDetail.phone || '-' }}</div>
                  </div>
                </div>
              </div>
              
            </template>
            
          </BaseModal>

          <!-- Bagian bawah table (jumlah users, pagination) -->
          <div class="mt-4 flex justify-between gap-2">
            <div class="relative flex items-center gap-2 mt-4">
              <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
                Jumlah Users: {{ filteredUsers.length }}
              </div>
            </div>
            <div class="relative flex items-center gap-2">
              <button 
                  @click="currentPage--" 
                  :disabled="currentPage === 1"
                  class="px-3 py-1 rounded-md bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Sebelumnya
                </button>
                    
                <div class="flex items-center gap-2">
                  <template v-for="page in totalPages" :key="page">
                    <button 
                      @click="currentPage = page"
                      :class="[
                        'px-3 py-1 rounded-md',
                        currentPage === page 
                          ? 'bg-background-dark dark:bg-surface-light text-white dark:text-black' 
                          : 'bg-gray-100 dark:bg-surface-dark hover:bg-gray-200'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </template>
                </div>

                <button 
                  @click="currentPage++" 
                  :disabled="currentPage === totalPages"
                  class="px-3 py-1 rounded-md bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Selanjutnya
                </button>
            </div>
          </div>


          <div class="flex flex-wrap gap-2 mb-6">
            <fwb-tooltip v-if="selectedUserIds.length > 0">
              <template #trigger>
                <FwbButton
                  color="dark"
                  class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
                  @click="bulkDelete"
                >
                  <div class="flex flex-row gap-2 items-center justify-center p-1">
                    <TrashIcon class="w-5 h-5" />
                    <span>({{ selectedUserIds.length }})</span>
                  </div>
                </FwbButton>
              </template>
              <template #content>
                Hapus User Terpilih
              </template>
            </fwb-tooltip>
          </div>

    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/config/api'
import UserForm from '@/components/form/UserForm.vue'
import { FwbButton, FwbModal, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import Notifications from '@/components/Notifications.vue'

const users = ref([])
const loading = ref(true)
const showAddModal = ref(false)
const selectedUser = ref(null)
const showDeleteModal = ref(false)
const userToDelete = ref(null)
const showDetailModal = ref(false)
const selectedUserDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const roles = ['admin', 'guru', 'siswa']
const selectedFilters = ref({
  roles: [],
  status: []
})

const itemsPerPage = 3
const currentPage = ref(1)

const filteredUsers = computed(() => {
  let result = users.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(user => 
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    )
  }

  if (selectedFilters.value.roles.length > 0) {
    result = result.filter(user => 
      selectedFilters.value.roles.includes(user.role)
    )
  }

  if (selectedFilters.value.status.length > 0) {
    result = result.filter(user => {
      if (selectedFilters.value.status.includes('active')) {
        return user.is_active
      }
      if (selectedFilters.value.status.includes('inactive')) {
        return !user.is_active
      }
      return true
    })
  }

  return result
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredUsers.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredUsers.value.length / itemsPerPage)
})

const notificationsRef = ref(null)

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
    notificationsRef.value.addNotification({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat data users'
    })
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedUser.value = null
  showAddModal.value = true
}

const editUser = (user) => {
  selectedUser.value = { ...user }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedUser.value = null
}

const saveUser = async (userData) => {
  try {
    if (selectedUser.value) {
      // Edit user
      const response = await api.put(`/users/${selectedUser.value.id}/`, userData)
      if (response.data) {
        notificationsRef.value.addNotification({
          type: 'success',
          title: 'Berhasil',
          message: 'User berhasil diperbarui'
        })
      }
    } else {
      // Tambah user baru
      const response = await api.post('/users/', userData)
      if (response.data) {
        notificationsRef.value.addNotification({
          type: 'success',
          title: 'Berhasil',
          message: 'User berhasil ditambahkan'
        })
      }
    }
    
    closeModal()
    fetchUsers()
  } catch (error) {
    console.error('Error saving user:', error)
    const errorMessage = error.response?.data?.detail || 
                        Object.values(error.response?.data || {})[0]?.[0] ||
                        'Terjadi kesalahan saat menyimpan data user'
    notificationsRef.value.addNotification({
      type: 'error',
      title: 'Error',
      message: errorMessage
    })
  }
}

const deleteUser = (userId) => {
  userToDelete.value = userId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (userToDelete.value) {
      // Single delete
      await api.delete(`/users/${userToDelete.value}/`)
    } else {
      // Bulk delete
      await api.post('/users/bulk-delete/', {
        ids: selectedUserIds.value
      })
      selectedUserIds.value = []
    }
    
    notificationsRef.value.addNotification({
      type: 'success',
      title: 'Berhasil',
      message: 'User berhasil dihapus'
    })
    showDeleteModal.value = false
    userToDelete.value = null
    fetchUsers()
  } catch (error) {
    notificationsRef.value.addNotification({
      type: 'error',
      title: 'Error',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus user'
    })
  }
}

const showUserDetail = (user) => {
  selectedUserDetail.value = user
  showDetailModal.value = true
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const filterDropdownRef = ref(null)

onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

watch([searchQuery, selectedFilters], () => {
  currentPage.value = 1
})

const selectedUserIds = ref([])
const selectAll = ref(false)

const activeFiltersCount = computed(() => {
  let count = 0
  count += selectedFilters.value.roles.length
  count += selectedFilters.value.status.length
  return count
})

const resetFilters = () => {
  selectedFilters.value = {
    roles: [],
    status: []
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedUserIds.value = filteredUsers.value.map(user => user.id)
  } else {
    selectedUserIds.value = []
  }
}

const bulkDelete = async () => {
  try {
    if (selectedUserIds.value.length === 0) return
    
    showDeleteModal.value = true
    userToDelete.value = null // Set null untuk menandakan bulk delete
  } catch (error) {
    notificationsRef.value.addNotification({
      type: 'error',
      title: 'Error',
      message: 'Terjadi kesalahan saat menghapus user'
    })
  }
}

watch(selectedUserIds, (newValue) => {
  const allSelected = filteredUsers.value.every(user => 
    newValue.includes(user.id)
  )
  selectAll.value = allSelected
})

onMounted(() => {
  fetchUsers()
})
</script>
