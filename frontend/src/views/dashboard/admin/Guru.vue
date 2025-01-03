<template>
  <TransitionWrapper>
    <div class="p-8 w-full">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Guru
      </h1>

          <!-- Bagian atas table (Search, Filter, Tambah Guru)-->
          <div class="flex flex-wrap items-center gap-2 mb-6">
            <!-- Search -->
            <div class="flex-1">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Cari nama guru..."
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

            <!-- Tambah Guru -->
            <fwb-tooltip>
              <template #trigger>
                <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="showModal">
                  <PlusIcon class="w-6 h-6" />
                </FwbButton>
              </template>
              <template #content>
                Tambah Guru
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
                      Nama Guru
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
                      Akses CRUD
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Aksi
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200 dark:divide-border-dark dark:bg-background-dark">
                  <template v-if="loading">
                    <tr v-for="n in 5" :key="n" class="hover:bg-gray-50">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="150px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="150px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="120px" />
                      </td>
                    </tr>
                  </template>
                  <template v-else>
                    <tr v-for="guru in filteredGuru" :key="guru.id" 
                        class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                        @click="showGuruDetail(guru)">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <Checkbox
                          v-model="selectedGuruIds"
                          :value="guru.id"
                          @click.stop
                        />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">{{ guru.username }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">{{ guru.nama_guru }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">{{ guru.nama_mata_pelajaran_detail?.nama_mata_pelajaran || '-' }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ guru.kelas_detail?.map(k => k.nama_kelas).join(', ') || '-' }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">{{ guru.jenjang_detail?.nama_jenjang || '-' }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">{{ guru.sekolah_detail?.nama_sekolah || '-' }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex flex-col gap-2">
                          <!-- Badge untuk CRUD Buku -->
                          <div class="inline-flex items-center">
                            <span class="text-xs font-medium mr-2">Buku:</span>
                            <span 
                              :class="[
                                'px-2 py-1 text-xs font-medium rounded-full',
                                guru.crud_buku 
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                              ]"
                            >
                              {{ guru.crud_buku ? 'Diizinkan' : 'Tidak Diizinkan' }}
                            </span>
                          </div>

                          <!-- Badge untuk CRUD Materi -->
                          <div class="inline-flex items-center">
                            <span class="text-xs font-medium mr-2">Materi:</span>
                            <span 
                              :class="[
                                'px-2 py-1 text-xs font-medium rounded-full',
                                guru.crud_materi 
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                              ]"
                            >
                              {{ guru.crud_materi ? 'Diizinkan' : 'Tidak Diizinkan' }}
                            </span>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap flex items-center justify-start space-x-2">
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="editGuru(guru)"
                            >
                              <PencilIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Edit Guru
                          </template>
                        </fwb-tooltip>
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="deleteGuru(guru.id)"
                            >
                              <TrashIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Hapus Guru
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
                      <SkeletonLoader width="120px" />
                    </div>
                  </div>
                </template>
                
                <template v-else>
                  <div v-for="guru in filteredGuru" :key="guru.id" 
                       class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow cursor-pointer"
                       @click="showGuruDetail(guru)">
                    <div class="space-y-2">
                      <div class="font-medium">{{ guru.username }}</div>
                      <div class="font-medium">{{ guru.nama_guru }}</div>
                      <div class="text-sm text-gray-500">
                        Mata Pelajaran: {{ guru.nama_mata_pelajaran_detail?.nama_mata_pelajaran || '-' }}
                      </div>
                      <div class="flex space-x-2 pt-2">
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="editGuru(guru)"
                            >
                              <PencilIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Edit Guru
                          </template>
                        </fwb-tooltip>
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark" 
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click.stop="deleteGuru(guru.id)"
                            >
                              <TrashIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Hapus Guru
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
              {{ selectedGuru ? 'Edit Guru' : 'Tambah Guru' }}
            </div>
          </template>
          <template #body>
            <GuruForm 
              :guru="selectedGuru"
              @submit="saveGuru"
              @cancel="closeModal"
            />
          </template>
        </BaseModal>

        <!-- Modal konfirmasi hapus -->
        <BaseModal v-model="showDeleteModal">
          <template #header>
            <div class="flex items-center">
              Konfirmasi Hapus
            </div>
          </template>
          <template #body>
            <p v-if="guruToDelete">
              Apakah Anda yakin ingin menghapus guru ini?
            </p>
            <p v-else>
              Apakah Anda yakin ingin menghapus {{ selectedGuruIds.length }} guru yang dipilih?
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

        <!-- Modal detail guru -->
        <BaseModal v-model="showDetailModal">
          <template #header>
            <div class="flex items-center">
              Detail Guru
            </div>
          </template>
          <template #body>
            <div v-if="selectedGuruDetail" class="space-y-4">
              <div class="flex flex-wrap justify-center gap-4">
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Username:</div>
                  <div class="w-1/2 break-words">{{ selectedGuruDetail.username }}</div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Nama Guru:</div>
                  <div class="w-1/2 break-words">{{ selectedGuruDetail.nama_guru }}</div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Mata Pelajaran:</div>
                  <div class="w-1/2 break-words">{{ selectedGuruDetail.nama_mata_pelajaran_detail?.nama_mata_pelajaran || '-' }}</div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Kelas:</div>
                  <div class="w-1/2 break-words">
                    {{ selectedGuruDetail.kelas_detail?.map(k => k.nama_kelas).join(', ') || '-' }}
                  </div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Jenjang:</div>
                  <div class="w-1/2 break-words">{{ selectedGuruDetail.jenjang_detail?.nama_jenjang || '-' }}</div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Sekolah:</div>
                  <div class="w-1/2 break-words">{{ selectedGuruDetail.sekolah_detail?.nama_sekolah || '-' }}</div>
                </div>
                <div class="w-full flex">
                  <div class="w-1/2 font-medium">Akses CRUD:</div>
                  <div class="w-1/2 break-words">
                    <div class="flex flex-col gap-2">
                      <!-- Badge untuk CRUD Buku -->
                      <div class="inline-flex items-center">
                        <span class="text-xs font-medium mr-2">Buku:</span>
                        <span 
                          :class="[
                            'px-2 py-1 text-xs font-medium rounded-full',
                            selectedGuruDetail.crud_buku 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                          ]"
                        >
                          {{ selectedGuruDetail.crud_buku ? 'Diizinkan' : 'Tidak Diizinkan' }}
                        </span>
                      </div>

                      <!-- Badge untuk CRUD Materi -->
                      <div class="inline-flex items-center">
                        <span class="text-xs font-medium mr-2">Materi:</span>
                        <span 
                          :class="[
                            'px-2 py-1 text-xs font-medium rounded-full',
                            selectedGuruDetail.crud_materi 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                          ]"
                        >
                          {{ selectedGuruDetail.crud_materi ? 'Diizinkan' : 'Tidak Diizinkan' }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </BaseModal>

        <!-- Bagian bawah table (Jumlah Guru, Pagination) -->
        <div class="mt-4 flex justify-between gap-2">
            <div class="relative flex items-center gap-2 mt-4">
              <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
                Jumlah Guru: {{ filteredGuru.length }}
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

        <!-- Bagian bawah table (Hapus Guru Terpilih) -->
        <div class="flex flex-wrap gap-2 mb-6">
          <fwb-tooltip v-if="selectedGuruIds.length > 0">
            <template #trigger>
                <FwbButton
                color="dark"
                class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
                @click="bulkDelete"
              >
                <div class="flex flex-row gap-2 items-center justify-center p-1">
                  <TrashIcon class="w-5 h-5" />
                  <span>({{ selectedGuruIds.length }})</span>
                </div>
                
              </FwbButton>
            </template>
            <template #content>
              Hapus Guru Terpilih
            </template>
          </fwb-tooltip>
        </div>

    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/config/api'
import GuruForm from '@/components/form/GuruForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import { useNotifications } from '@/composables/useNotifications'
import Notifications from '@/components/Notifications.vue'

const loading = ref(true)
const guruList = ref([])
const showAddModal = ref(false)
const selectedGuru = ref(null)
const showDeleteModal = ref(false)
const guruToDelete = ref(null)
const showDetailModal = ref(false)
const selectedGuruDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedFilters = ref({
  mapel: [],
  kelas: [],
  jenjang: [],
  sekolah: []
})

const itemsPerPage = 3
const currentPage = ref(1)

const paginatedGuru = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredGuru.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredGuru.value.length / itemsPerPage)
})

