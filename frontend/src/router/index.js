import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import AdminDashboard from '@/views/dashboard/admin/Dashboard.vue'
import GuruDashboard from '@/views/dashboard/guru/Dashboard.vue'
import SiswaDashboard from '@/views/dashboard/siswa/Dashboard.vue'
import AdminDashboard_Users from '@/views/dashboard/admin/Users.vue'
import AdminDashboard_Guru from '@/views/dashboard/admin/Guru.vue'
import AdminDashboard_Siswa from '@/views/dashboard/admin/Siswa.vue'
import Profile from '@/views/profile/Profile.vue'
import AdminDashboard_Materi from '@/views/dashboard/admin/Materi.vue'
import LandingPage from '@/views/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/admin/users',
    name: 'AdminDashboard_Users',
    component: AdminDashboard_Users,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/guru',
    name: 'GuruDashboard',
    component: GuruDashboard,
    meta: { requiresAuth: true, role: 'guru' }
  },
  {
    path: '/dashboard/guru/buku',
    name: 'GuruDashboard_Buku',
    component: () => import('@/views/dashboard/guru/BukuGuru.vue'),
    meta: { requiresAuth: true, role: 'guru' }
  },
  {
    path: '/dashboard/siswa',
    name: 'SiswaDashboard',
    component: SiswaDashboard,
    meta: { requiresAuth: true, role: 'siswa' }
  },
  {
    path: '/dashboard/admin/guru',
    name: 'AdminDashboard_Guru',
    component: AdminDashboard_Guru,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/admin/siswa',
    name: 'AdminDashboard_Siswa',
    component: AdminDashboard_Siswa,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/admin/atribut/:type',
    name: 'Atribut',
    component: () => import('@/views/dashboard/admin/Atribut.vue'),
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/dashboard/admin/buku',
    name: 'AdminDashboard_Buku',
    component: () => import('@/views/dashboard/admin/Buku.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/buku/:bookId/:title',
    name: 'BukuViewer',
    component: () => import('@/components/BukuViewer.vue')
  },
  {
    path: '/dashboard/admin/perangkat-kurikulum',
    name: 'AdminDashboard_PerangkatKurikulum',
    component: () => import('@/views/dashboard/admin/PerangkatKurikulum.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/perangkat/:perangkatId/:title',
    name: 'PerangkatViewer',
    component: () => import('@/components/PerangkatViewer.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/admin/materi',
    name: 'AdminDashboard_Materi',
    component: () => import('@/views/dashboard/admin/Materi.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/materi/:materiId/:title',
    name: 'MateriViewer',
    component: () => import('@/components/MateriViewer.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/guru/materi',
    name: 'MateriGuru',
    component: () => import('@/views/dashboard/guru/MateriGuru.vue'),
    meta: {
      requiresAuth: true,
      allowedRoles: ['guru']
    }
  },
  {
    path: '/dashboard/guru/perangkat-kurikulum',
    name: 'PerangkatKurikulumGuru',
    component: () => import('@/views/dashboard/guru/PerangkatKurikulumGuru.vue'),
    meta: {
      requiresAuth: true,
      allowedRoles: ['guru']
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  // Izinkan akses ke landing page tanpa batasan
  if (to.name === 'LandingPage') {
    next()
    return
  }

  // Redirect dari login page jika sudah terotentikasi
  if (to.path === '/login' && token) {
    next('/dashboard/' + userRole)
    return
  }

  // Cek authentication untuk protected routes
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    next('/dashboard/' + userRole)
  } else {
    next()
  }
})

export default router
