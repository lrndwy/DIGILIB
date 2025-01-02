<template>
  <Notifications ref="notificationsRef" />
  <TransitionWrapper>
    <div class="p-8 w-full">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Buku
      </h1>

      <!-- Bagian atas table (Search, Filter, Tambah Buku)-->
      <div class="flex flex-wrap items-center gap-2 mb-6">
        <!-- Search -->
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari nama buku..."
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

                <!-- Filter Sekolah (hanya tampil untuk admin) -->
                <div v-if="isAdmin" class="mb-4">
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
            Tambah Buku
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
                  Cover
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Nama Buku
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Penerbit
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Mata Pelajaran
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                  Kelas
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
              <template v-if="loading">
                <tr v-for="n in 5" :key="n">
                  <td v-for="i in 8" :key="i" class="px-6 py-4 whitespace-nowrap">
                    <SkeletonLoader :width="i === 1 ? '20px' : '150px'" />
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr v-for="buku in paginatedBuku" :key="buku.id" 
                    class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                    @click="showBukuDetail(buku)">
                  <td class="px-6 py-4" @click.stop>
                    <Checkbox
                      v-model="selectedBukuIds"
                      :value="buku.id"
                    />
                  </td>
                  <td class="px-6 py-4">
                    <div class="w-24 h-32">
                      <template v-if="buku.file_buku.endsWith('.pdf')">
                        <PDFCover :file-url="buku.file_buku" />
                      </template>
                      <template v-else>
                        <div class="w-full h-full bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                          <div class="text-center">
                            <DocumentTextIcon class="w-12 h-12 mx-auto text-gray-400" />
                            <span class="text-xs text-gray-500">
                              {{ buku.file_buku.split('.').pop().toUpperCase() }}
                            </span>
                          </div>
                        </div>
                      </template>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ buku.nama_buku }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ buku.penerbit }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ buku.mata_pelajaran_detail?.nama_mata_pelajaran }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ buku.kelas_detail?.nama_kelas }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ buku.sekolah_detail?.nama_sekolah || 'Umum' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="{
                      'px-2 py-1 text-xs font-medium rounded-full': true,
                      'bg-green-100 text-green-800': buku.status === 'aktif',
                      'bg-red-100 text-red-800': buku.status === 'tidak_aktif'
                    }">
                      {{ buku.status === 'aktif' ? 'Aktif' : 'Tidak Aktif' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editBuku(buku)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Buku
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteBuku(buku.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Buku
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click.stop="viewBuku(buku)"
                        >
                          <EyeIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Lihat Buku
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
              <div v-for="buku in paginatedBuku" :key="buku.id" 
                   class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                <div class="space-y-2">
                  <div class="flex justify-between items-start">
                    <div class="w-24 h-32 mr-4">
                      <template v-if="buku.file_buku.endsWith('.pdf')">
                        <PDFCover :file-url="buku.file_buku" />
                      </template>
                      <template v-else>
                        <div class="w-full h-full bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                          <div class="text-center">
                            <DocumentTextIcon class="w-12 h-12 mx-auto text-gray-400" />
                            <span class="text-xs text-gray-500">
                              {{ buku.file_buku.split('.').pop().toUpperCase() }}
                            </span>
                          </div>
                        </div>
                      </template>
                    </div>
                    <div class="flex-1">
                      <h3 class="font-medium">{{ buku.nama_buku }}</h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ buku.penerbit }}</p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        {{ buku.mata_pelajaran_detail?.nama_mata_pelajaran }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        Kelas: {{ buku.kelas_detail?.nama_kelas }}
                      </p>
                      <span :class="{
                        'px-2 py-1 text-xs font-medium rounded-full': true,
                        'bg-green-100 text-green-800': buku.status === 'aktif',
                        'bg-red-100 text-red-800': buku.status === 'tidak_aktif'
                      }">
                        {{ buku.status === 'aktif' ? 'Aktif' : 'Tidak Aktif' }}
                      </span>
                    </div>
                  </div>
                  <div class="flex justify-end space-x-2 mt-2">
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="editBuku(buku)"
                        >
                          <PencilIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Edit Buku
                      </template>
                    </fwb-tooltip>
                    <fwb-tooltip>
                      <template #trigger>
                        <FwbButton
                          color="dark"
                          class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                          @click="deleteBuku(buku.id)"
                        >
                          <TrashIcon class="w-4 h-4" />
                        </FwbButton>
                      </template>
                      <template #content>
                        Hapus Buku
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
            Jumlah Buku: {{ filteredBuku.length }}
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
      <div class="flex flex-wrap gap-2 mb-6" v-if="selectedBukuIds.length > 0">
        <fwb-tooltip>
          <template #trigger>
            <FwbButton
              color="dark"
              class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
              @click="bulkDelete"
            >
              <div class="flex flex-row gap-2 items-center justify-center p-1">
                <TrashIcon class="w-5 h-5" />
                <span>({{ selectedBukuIds.length }})</span>
              </div>
            </FwbButton>
          </template>
          <template #content>
            Hapus Buku Terpilih
          </template>
        </fwb-tooltip>
      </div>

      <!-- Modals -->
      <BaseModal v-model="showAddModal">
        <template #header>
          <div class="flex items-center">
            {{ selectedBuku ? 'Edit Buku' : 'Tambah Buku' }}
          </div>
        </template>
        <template #body>
          <BukuForm 
            :buku="selectedBuku"
            :is-guru="true"
            :guru-data="guruData"
            @submit="saveBuku"
            @cancel="closeModal"
          />
        </template>
      </BaseModal>

      <BaseModal v-model="showDeleteModal">
        <template #header>
          <div class="flex items-center">
            Konfirmasi Hapus
          </div>
        </template>
        <template #body>
          <p v-if="bukuToDelete">
            Apakah Anda yakin ingin menghapus buku ini?
          </p>
          <p v-else>
            Apakah Anda yakin ingin menghapus {{ selectedBukuIds.length }} buku yang dipilih?
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
            class="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white"
            @click="confirmDelete"
          >
            Hapus
          </FwbButton>
        </template>
      </BaseModal>

      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            Detail Buku
          </div>
        </template>
        <template #body>
          <div v-if="selectedBukuDetail" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <div class="w-full flex justify-center mb-4">
                <div class="w-32 h-48">
                  <template v-if="selectedBukuDetail.file_buku.endsWith('.pdf')">
                    <PDFCover :file-url="selectedBukuDetail.file_buku" />
                  </template>
                  <template v-else>
                    <div class="w-full h-full bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                      <div class="text-center">
                        <DocumentTextIcon class="w-12 h-12 mx-auto text-gray-400" />
                        <span class="text-xs text-gray-500">
                          {{ selectedBukuDetail.file_buku.split('.').pop().toUpperCase() }}
                        </span>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Nama Buku:</div>
                <div class="w-1/2">{{ selectedBukuDetail.nama_buku }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Penerbit:</div>
                <div class="w-1/2">{{ selectedBukuDetail.penerbit }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Mata Pelajaran:</div>
                <div class="w-1/2">{{ selectedBukuDetail.mata_pelajaran_detail?.nama_mata_pelajaran }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Kelas:</div>
                <div class="w-1/2">{{ selectedBukuDetail.kelas_detail?.nama_kelas }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Status:</div>
                <div class="w-1/2">
                  <span :class="{
                    'px-2 py-1 text-xs font-medium rounded-full': true,
                    'bg-green-100 text-green-800': selectedBukuDetail.status === 'aktif',
                    'bg-red-100 text-red-800': selectedBukuDetail.status === 'tidak_aktif'
                  }">
                    {{ selectedBukuDetail.status === 'aktif' ? 'Aktif' : 'Tidak Aktif' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </BaseModal>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/config/api'
import BukuForm from '@/components/form/BukuForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon, DocumentTextIcon, EyeIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import PDFCover from '@/components/PDFCover.vue'
import { useNotifications } from '@/composables/useNotifications'
import Notifications from '@/components/Notifications.vue'

// State
const loading = ref(true)
const bukuList = ref([])
const showAddModal = ref(false)
const selectedBuku = ref(null)
const showDeleteModal = ref(false)
const bukuToDelete = ref(null)
const showDetailModal = ref(false)
const selectedBukuDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedBukuIds = ref([])
const selectAll = ref(false)

// Filter lists
const mapelList = ref([])
const kelasList = ref([])
const sekolahList = ref([])
const selectedFilters = ref({
  mapel: [],
  kelas: [],
  status: [],
  sekolah: []
})

// Pagination
const itemsPerPage = 5
const currentPage = ref(1)

// Computed
const activeFiltersCount = computed(() => {
  let count = selectedFilters.value.mapel.length + 
              selectedFilters.value.kelas.length + 
              selectedFilters.value.status.length
              
  // Hanya tambahkan filter sekolah jika user adalah admin
  if (isAdmin.value) {
    count += selectedFilters.value.sekolah.length
  }
  
  return count
})

const filteredBuku = computed(() => {
  let result = bukuList.value

  // Filter berdasarkan pencarian
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(buku =>
      buku.nama_buku.toLowerCase().includes(query) ||
      buku.penerbit.toLowerCase().includes(query)
    )
  }

  // Filter berdasarkan mata pelajaran
  if (selectedFilters.value.mapel.length > 0) {
    result = result.filter(buku => 
      selectedFilters.value.mapel.includes(buku.mata_pelajaran_detail?.id)
    )
  }

  // Filter berdasarkan kelas
  if (selectedFilters.value.kelas.length > 0) {
    result = result.filter(buku => 
      selectedFilters.value.kelas.includes(buku.kelas_detail?.id)
    )
  }

  // Filter berdasarkan status
  if (selectedFilters.value.status.length > 0) {
    result = result.filter(buku =>
      selectedFilters.value.status.includes(buku.status)
    )
  }

  // Filter berdasarkan sekolah
  if (selectedFilters.value.sekolah.length > 0) {
    result = result.filter(buku => 
      selectedFilters.value.sekolah.includes(buku.sekolah)
    )
  }

  return result
})

const paginatedBuku = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredBuku.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredBuku.value.length / itemsPerPage)
})

// Methods
const fetchBuku = async () => {
  try {
    if (!guruData.value?.nama_mata_pelajaran) {
      console.warn('Data guru belum tersedia')
      return
    }
    
    const response = await api.get('/buku/by_guru/')
    bukuList.value = response.data.map(buku => ({
      ...buku,
      mata_pelajaran_detail: buku.mata_pelajaran_detail,
      kelas_detail: buku.kelas_detail
    }))
  } catch (error) {
    console.error('Error fetching buku:', error.response?.data || error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.error || 'Gagal mengambil data buku'
    })
  }
}

const fetchFilterData = async () => {
  try {
    // Jika admin, ambil data sekolah
    if (isAdmin.value) {
      const sekolahResponse = await api.get('/sekolah/')
      sekolahList.value = sekolahResponse.data
    }

    // Set mapelList dari data guru
    if (guruData.value?.nama_mata_pelajaran_detail) {
      mapelList.value = [guruData.value.nama_mata_pelajaran_detail]
    }

    // Set kelasList dari data guru berdasarkan jenjang
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
  } catch (error) {
    console.error('Error fetching filter data:', error)
  }
}

const showModal = () => {
  selectedBuku.value = null
  showAddModal.value = true
}

const editBuku = (buku) => {
  selectedBuku.value = {
    id: buku.id,
    nama_buku: buku.nama_buku,
    penerbit: buku.penerbit,
    mata_pelajaran: buku.mata_pelajaran,
    kelas: buku.kelas,
    jenjang: buku.jenjang,
    sekolah: buku.sekolah,
    status: buku.status,
    file_buku: buku.file_buku
  }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedBuku.value = null
}

const saveBuku = async (bukuData) => {
  try {
    if (selectedBuku.value) {
      await api.put(`/buku/${selectedBuku.value.id}/`, bukuData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Buku berhasil diperbarui'
      })
    } else {
      await api.post('/buku/', bukuData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Buku baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchBuku()
  } catch (error) {
    console.error('Error:', error.response?.data || error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.error || 'Terjadi kesalahan saat menyimpan buku'
    })
  }
}

const deleteBuku = (id) => {
  bukuToDelete.value = id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (bukuToDelete.value) {
      // Single delete
      await api.delete(`/buku/${bukuToDelete.value}/`)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Buku berhasil dihapus'
      })
    } else {
      // Bulk delete
      await api.post('/buku/bulk-delete/', {
        ids: selectedBukuIds.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      notify({
        type: 'success',
        title: 'Berhasil',
        message: `${selectedBukuIds.value.length} buku berhasil dihapus`
      })
      selectedBukuIds.value = []
      selectAll.value = false
    }
    showDeleteModal.value = false
    bukuToDelete.value = null
    fetchBuku()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus buku'
    })
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedBukuIds.value = filteredBuku.value.map(buku => buku.id)
  } else {
    selectedBukuIds.value = []
  }
}