const mapelList = ref([])
const kelasList = ref([])
const jenjangList = ref([])
const sekolahList = ref([])

const fetchMapel = async () => {
  try {
    const response = await api.get('/mata-pelajaran/')
    mapelList.value = response.data
  } catch (error) {
    console.error('Error fetching mapel:', error)
  }
}

const filteredGuru = computed(() => {
  let result = guruList.value

  if (selectedFilters.value.mapel?.length) {
    result = result.filter(guru => 
      selectedFilters.value.mapel.includes(guru.nama_mata_pelajaran)
    )
  }

  if (selectedFilters.value.kelas?.length) {
    result = result.filter(guru => 
      selectedFilters.value.kelas.includes(guru.kelas)
    )
  }

  if (selectedFilters.value.jenjang?.length) {
    result = result.filter(guru => 
      selectedFilters.value.jenjang.includes(guru.jenjang)
    )
  }

  if (selectedFilters.value.sekolah?.length) {
    result = result.filter(guru => 
      selectedFilters.value.sekolah.includes(guru.sekolah)
    )
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(guru =>
      guru.nama_guru?.toLowerCase().includes(query) ||
      guru.username?.toLowerCase().includes(query)
    )
  }

  return result
})

// Inisialisasi notifications
const { notify } = useNotifications()

