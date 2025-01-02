<template>

  <TransitionWrapper>
    <div class="p-8 w-full">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Siswa
      </h1>

        <!-- Bagian atas table (Search, Filter, Tambah Siswa)-->
        <div class="flex flex-wrap items-center gap-2 mb-6">
          <!-- Search -->
          <div class="flex-1">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari nama siswa..."
              class="w-full px-4 py-2 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
            />
          </div>
          
          <!-- Filter -->
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
              <div v-show="showFilterDropdown" class="absolute right-0 mt-2 w-72 bg-white dark:bg-surface-dark rounded-lg shadow-lg border border-border-light dark:border-border-dark z-30">
                <div class="p-4 max-h-[400px] overflow-y-auto">
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

                  <!-- Filter Kelas -->
                  <div class="mb-4">
                    <h3 class="font-medium mb-2">Kelas</h3>
                    <div class="flex flex-col space-y-2">
                      <Checkbox
                        v-for="kelas in kelasList"
                        :key="kelas.id"
                        v-model="selectedFilters.kelas"
                        :value="kelas.id"
                      >
                        {{ kelas.nama_kelas }}
                      </Checkbox>
                    </div>
                  </div>

                  <!-- Filter Jenjang -->
                  <div class="mb-4">
                    <h3 class="font-medium mb-2">Jenjang</h3>
                    <div class="flex flex-col space-y-2">
                      <Checkbox
                        v-for="jenjang in jenjangList"
                        :key="jenjang.id"
                        v-model="selectedFilters.jenjang"
                        :value="jenjang.id"
                      >
                        {{ jenjang.nama_jenjang }}
                      </Checkbox>
                    </div>
                  </div>

                  <!-- Filter Sekolah -->
                  <div class="mb-4">
                    <h3 class="font-medium mb-2">Sekolah</h3>
                    <div class="flex flex-col space-y-2">
                      <Checkbox
                        v-for="sekolah in sekolahList"
                        :key="sekolah.id"
                        v-model="selectedFilters.sekolah"
                        :value="sekolah.id"
                      >
                        {{ sekolah.nama_sekolah }}
                      </Checkbox>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>

          <!-- Tambah Siswa -->
          <fwb-tooltip>
            <template #trigger>
              <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="showModal">
                <PlusIcon class="w-6 h-6" />
              </FwbButton>
            </template>
            <template #content>
              Tambah Siswa
            </template>
          </fwb-tooltip>
        </div>

        <!-- Bagian table -->
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
                    Nama Siswa
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Kelas
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Jenjang
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Sekolah
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Aksi
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-background-dark divide-y divide-gray-200 dark:divide-border-dark">
                <template v-if="loading">
                  <tr v-for="n in 5" :key="n" class="hover:bg-gray-50 dark:hover:bg-surface-dark">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
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
                  <tr v-for="siswa in paginatedSiswa" :key="siswa.id" 
                      class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                      @click="showSiswaDetail(siswa)">
                    <td class="px-6 py-4" @click.stop>
                      <Checkbox
                        v-model="selectedSiswaIds"
                        :value="siswa.id"
                      />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.nama_siswa }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.kelas_detail?.nama_kelas }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.jenjang_detail?.nama_jenjang }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.sekolah_detail?.nama_sekolah }}</td>
                    <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editSiswa(siswa)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Siswa
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton 
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteSiswa(siswa.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Siswa
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
                <div v-for="n in 5" :key="n" class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                  <div class="space-y-3">
                    <SkeletonLoader width="150px" />
                    <SkeletonLoader width="80px" />
                  </div>
                </div>
              </template>
              
              <template v-else>
                <div v-for="siswa in paginatedSiswa" :key="siswa.id" 
                     class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow cursor-pointer"
                     @click="showSiswaDetail(siswa)">
                  <div class="space-y-2">
                    <div class="font-medium">{{ siswa.username }}</div>
                    <div class="font-medium">{{ siswa.nama_siswa }}</div>
                    <div class="text-sm text-gray-500">
                      Kelas: {{ siswa.kelas_detail?.nama_kelas }}
                    </div>
                    <div class="flex space-x-2 pt-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editSiswa(siswa)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Siswa
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark" 
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteSiswa(siswa.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Siswa
                        </template>
                      </fwb-tooltip>
                    </div>
                  </div>
                </div>
              </template>
            </div>

          </div>
        </div>

      <!-- Modal Tambah Siswa -->
      <BaseModal v-model="showAddModal">
        <template #header>
          <div class="flex items-center">
            {{ selectedSiswa ? 'Edit Siswa' : 'Tambah Siswa' }}
          </div>
        </template>
        <template #body>
          <SiswaForm 
            :siswa="selectedSiswa"
            @submit="saveSiswa"
            @cancel="closeModal"
          />
        </template>
      </BaseModal>

      <!-- Modal Konfirmasi Hapus -->
      <BaseModal v-model="showDeleteModal">
        <template #header>
          <div class="flex items-center">
            Konfirmasi Hapus
          </div>
        </template>
        <template #body>
          <p>Apakah Anda yakin ingin menghapus siswa ini?</p>
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

      <!-- Modal Detail Siswa -->
      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            Detail Siswa
          </div>
        </template>
        <template #body>
          <div v-if="selectedSiswaDetail" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Username:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.username }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Nama Siswa:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.nama_siswa }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Kelas:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.kelas_detail?.nama_kelas }}</div>
              </div>

              <div class="w-full flex">
                <div class="w-1/2 font-medium">Jenjang:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.jenjang_detail?.nama_jenjang }}</div>
              </div>

              <div class="w-full flex">
                <div class="w-1/2 font-medium">Sekolah:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.sekolah_detail?.nama_sekolah }}</div>
              </div>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Bagian bawah table (Jumlah Siswa, Pagination) -->
      <div class="mt-4 flex justify-between gap-2">
        <div class="relative flex items-center gap-2 mt-4">
          <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
            Jumlah Siswa: {{ filteredSiswa.length }}
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

      <!-- Bagian bawah table (Hapus Siswa Terpilih) -->
      <div class="flex flex-wrap gap-2 mb-6">
          <fwb-tooltip v-if="selectedSiswaIds.length > 0">
            <template #trigger>
              <FwbButton
                color="dark"
                class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
                @click="bulkDelete"
              >
              <div class="flex flex-row gap-2 items-center justify-center p-1">
                <TrashIcon class="w-5 h-5" />
                <span>({{ selectedSiswaIds.length }})</span>
              </div>
                
              </FwbButton>
            </template>
            <template #content>
              Hapus Siswa Terpilih
            </template>
          </fwb-tooltip>
      </div>

    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/config/api'
