import type { RouteRecordRaw } from 'vue-router'
import HomeView from '@/pages/HomeView.vue'

const NotFind = () => import('@/pages/404/index.vue')

const routes: RouteRecordRaw[] = [
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFind },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../../pages/AboutView.vue')
  }
]

export default routes
