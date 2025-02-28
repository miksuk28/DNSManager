<template>
  <main class="container">
    <!--<AddSericeModal :hostId="this.newServiceModalHostId" :open="showAddServiceModal" />-->

    <AddHostModal @closeModal="this.closeAddHostModal()" @updateHosts="getHosts()" :open="this.showAddHostModal" />

    <HostsTable @addServiceModal="openAddServiceModal" class="overflow-auto" :hosts="this.hosts"/>
    <div class="grid">
      <button @click="openAddHostModal" class="outline">Add host</button>
    </div>
  </main>
</template>


<script>
  import HostsTable from '@/components/HostsTable.vue';
  import AddHostModal from "@/components/AddHostModal.vue"
  import AddSericeModal from "@/components/AddServiceModal.vue"

  export default {
    components: {
      HostsTable,
      AddHostModal,
      AddSericeModal
    },

    data() {
      return {
        hosts: [],
        showAddHostModal: false,
        showAddServiceModal: false,
        newServiceModalHostId: null
      }
    },
    
    methods: {
      async getHosts() {
        const response = await fetch("/api/hosts/list")
        this.hosts = await response.json()
      },

      openAddHostModal() {
        this.showAddHostModal = true
      },
      closeAddHostModal() {
        this.showAddHostModal = false
      },
      openAddServiceModal(hostId) {
        console.log(`IN HSOT VIEW FUNC: ${hostId}`)
        this.newServiceModalHostId = hostId
        this.showAddServiceModal = true
      }
    },

    mounted() {
      this.getHosts()
    }
  }
</script>