import SiswaForm from '@/components/form/SiswaForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import { useNotifications } from '@/composables/useNotifications'

// State untuk data
const loading = ref(true)
const siswaList = ref([])
const showAddModal = ref(false)
const selectedSiswa = ref(null)
const showDeleteModal = ref(false)
const siswaToDelete = ref(null)
const showDetailModal = ref(false)
const selectedSiswaDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)

// State untuk filter
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const selectedFilters = ref({
  kelas: [],
  jenjang: [],
  sekolah: []
})

// Pagination
const itemsPerPage = 3
const currentPage = ref(1)

// Tambahkan setelah baris 423
const selectedSiswaIds = ref([])
const selectAll = ref(false)

// Computed properties
const filteredSiswa = computed(() => {
  let result = siswaList.value

  // Filter berdasarkan pencarian
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(siswa =>
      siswa.nama_siswa.toLowerCase().includes(query) ||
      siswa.username?.toLowerCase().includes(query)
    )
  }

  // Filter berdasarkan kelas
  if (selectedFilters.value.kelas.length > 0) {
    result = result.filter(siswa => 
      selectedFilters.value.kelas.includes(siswa.kelas_detail?.id)
    )
  }

  // Filter berdasarkan jenjang
  if (selectedFilters.value.jenjang.length > 0) {
    result = result.filter(siswa => 
      selectedFilters.value.jenjang.includes(siswa.jenjang_detail?.id)
    )
  }

  // Filter berdasarkan sekolah
  if (selectedFilters.value.sekolah.length > 0) {
    result = result.filter(siswa => 
      selectedFilters.value.sekolah.includes(siswa.sekolah_detail?.id)
    )
  }

  return result
})

const paginatedSiswa = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredSiswa.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredSiswa.value.length / itemsPerPage)
})

const activeFiltersCount = computed(() => {
  let count = 0
  count += selectedFilters.value.kelas.length
  count += selectedFilters.value.jenjang.length
  count += selectedFilters.value.sekolah.length
  return count
})

const { notify } = useNotifications()

