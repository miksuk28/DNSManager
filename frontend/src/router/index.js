import { createRouter, createWebHistory } from 'vue-router'
import HostsView from '@/views/HostsView.vue'
import ServicesView from '@/views/ServicesView.vue'
import HostDetailsView from '@/views/HostDetailsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: "/services",
    },
    {
      path: "/hosts",
      name: "host",
      component: HostsView
    },
    {
      path: "/services",
      name: "services",
      component: ServicesView
    },
    {
      path: "/hosts/:hostId",
      name: "hostdetails",
      component: HostDetailsView
    }
  ],
})

export default router
