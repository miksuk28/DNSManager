import { createRouter, createWebHistory } from 'vue-router'
import HostsView from '@/views/HostsView.vue'
import ServicesView from '@/views/ServicesView.vue'
import HostDetailsView from '@/views/HostDetailsView.vue'
import DomainsView from '@/views/DomainsView.vue'
import AliasesView from '@/views/AliasesView.vue'

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
    },
    {
      path: "/domains",
      name: "domainsview",
      component: DomainsView
    },
    {
      path: "/aliases",
      name: "aliasesview",
      component: AliasesView
    }
  ],
})

export default router
