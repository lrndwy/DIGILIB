<template>
  <Notifications ref="notificationsRef" />
  <TransitionWrapper>
    <div class="p-8 w-full">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Perangkat Kurikulum
      </h1>

      <!-- Bagian atas table (Search, Filter, Tambah) -->
      <div class="flex flex-wrap items-center gap-2 mb-6">
        <!-- Search -->
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari nama perangkat..."
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

          <!-- Filter Dropdown -->
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <div v-show="showFilterDropdown" class="absolute right-0 mt-2 w-72 bg-white dark:bg-surface-dark rounded-lg shadow-lg border border-border-light dark:border-border-dark z-30">
              <div class="p-4 max-h-[400px] overflow-y-auto">
                <!-- Header dengan Reset Filter -->
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

                <!-- Filter Mata Pelajaran -->
                <div class="mb-4">
                  <h3 class="font-medium mb-2">Mata Pelajaran</h3>
                  <div class="flex flex-col space-y-2">
                    <Checkbox
                      v-for="mapel in mapelList"
                      :key="mapel.id"
                      v-model="selectedFilters.mapel"
                      :value="mapel.id"
                    >
                      {{ mapel.nama_mata_pelajaran }}
                    </Checkbox>
                  </div>
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

        <!-- Tambah Button -->
        <fwb-tooltip>
          <template #trigger>
            <FwbButton 
              color="dark" 
              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" 
              @click="showModal"
            >
              <PlusIcon class="w-6 h-6" />
            </FwbButton>
          </template>
          <template #content>
            Tambah Perangkat
          </template>
        </fwb-tooltip>
      </div>



      <!-- Table -->
      <div class="overflow-x-auto rounded-lg lg:border lg:border-gray-200 dark:border-border-dark">
        <div class="inline-block min-w-full align-middle">
          <!-- Desktop Table -->
          <table class="hidden md:table min-w-full divide-y divide-gray-200 dark:divide-border-dark">
            <thead class="bg-surface-light dark:bg-surface-dark">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  <Checkbox
                    v-model="selectAll"
                    @change="toggleSelectAll"
                  />
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Nama Perangkat
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Mata Pelajaran
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
              <!-- Loading State -->
              <template v-if="loading">
                <tr v-for="n in 5" :key="n">
                  <td v-for="i in 7" :key="i" class="px-6 py-4 whitespace-nowrap">
                    <SkeletonLoader :width="i === 1 ? '20px' : '150px'" />
                  </td>
                </tr>
              </template>

              <!-- Data -->
              <template v-else>
                <tr v-for="perangkat in paginatedPerangkat" :key="perangkat.id">
                  <td class="px-6 py-4">
                    <Checkbox
                      v-model="selectedPerangkatIds"
                      :value="perangkat.id"
                    />
                  </td>
                  <td class="px-6 py-4">{{ perangkat.nama_perangkat_kurikulum }}</td>
                  <td class="px-6 py-4">{{ perangkat.mata_pelajaran_detail?.nama_mata_pelajaran }}</td>
                  <td class="px-6 py-4">{{ perangkat.kelas_detail?.nama_kelas }}</td>
                  <td class="px-6 py-4">{{ perangkat.jenjang_detail?.nama_jenjang }}</td>
                  <td class="px-6 py-4">{{ perangkat.sekolah_detail?.nama_sekolah }}</td>
                  <td class="px-6 py-4">
                    <div class="flex items-center space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="editPerangkat(perangkat)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="deletePerangkat(perangkat.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="viewPerangkat(perangkat)"
                          >
                            <EyeIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Lihat Perangkat
                        </template>
                      </fwb-tooltip>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>

          <!-- Mobile View -->
          <div class="block md:hidden">
            <template v-if="loading">
              <div v-for="n in 5" :key="n" class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                <div class="space-y-2">
                  <SkeletonLoader width="150px" />
                  <SkeletonLoader width="100px" />
                  <SkeletonLoader width="80px" />
                </div>
              </div>
            </template>
            <template v-else>
              <div v-for="perangkat in paginatedPerangkat" :key="perangkat.id" 
                   class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                <div class="space-y-2">
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <h3 class="font-medium">{{ perangkat.nama_perangkat_kurikulum }}</h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        {{ perangkat.mata_pelajaran_detail?.nama_mata_pelajaran }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Kelas: {{ perangkat.kelas_detail?.nama_kelas }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Jenjang: {{ perangkat.jenjang_detail?.nama_jenjang }}
                      </p>
                    </div>
                  </div>
                  <div class="flex justify-end space-x-2 mt-2">
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="editPerangkat(perangkat)"
                        >
                          <PencilIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Edit
                      </template>
                    </fwb-tooltip>
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="deletePerangkat(perangkat.id)"
                        >
                          <TrashIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Hapus
                      </template>
                    </fwb-tooltip>
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="viewPerangkat(perangkat)"
                        >
                          <EyeIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Lihat Perangkat
                      </template>
                    </fwb-tooltip>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-4 flex justify-between gap-2">
        <div class="relative flex items-center gap-2 mt-4">
          <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
            Jumlah Perangkat: {{ filteredPerangkat.length }}
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

      <!-- Bulk Actions -->
      <div class="flex flex-wrap gap-2 mb-6" v-if="selectedPerangkatIds.length > 0">
        <fwb-tooltip>
          <template #trigger>
            <FwbButton
              color="dark"
              class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
              @click="bulkDelete"
            >
              <div class="flex flex-row gap-2 items-center justify-center p-1">
                <TrashIcon class="w-5 h-5" />
                <span>({{ selectedPerangkatIds.length }})</span>
              </div>
            </FwbButton>
          </template>
          <template #content>
            Hapus Perangkat Terpilih
          </template>
        </fwb-tooltip>
      </div>

      <BaseModal v-model="showAddModal">
        <template #header>
          <h3 class="text-xl font-semibold">
            {{ selectedPerangkat ? 'Edit Perangkat' : 'Tambah Perangkat' }}
          </h3>
        </template>
        <template #body>
          <PerangkatKurikulumForm
            :perangkat="selectedPerangkat"
            @submit="savePerangkat"
            @cancel="closeModal"
            @error="notify"
          />
        </template>
      </BaseModal>

      <!-- Delete Confirmation Modal -->
      <BaseModal v-model="showDeleteModal">
        <template #header>
          <h3 class="text-xl font-semibold">Konfirmasi Hapus</h3>
        </template>
        <template #body>
          <p class="text-gray-600 dark:text-gray-400">
            {{ perangkatToDelete ? 'Apakah Anda yakin ingin menghapus perangkat ini?' : 
              `Apakah Anda yakin ingin menghapus ${selectedPerangkatIds.length} perangkat yang dipilih?` }}
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
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/config/api'
import PerangkatKurikulumForm from '@/components/form/PerangkatKurikulumForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import { useNotifications } from '@/composables/useNotifications'
import Notifications from '@/components/Notifications.vue'
import { EyeIcon } from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'

// State
const loading = ref(true)
const perangkatList = ref([])
const showAddModal = ref(false)
const selectedPerangkat = ref(null)
const showDeleteModal = ref(false)
const perangkatToDelete = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedPerangkatIds = ref([])
const selectAll = ref(false)

// Filter lists
const mapelList = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])
const selectedFilters = ref({
  mapel: [],
  kelas: [],
  jenjang: [],
  sekolah: [],
  status: []
})

