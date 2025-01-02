<template>
  <Notifications ref="notificationsRef" />
  <TransitionWrapper>
    <div class="p-8 w-full">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Materi
      </h1>

      <!-- Bagian atas table (Search, Filter, Tambah Materi)-->
      <div class="flex flex-wrap items-center gap-2 mb-6">
        <!-- Search -->
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari nama materi..."
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
            leave-active-class="transition duration-75 ease-in"
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

                <!-- Filter Status -->
                <div class="mb-4">
                  <h3 class="font-medium mb-2">Status</h3>
                  <div class="flex flex-col space-y-2">
                    <Checkbox
                      v-model="selectedFilters.status"
                      value="aktif"
                    >
                      Aktif
                    </Checkbox>
                    <Checkbox
                      v-model="selectedFilters.status"
                      value="tidak_aktif"
                    >
                      Tidak Aktif
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
            Tambah Materi
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
                  Nama Materi
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
                  Status
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
                  <td v-for="i in 7" :key="i" class="px-6 py-4">
                    <SkeletonLoader :width="i === 1 ? '20px' : '150px'" />
                  </td>
                </tr>
              </template>

              <!-- Data -->
              <template v-else>
                <tr v-for="materi in paginatedMateri" :key="materi.id">
                  <td class="px-6 py-4">
                    <Checkbox
                      v-model="selectedMateriIds"
                      :value="materi.id"
                    />
                  </td>
                  <td class="px-6 py-4">{{ materi.nama_materi }}</td>
                  <td class="px-6 py-4">{{ materi.mata_pelajaran_detail?.nama_mata_pelajaran }}</td>
                  <td class="px-6 py-4">{{ materi.kelas_detail?.nama_kelas }}</td>
                  <td class="px-6 py-4">{{ materi.jenjang_detail?.nama_jenjang }}</td>
                  <td class="px-6 py-4">{{ materi.sekolah_detail?.nama_sekolah }}</td>
                  <td class="px-6 py-4">
                    <span 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      :class="materi.status === 'aktif' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                    >
                      {{ materi.status === 'aktif' ? 'Aktif' : 'Tidak Aktif' }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="editMateri(materi)"
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
                            @click="deleteMateri(materi.id)"
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
                            @click="viewMateri(materi)"
                          >
                            <EyeIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Lihat Materi
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
              <div v-for="materi in paginatedMateri" :key="materi.id" 
                   class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                <div class="space-y-2">
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <h3 class="font-medium">{{ materi.nama_materi }}</h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        {{ materi.mata_pelajaran_detail?.nama_mata_pelajaran }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Kelas: {{ materi.kelas_detail?.nama_kelas }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Sekolah: {{ materi.sekolah_detail?.nama_sekolah }}
                      </p>
                    </div>
                  </div>
                  <div class="flex justify-end space-x-2 mt-2">
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="editMateri(materi)"
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
                          @click="deleteMateri(materi.id)"
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
                          @click="viewMateri(materi)"
                        >
                          <EyeIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Lihat Materi
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
            Jumlah Materi: {{ filteredMateri.length }}
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
      <div class="flex flex-wrap gap-2 mb-6" v-if="selectedMateriIds.length > 0">
        <fwb-tooltip>
          <template #trigger>
            <FwbButton
              color="dark"
              class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
              @click="bulkDelete"
            >
              <div class="flex flex-row gap-2 items-center justify-center p-1">
                <TrashIcon class="w-5 h-5" />
                <span>({{ selectedMateriIds.length }})</span>
              </div>
            </FwbButton>
          </template>
          <template #content>
            Hapus Materi Terpilih
          </template>
        </fwb-tooltip>
      </div>
    </div>

    <!-- Modal Form -->
    <Modal 
      v-model="showAddModal"
      @close="closeModal"
    >
      <template #header>
        <h3 class="text-xl font-semibold">
          {{ selectedMateri ? 'Edit Materi' : 'Tambah Materi Baru' }}
        </h3>
      </template>
      <template #body>
        <MateriForm
          :materi="selectedMateri"
          :is-guru="true"
          :guru-data="guruData"
          @submit="saveMateri"
          @cancel="closeModal"
          @error="handleError"
        />
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal 
      v-model="showDeleteModal"
      @close="showDeleteModal = false"
    >
      <template #header>
        <h3 class="text-xl font-semibold">
          Konfirmasi Hapus
        </h3>
      </template>
      <template #body>
        <p class="mb-4">
          {{ materiToDelete ? 'Apakah Anda yakin ingin menghapus materi ini?' : `Apakah Anda yakin ingin menghapus ${selectedMateriIds.length} materi yang dipilih?` }}
        </p>
        <div class="flex justify-end gap-2">
          <FwbButton
            color="gray"
            @click="showDeleteModal = false"
          >
            Batal
          </FwbButton>
          <FwbButton
            color="red"
            @click="confirmDelete"
          >
            Hapus
          </FwbButton>
        </div>
      </template>
    </Modal>
  </TransitionWrapper>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '@/composables/useNotifications'
import { onClickOutside } from '@vueuse/core'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import Modal from '@/components/BaseModal.vue'
import MateriForm from '@/components/form/MateriForm.vue'
import Checkbox from '@/components/Checkbox.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import { PlusIcon, FunnelIcon, PencilIcon, TrashIcon, EyeIcon } from '@heroicons/vue/24/outline'
import api from '@/config/api'
import Notifications from '@/components/Notifications.vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'

// State
const materiList = ref([])
const selectedMateri = ref(null)
const showAddModal = ref(false)
const showDeleteModal = ref(false)
const materiToDelete = ref(null)
const loading = ref(false)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedMateriIds = ref([])
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
const itemsPerPage = 2
const currentPage = ref(1)

// Computed
const activeFiltersCount = computed(() => {
  return selectedFilters.value.mapel.length + 
         selectedFilters.value.kelas.length + 
         selectedFilters.value.jenjang.length +
         selectedFilters.value.sekolah.length +
         selectedFilters.value.status.length
})

const filteredMateri = computed(() => {
  let result = materiList.value

  // Filter berdasarkan search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(materi => 
      materi.nama_materi.toLowerCase().includes(query)
    )
  }

  // Filter berdasarkan mata pelajaran
  if (selectedFilters.value.mapel.length > 0) {
    result = result.filter(materi => 
      selectedFilters.value.mapel.includes(materi.mata_pelajaran)
    )
  }

  // Filter berdasarkan kelas
  if (selectedFilters.value.kelas.length > 0) {
    result = result.filter(materi => 
      selectedFilters.value.kelas.includes(materi.kelas)
    )
  }

  // Filter berdasarkan jenjang
  if (selectedFilters.value.jenjang.length > 0) {
    result = result.filter(materi => 
      selectedFilters.value.jenjang.includes(materi.jenjang)
    )
  }

  // Filter berdasarkan sekolah
  if (selectedFilters.value.sekolah.length > 0) {
    result = result.filter(materi => 
      selectedFilters.value.sekolah.includes(materi.sekolah)
    )
  }

  // Filter berdasarkan status
  if (selectedFilters.value.status.length > 0) {
    result = result.filter(materi =>
      selectedFilters.value.status.includes(materi.status)
    )
  }

  return result
})

const paginatedMateri = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredMateri.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredMateri.value.length / itemsPerPage)
})

