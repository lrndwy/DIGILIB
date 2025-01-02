<template>
  <TransitionWrapper>
    <div class="p-8 w-full">
      <!-- Konten utama dengan transisi -->
      <Transition
        name="slide"
        mode="out-in"
      >
        <div :key="type" class="space-y-6">
          <!-- Title -->
          <h1 class="text-2xl sm:text-3xl font-bold text-text-light-primary dark:text-text-dark-primary">
            {{ pageTitle }}
          </h1>

          <!-- Search dan Tambah -->
          <div class="flex flex-wrap items-center gap-2">
            <!-- Search -->
            <div class="flex-1">
              <input
                type="text"
                v-model="searchQuery"
                :placeholder="`Cari ${singularTitle.toLowerCase()}...`"
                class="w-full px-4 py-2 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
              />
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
                Tambah {{ singularTitle }}
              </template>
            </fwb-tooltip>
          </div>

          <!-- Table -->
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
                    <th 
                      v-for="header in headers" 
                      :key="header.value"
                      class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider"
                    >
                      {{ header.text }}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                      Aksi
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-background-dark divide-y divide-gray-200 dark:divide-border-dark">
                  <template v-if="loading">
                    <tr v-for="n in 5" :key="n" class="hover:bg-gray-50 dark:hover:bg-surface-dark">
                      <td v-for="header in headers" :key="header.value" class="px-6 py-4 whitespace-nowrap">
                        <SkeletonLoader width="150px" />
                      </td>
                    </tr>
                  </template>
                  <template v-else>
                    <tr v-for="item in paginatedItems" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-surface-dark">
                      <td class="px-6 py-4">
                        <Checkbox
                          v-model="selectedIds"
                          :value="item.id"
                        />
                      </td>
                      <td v-for="header in headers" :key="header.value" class="px-6 py-4 whitespace-nowrap">
                        <template v-if="header.value === 'logo_sekolah' && type === 'sekolah'">
                          <img
                            v-if="item.logo_sekolah"
                            :src="item.logo_sekolah"
                            class="w-12 h-12 object-contain"
                            alt="Logo Sekolah"
                          />
                          <span v-else>-</span>
                        </template>
                        <template v-else-if="header.value === 'jenjang_detail.nama_jenjang'">
                          {{ item.jenjang_detail?.nama_jenjang || '-' }}
                        </template>
                        <template v-else>
                          {{ item[header.value] }}
                        </template>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click="editItem(item)"
                            >
                              <PencilIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Edit {{ singularTitle }}
                          </template>
                        </fwb-tooltip>
                        <fwb-tooltip>
                          <template #trigger>
                            <FwbButton
                              color="dark"
                              class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                              @click="deleteItem(item.id)"
                            >
                              <TrashIcon class="w-4 h-4" />
                            </FwbButton>
                          </template>
                          <template #content>
                            Hapus {{ singularTitle }}
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
                      <SkeletonLoader width="150px" />
                      <SkeletonLoader width="100px" />
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div v-for="item in paginatedItems" :key="item.id" 
                       class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                    <div class="space-y-2">

                      <div v-for="header in headers" :key="header.value">
                        <div class="font-medium">{{ header.text }}</div>
                        <div>
                          <template v-if="header.value === 'logo_sekolah' && type === 'sekolah'">
                            <span v-if="!item.logo_sekolah">-</span>
                            <img
                              v-if="item.logo_sekolah"
                              :src="item.logo_sekolah"
                              class="w-24 h-24 object-contain"
                              alt="Logo Sekolah"
                            />
                          </template>
                          <template v-else>
                            {{ item[header.value] }}
                          </template>
                        </div>
                      </div>
                      <div class="flex justify-start space-x-2 mt-4">
                        <FwbButton
                          color="dark"
                          class="p-2"
                          @click="editItem(item)"
                        >
                          <PencilIcon class="w-4 h-4" />
                        </FwbButton>
                        <FwbButton
                          color="dark"
                          class="p-2"
                          @click="deleteItem(item.id)"
                        >
                          <TrashIcon class="w-4 h-4" />
                        </FwbButton>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div class="flex justify-between gap-2">
            <div class="relative flex items-center gap-2">
              <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
                Jumlah {{ singularTitle }}: {{ filteredItems.length }}
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
          <div class="flex flex-wrap gap-2" v-if="selectedIds.length > 0">
            <fwb-tooltip>
              <template #trigger>
                <FwbButton
                  color="dark"
                  class="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white"
                  @click="bulkDelete"
                >
                  <div class="flex flex-row gap-2 items-center justify-center p-1">
                    <TrashIcon class="w-5 h-5" />
                    <span>({{ selectedIds.length }})</span>
                  </div>
                </FwbButton>
              </template>
              <template #content>
                Hapus {{ singularTitle }} Terpilih
              </template>
            </fwb-tooltip>
          </div>
        </div>
      </Transition>

      <!-- Modals -->
      <BaseModal v-model="showAddModal">
        <template #header>
          <div class="flex items-center">
            {{ formTitle }}
          </div>
        </template>
        <template #body>
          <AtributForm 
            :type="type"
            :initial-data="selectedItem"
            @submit="saveItem"
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
          <p>Apakah Anda yakin ingin menghapus {{ itemToDelete ? singularTitle : `${selectedIds.length} ${singularTitle}` }} ini?</p>

        </template>
        <template #footer>
          <div class="flex justify-end gap-2 mt-4">
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
          </div>
        </template>
      </BaseModal>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNotifications } from '@/composables/useNotifications'