// Pagination
const itemsPerPage = 5
const currentPage = ref(1)

// Computed
const activeFiltersCount = computed(() => {
  return selectedFilters.value.mapel.length + 
         selectedFilters.value.kelas.length + 
         selectedFilters.value.jenjang.length +
         selectedFilters.value.sekolah.length +
         selectedFilters.value.status.length
})

const filteredPerangkat = computed(() => {
  let result = perangkatList.value

  // Filter berdasarkan search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(perangkat => 
      perangkat.nama_perangkat_kurikulum.toLowerCase().includes(query)
    )
  }

  // Filter berdasarkan mata pelajaran
  if (selectedFilters.value.mapel.length > 0) {
    result = result.filter(perangkat => 
      selectedFilters.value.mapel.includes(perangkat.mata_pelajaran)
    )
  }

  // Filter berdasarkan kelas
  if (selectedFilters.value.kelas.length > 0) {
    result = result.filter(perangkat => 
      selectedFilters.value.kelas.includes(perangkat.kelas)
    )
  }

  // Filter berdasarkan jenjang
  if (selectedFilters.value.jenjang.length > 0) {
    result = result.filter(perangkat => 
      selectedFilters.value.jenjang.includes(perangkat.jenjang)
    )
  }

  // Filter berdasarkan sekolah
  if (selectedFilters.value.sekolah.length > 0) {
    result = result.filter(perangkat => 
      selectedFilters.value.sekolah.includes(perangkat.sekolah)
    )
  }

  return result
})

const paginatedPerangkat = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredPerangkat.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredPerangkat.value.length / itemsPerPage)
})

// Tambahkan method-method berikut di dalam script setup, setelah computed properties

const showModal = () => {
  selectedPerangkat.value = null
  showAddModal.value = true
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPerangkatIds.value = filteredPerangkat.value.map(perangkat => perangkat.id)
  } else {
    selectedPerangkatIds.value = []
  }
}

// Tambahkan watch untuk mengupdate selectAll
watch(selectedPerangkatIds, (newValue) => {
  const allSelected = filteredPerangkat.value.every(perangkat => 
    newValue.includes(perangkat.id)
  )
  selectAll.value = allSelected
})