const fetchSiswa = async () => {
  try {
    const response = await api.get('/siswa/')
    const siswaWithUsers = await Promise.all(
      response.data.map(async (siswa) => {
        try {
          const userResponse = await api.get(`/users/${siswa.user}/`)
          return {
            ...siswa,
            username: userResponse.data.username,
            kelas_detail: siswa.kelas_detail,
            jenjang_detail: siswa.jenjang_detail,
            sekolah_detail: siswa.sekolah_detail
          }
        } catch (error) {
          notify({
            type: 'warning',
            title: 'Peringatan',
            message: `Gagal mengambil data user untuk siswa ${siswa.nama_siswa}`
          })
          return {
            ...siswa,
            username: 'User tidak ditemukan'
          }
        }
      })
    )
    siswaList.value = siswaWithUsers
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data siswa'
    })
    console.error('Error fetching siswa:', error)
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedSiswa.value = null
  showAddModal.value = true
}

const editSiswa = (siswa) => {
  selectedSiswa.value = {
    id: siswa.id,
    user: siswa.user,
    user_detail: siswa.user_detail,
    nama_siswa: siswa.nama_siswa,
    kelas: siswa.kelas,
    jenjang: siswa.jenjang,
    sekolah: siswa.sekolah
  }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedSiswa.value = null
}

const saveSiswa = async (siswaData) => {
  try {
    // Pastikan format data sesuai dengan yang diharapkan backend
    const dataToSend = {
      user: parseInt(siswaData.user),
      nama_siswa: siswaData.nama_siswa,
      kelas: parseInt(siswaData.kelas),
      jenjang: parseInt(siswaData.jenjang),
      sekolah: parseInt(siswaData.sekolah)
    }

    if (selectedSiswa.value) {
      await api.put(`/siswa/${selectedSiswa.value.id}/`, dataToSend)
    } else {
      const response = await api.post('/siswa/', dataToSend)
    }
    
    closeModal()
    fetchSiswa()
    notify({
      type: 'success',
      title: 'Berhasil',
      message: selectedSiswa.value ? 'Data siswa berhasil diperbarui' : 'Siswa baru berhasil ditambahkan'
    })
  } catch (error) {
    console.error('Response error:', error.response?.data)
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.error || 
                        'Terjadi kesalahan saat menyimpan data siswa'
    notify({
      type: 'error',
      title: 'Gagal',
      message: errorMessage
    })
  }
}

const deleteSiswa = async (siswaId) => {
  siswaToDelete.value = siswaId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (siswaToDelete.value) {
      // Single delete
      await api.delete(`/siswa/${siswaToDelete.value}/`)
    } else {
      // Bulk delete
      await Promise.all(
        selectedSiswaIds.value.map(id => api.delete(`/siswa/${id}/`))
      )
    }
    
    notify({
      type: 'success',
      title: 'Berhasil',
      message: siswaToDelete.value ? 
        'Siswa berhasil dihapus' : 
        'Siswa terpilih berhasil dihapus'
    })
    
    showDeleteModal.value = false
    siswaToDelete.value = null
    selectedSiswaIds.value = []
    fetchSiswa()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus siswa'
    })
  }
}

const showSiswaDetail = (siswa) => {
  selectedSiswaDetail.value = siswa
  showDetailModal.value = true
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const filterDropdownRef = ref(null)

onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

const fetchFilterData = async () => {
  try {
    const [kelasRes, jenjangRes, sekolahRes] = await Promise.all([
      api.get('/kelas/'),
      api.get('/jenjang/'),
      api.get('/sekolah/')
    ])
    
    kelasList.value = kelasRes.data
    jenjangList.value = jenjangRes.data
    sekolahList.value = sekolahRes.data
    

  } catch (error) {
    console.error('Error fetching filter data:', error)
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat data filter'
    })
  }
}

const resetFilters = () => {
  selectedFilters.value = {
    kelas: [],
    jenjang: [],
    sekolah: []
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedSiswaIds.value = filteredSiswa.value.map(siswa => siswa.id)
  } else {
    selectedSiswaIds.value = []
  }
}

// Tambahkan watch untuk mengupdate selectAll
watch(selectedSiswaIds, (newValue) => {
  const allSelected = filteredSiswa.value.every(siswa => 
    newValue.includes(siswa.id)
  )
  selectAll.value = allSelected
})

const bulkDelete = async () => {
  try {
    if (selectedSiswaIds.value.length === 0) return
    
    showDeleteModal.value = true
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Terjadi kesalahan saat menghapus siswa'
    })
  }
}

onMounted(() => {
  fetchSiswa()
  fetchFilterData()
})
</script>