import api from '@/config/api'
import AtributForm from '@/components/form/AtributForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import Checkbox from '@/components/Checkbox.vue'

const route = useRoute()
const router = useRouter()
const { notify } = useNotifications()

// State
const type = ref('')
const items = ref([])
const loading = ref(false)
const showAddModal = ref(false)
const selectedItem = ref(null)
const showDeleteModal = ref(false)
const itemToDelete = ref(null)
const searchQuery = ref('')
const selectedIds = ref([])
const selectAll = ref(false)
const itemsPerPage = 5
const currentPage = ref(1)

// Computed
const pageTitle = computed(() => {
  const titles = {
    sekolah: 'Daftar Sekolah',
    jenjang: 'Daftar Jenjang',
    kelas: 'Daftar Kelas',
    mata_pelajaran: 'Daftar Mata Pelajaran'
  }
  return titles[type.value] || ''
})

const singularTitle = computed(() => {
  const titles = {
    sekolah: 'Sekolah',
    jenjang: 'Jenjang',
    kelas: 'Kelas',
    mata_pelajaran: 'Mata Pelajaran'
  }
  return titles[type.value] || ''
})

const formTitle = computed(() => {
  return selectedItem.value ? `Edit ${singularTitle.value}` : `Tambah ${singularTitle.value}`
})

const headers = computed(() => {
  const headerMap = {
    sekolah: [
      { text: 'Nama Sekolah', value: 'nama_sekolah' },
      { text: 'Logo', value: 'logo_sekolah' }
    ],
    jenjang: [
      { text: 'Nama Jenjang', value: 'nama_jenjang' }
    ],
    kelas: [
      { text: 'Nama Kelas', value: 'nama_kelas' },
      { text: 'Jenjang', value: 'jenjang_detail.nama_jenjang' }
    ],
    mata_pelajaran: [
      { text: 'Nama Mata Pelajaran', value: 'nama_mata_pelajaran' }
    ]
  }
  return headerMap[type.value] || []
})

const filteredItems = computed(() => {
  if (!searchQuery.value) return items.value
  
  const query = searchQuery.value.toLowerCase()
  return items.value.filter(item => {
    const searchFields = {
      sekolah: ['nama_sekolah'],
      jenjang: ['nama_jenjang'],
      kelas: ['nama_kelas'],
      mata_pelajaran: ['nama_mata_pelajaran']
    }
    
    return searchFields[type.value].some(field => 
      item[field]?.toLowerCase().includes(query)
    )
  })
})

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredItems.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / itemsPerPage)
})