// Methods
const fetchPerangkat = async () => {
  try {
    loading.value = true
    const response = await api.get('/perangkat-kurikulum/')
    perangkatList.value = response.data
  } catch (error) {
    console.error('Error fetching perangkat:', error)
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat data perangkat kurikulum'
    })
  } finally {
    loading.value = false
  }
}

const fetchFilterData = async () => {
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
    console.error('Error fetching filter data:', error)
  }
}

const closeModal = () => {
  showAddModal.value = false
  selectedPerangkat.value = null
}

const savePerangkat = async (perangkatData) => {
  try {
    const formData = new FormData()
    
    // Append semua field non-file
    formData.append('nama_perangkat_kurikulum', perangkatData.get('nama_perangkat_kurikulum'))
    formData.append('kelas', perangkatData.get('kelas'))
    formData.append('jenjang', perangkatData.get('jenjang'))
    formData.append('mata_pelajaran', perangkatData.get('mata_pelajaran'))
    formData.append('sekolah', perangkatData.get('sekolah'))
    formData.append('status', perangkatData.get('status') || 'aktif')

    // Handle file jika ada file baru
    const file = perangkatData.get('file_perangkat_kurikulum')
    if (file instanceof File) {
      formData.append('file_perangkat_kurikulum', file)
    }

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }

    if (selectedPerangkat.value) {
      await api.put(`/perangkat-kurikulum/${selectedPerangkat.value.id}/`, formData, config)
    } else {
      await api.post('/perangkat-kurikulum/', formData, config)
    }

    closeModal()
    fetchPerangkat()
    notify({
      type: 'success',
      title: 'Berhasil',
      message: selectedPerangkat.value ? 'Perangkat berhasil diperbarui' : 'Perangkat berhasil ditambahkan'
    })
  } catch (error) {
    console.error('Error saving perangkat:', error.response?.data || error)
    notify({
      type: 'error',
      title: 'Error',
      message: error.response?.data?.file_perangkat_kurikulum?.[0] || 'Gagal menyimpan perangkat kurikulum'
    })
  }
}

const editPerangkat = (perangkat) => {
  selectedPerangkat.value = {
    id: perangkat.id,
    nama_perangkat_kurikulum: perangkat.nama_perangkat_kurikulum,
    kelas: perangkat.kelas,
    jenjang: perangkat.jenjang,
    mata_pelajaran: perangkat.mata_pelajaran,
    sekolah: perangkat.sekolah,
    status: perangkat.status,
    file_perangkat_kurikulum: perangkat.file_perangkat_kurikulum
  }
  showAddModal.value = true
}

const deletePerangkat = (id) => {
  perangkatToDelete.value = id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (perangkatToDelete.value) {
      // Single delete
      await api.delete(`/perangkat-kurikulum/${perangkatToDelete.value}/`)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Perangkat kurikulum berhasil dihapus'
      })
    } else {
      // Bulk delete
      await api.post('/perangkat-kurikulum/bulk-delete/', {
        ids: selectedPerangkatIds.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: `${selectedPerangkatIds.value.length} perangkat kurikulum berhasil dihapus`
      })
      selectedPerangkatIds.value = []
      selectAll.value = false
    }
    showDeleteModal.value = false
    perangkatToDelete.value = null
    fetchPerangkat()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus perangkat kurikulum'
    })
  }
}

const isFile = (value) => {
  return value && 
    typeof value === 'object' && 
    'name' in value && 
    'size' in value && 
    'type' in value && 
    value instanceof File
}

const router = useRouter()

const viewPerangkat = (perangkat) => {
  router.push({
    name: 'PerangkatViewer',
    params: {
      perangkatId: perangkat.id,
      title: encodeURIComponent(perangkat.nama_perangkat_kurikulum)
    }
  })
}

// Tambahkan method resetFilters
const resetFilters = () => {
  selectedFilters.value = {
    mapel: [],
    kelas: [],
    jenjang: [],
    sekolah: [],
    status: []
  }
}

// Tambahkan watch untuk reset halaman saat filter berubah
watch([searchQuery, selectedFilters], () => {
  currentPage.value = 1
})

// Tambahkan click outside handler
const filterDropdownRef = ref(null)
onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

// Lifecycle hooks
onMounted(async () => {
  await Promise.all([
    fetchPerangkat(),
    fetchFilterData()
  ])
})

// Notifications
const { notify } = useNotifications()
const notificationsRef = ref(null)

const bulkDelete = async () => {
  try {
    if (selectedPerangkatIds.value.length === 0) return
    
    showDeleteModal.value = true
    perangkatToDelete.value = null // Set null untuk menandakan bulk delete
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Terjadi kesalahan saat menghapus perangkat'
    })
  }
}
</script> 