const fetchGuru = async () => {
  try {
    const response = await api.get('/guru/')
    guruList.value = response.data.map(guru => ({
      ...guru,
      username: guru.user_detail?.username || 'User tidak ditemukan'
    }))
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data guru'
    })
    console.error('Error fetching guru:', error)
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedGuru.value = null
  showAddModal.value = true
}

const editGuru = (guru) => {
  selectedGuru.value = { ...guru }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedGuru.value = null
}

const saveGuru = async (guruData) => {
  try {
    if (selectedGuru.value) {
      await api.put(`/guru/${selectedGuru.value.id}/`, guruData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Data guru berhasil diperbarui'
      })
    } else {
      const response = await api.post('/guru/', guruData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Guru baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchGuru()
  } catch (error) {
    const errorMessage = error.response?.data?.error || 
                        error.response?.data?.detail || 
                        'Terjadi kesalahan saat menyimpan data guru'
    notify({
      type: 'error',
      title: 'Gagal',
      message: errorMessage
    })
    console.error('Error saving guru:', error)
  }
}

const deleteGuru = async (guruId) => {
  guruToDelete.value = guruId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    if (guruToDelete.value) {
      // Single delete
      await api.delete(`/guru/${guruToDelete.value}/`)
    } else {
      // Bulk delete
      await api.post('/guru/bulk-delete/', {
        ids: selectedGuruIds.value
      })
      selectedGuruIds.value = []
    }
    
    notify({
      type: 'success',
      title: 'Berhasil',
      message: 'Guru berhasil dihapus'
    })
    showDeleteModal.value = false
    guruToDelete.value = null
    fetchGuru()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus guru'
    })
  }
}

const showGuruDetail = (guru) => {
  selectedGuruDetail.value = guru
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

const activeFiltersCount = computed(() => {
  let count = 0
  count += selectedFilters.value.mapel.length
  count += selectedFilters.value.kelas.length
  count += selectedFilters.value.jenjang.length
  count += selectedFilters.value.sekolah.length
  return count
})

const resetFilters = () => {
  selectedFilters.value = {
    mapel: [],
    kelas: [],
    jenjang: [],
    sekolah: []
  }
}

const selectedGuruIds = ref([])

const selectAll = ref(false)

const toggleSelectAll = () => {
  if (selectAll.value) {
    // Pilih semua guru yang ada di halaman saat ini
    selectedGuruIds.value = filteredGuru.value.map(guru => guru.id)
  } else {
    // Kosongkan pilihan
    selectedGuruIds.value = []
  }
}

// Tambahkan watch untuk mengupdate selectAll berdasarkan selectedGuruIds
watch(selectedGuruIds, (newValue) => {
  // Cek apakah semua guru di halaman saat ini terpilih
  const allSelected = filteredGuru.value.every(guru => 
    newValue.includes(guru.id)
  )
  selectAll.value = allSelected
})

onMounted(() => {
  fetchGuru()
  fetchFilterData()
})

const bulkDelete = async () => {
  try {
    if (selectedGuruIds.value.length === 0) return
    
    showDeleteModal.value = true
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Terjadi kesalahan saat menghapus guru'
    })
  }
}

const notificationsRef = ref(null)
</script>