// Methods
const fetchItems = async () => {
  loading.value = true
  try {
    let endpoint = ''
    switch (type.value) {
      case 'mata_pelajaran':
        endpoint = 'mata-pelajaran'
        break
      case 'kelas':
        endpoint = 'kelas'
        break
      case 'jenjang':
        endpoint = 'jenjang'
        break
      case 'sekolah':
        endpoint = 'sekolah'
        break
      default:
        throw new Error('Tipe atribut tidak valid')
    }
    
    const response = await api.get(`/${endpoint}/`)
    items.value = response.data
  } catch (error) {
    console.error('Error fetching items:', error)
    notify({
      type: 'error',
      title: 'Gagal',
      message: `Gagal mengambil data ${singularTitle.value.toLowerCase()}`
    })
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedItem.value = null
  showAddModal.value = true
}

const editItem = (item) => {
  selectedItem.value = { ...item }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedItem.value = null
}

const saveItem = async (formData) => {
  try {
    let endpoint = ''
    switch (type.value) {
      case 'mata_pelajaran':
        endpoint = 'mata-pelajaran'
        break
      case 'kelas':
        endpoint = 'kelas'
        break
      case 'jenjang':
        endpoint = 'jenjang'
        break
      case 'sekolah':
        endpoint = 'sekolah'
        break
      default:
        throw new Error('Tipe atribut tidak valid')
    }

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }

    if (selectedItem.value) {
      await api.put(`/${endpoint}/${selectedItem.value.id}/`, formData, config)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: `${singularTitle.value} berhasil diperbarui`
      })
    } else {
      await api.post(`/${endpoint}/`, formData, config)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: `${singularTitle.value} berhasil ditambahkan`
      })
    }
    closeModal()
    fetchItems()
  } catch (error) {
    console.error('Error detail:', error.response?.data)
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || `Gagal menyimpan ${singularTitle.value.toLowerCase()}`
    })
  }
}

const deleteItem = (id) => {
  itemToDelete.value = id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    let endpoint = ''
    switch (type.value) {
      case 'mata_pelajaran':
        endpoint = 'mata-pelajaran'
        break
      case 'kelas':
        endpoint = 'kelas'
        break
      case 'jenjang':
        endpoint = 'jenjang'
        break
      case 'sekolah':
        endpoint = 'sekolah'
        break
      default:
        throw new Error('Tipe atribut tidak valid')
    }

    if (itemToDelete.value) {
      await api.delete(`/${endpoint}/${itemToDelete.value}/`)
    } else {
      await api.post(`/${endpoint}/bulk-delete/`, {
        ids: selectedIds.value
      })
      selectedIds.value = []
    }
    
    notify({
      type: 'success',
      title: 'Berhasil',
      message: `${singularTitle.value} berhasil dihapus`
    })
    showDeleteModal.value = false
    itemToDelete.value = null
    fetchItems()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal', 
      message: error.response?.data?.message || `Gagal menghapus ${singularTitle.value.toLowerCase()}`
    })
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedIds.value = items.value.map(item => item.id)
  } else {
    selectedIds.value = []
  }
}

const bulkDelete = () => {
  showDeleteModal.value = true
  itemToDelete.value = null
}

// Watchers
watch(() => route.params.type, (newType) => {
  type.value = newType
  if (['sekolah', 'jenjang', 'kelas', 'mata_pelajaran'].includes(newType)) {
    fetchItems()
  } else {
    router.push('/dashboard/admin')
  }
}, { immediate: true })

watch(selectedIds, (newValue) => {
  selectAll.value = items.value.length > 0 && newValue.length === items.value.length
})

watch([searchQuery, type], () => {
  currentPage.value = 1
})
</script> 

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style> 