// Methods
const fetchMateri = async () => {
  try {
    loading.value = true
    const response = await api.get('/materi/')
    materiList.value = response.data
  } catch (error) {
    console.error('Error fetching materi:', error)
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal memuat data materi'
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

const showModal = () => {
  selectedMateri.value = null
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedMateri.value = null
  formData.value = {
    nama_materi: '',
    kelas: '',
    jenjang: '',
    mata_pelajaran: '',
    sekolah: '',
    status: 'aktif',
    file_materi: null
  }
}

const saveMateri = async (materiData) => {
  try {
    if (selectedMateri.value) {
      await api.put(`/materi/${selectedMateri.value.id}/`, materiData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Materi berhasil diperbarui'
      })
    } else {
      await api.post('/materi/', materiData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Materi baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchMateri()
  } catch (error) {
    console.error('Error:', error.response?.data || error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.error || 'Terjadi kesalahan saat menyimpan materi'
    })
  }
}

const editMateri = (materi) => {
  selectedMateri.value = materi
  showAddModal.value = true
}

const deleteMateri = (id) => {
  materiToDelete.value = id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (materiToDelete.value) {
      // Single delete
      await api.delete(`/materi/${materiToDelete.value}/`)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Materi berhasil dihapus'
      })
    } else {
      // Bulk delete
      await api.post('/materi/bulk-delete/', {
        ids: selectedMateriIds.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: `${selectedMateriIds.value.length} materi berhasil dihapus`
      })
      selectedMateriIds.value = []
      selectAll.value = false
    }
    showDeleteModal.value = false
    materiToDelete.value = null
    fetchMateri()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus materi'
    })
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedMateriIds.value = filteredMateri.value.map(materi => materi.id)
  } else {
    selectedMateriIds.value = []
  }
}

const viewMateri = (materi) => {
  router.push({
    name: 'MateriViewer',
    params: {
      materiId: materi.id,
      title: encodeURIComponent(materi.nama_materi)
    }
  })
}

const bulkDelete = async () => {
  try {
    if (selectedMateriIds.value.length === 0) return
    
    showDeleteModal.value = true
    materiToDelete.value = null // Set null untuk menandakan bulk delete
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Terjadi kesalahan saat menghapus materi'
    })
  }
}

const resetFilters = () => {
  selectedFilters.value = {
    mapel: [],
    kelas: [],
    jenjang: [],
    sekolah: [],
    status: []
  }
}

// Click outside handler
const filterDropdownRef = ref(null)
onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

// Watch
watch([searchQuery, selectedFilters], () => {
  currentPage.value = 1
})

// Lifecycle hooks
onMounted(async () => {
  await fetchGuruData()
  await fetchFilterData()
})

// Notifications
const { notify } = useNotifications()
const notificationsRef = ref(null)
const router = useRouter()

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

// Tambahkan di bagian state (setelah baris 378)
const formData = ref({
  nama_materi: '',
  kelas: '',
  jenjang: '',
  mata_pelajaran: '',
  sekolah: '',
  status: 'aktif',
  file_materi: null
})

// Tambahkan method untuk update form data
const updateFormData = (newValue) => {
  formData.value = newValue
}

// Tambahkan state untuk menyimpan data guru
const guruData = ref(null)

// Tambahkan fungsi untuk mengambil data guru saat komponen dimount
const fetchGuruData = async () => {
  try {
    loading.value = true
    const response = await api.get('/user/profile/')
    guruData.value = response.data
    
    // Set kelas berdasarkan jenjang guru
    if (guruData.value?.jenjang) {
      try {
        const response = await api.get('/guru/kelas-by-jenjang/', {
          params: {
            jenjang_id: guruData.value.jenjang
          }
        })
        kelasList.value = response.data
      } catch (error) {
        console.error('Error fetching kelas:', error)
      }
    }
    
    // Setelah mendapatkan data guru, fetch materi
    await fetchMateri()
  } catch (error) {
    console.error('Error fetching guru data:', error.response?.data || error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data guru'
    })
  } finally {
    loading.value = false
  }
}
</script> 