const showBukuDetail = (buku) => {
  selectedBukuDetail.value = buku
  showDetailModal.value = true
}

const filterDropdownRef = ref(null)
const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

// Tutup dropdown filter saat klik di luar
onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

// Reset halaman saat filter atau pencarian berubah
watch([searchQuery, selectedFilters], () => {
  currentPage.value = 1
})

// Tambahkan state untuk menyimpan data guru
const guruData = ref(null)

// Tambahkan fungsi untuk mengambil data guru saat komponen dimount
const fetchGuruData = async () => {
  try {
    loading.value = true
    const response = await api.get('/user/profile/')
    guruData.value = response.data
    
    // Setelah mendapatkan data guru, fetch buku berdasarkan mata pelajaran guru
    await fetchBuku()
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

// Panggil fetchGuruData saat komponen dimount
onMounted(async () => {
  await fetchGuruData() // Ini akan memanggil fetchBuku setelah mendapatkan data guru
  await fetchFilterData()
})

// Notifikasi
const { notify } = useNotifications()
const notificationsRef = ref(null)

const router = useRouter()

const viewBuku = (buku) => {
  router.push({
    name: 'BukuViewer',
    params: {
      bookId: buku.id,
      title: encodeURIComponent(buku.nama_buku)
    }
  })
}

const bulkDelete = async () => {
  try {
    if (selectedBukuIds.value.length === 0) return
    
    showDeleteModal.value = true
    bukuToDelete.value = null // Set null untuk menandakan bulk delete
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Terjadi kesalahan saat menghapus buku'
    })
  }
}

const resetFilters = () => {
  selectedFilters.value = {
    mapel: [],
    kelas: [],
    status: [],
    sekolah: []
  }
}

// Tambahkan computed property isAdmin
const isAdmin = computed(() => {
  return guruData.value?.role === 'admin'
})
</script>
