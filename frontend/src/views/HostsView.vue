<template>
  <main class="container">
    <h3>Hosts</h3>
    <hr>
    <AddHostModal @closeModal="this.closeAddHostModal()" @updateHosts="getHosts()" :open="this.showAddHostModal" />
    
    <HostsTable v-show="this.hosts.length !== 0" class="overflow-auto" :hosts="this.hosts"/>
    <h4 v-show="this.hosts.length === 0">No Hosts Defined</h4>
    <div class="grid">
      <button @click="openAddHostModal" class="outline">Add host</button>
    </div>
  </main>
</template>


<script>
  import HostsTable from '@/components/HostsTable.vue';
  import AddHostModal from "@/components/AddHostModal.vue"
  //import AddSericeModal from "@/components/AddServiceModal.vue"

  export default {
    components: {
      HostsTable,
      AddHostModal
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