<template>
  <main class="container">
    <AddDomainModal 
      :open="this.showAddDomainModal"
      @updateDomains="this.getDomains()"
      @closeModal="this.showAddDomainModal=false"
    />
    <DomainsTable :domains="this.domains" />

    <div class="grid">
      <button @click="this.showAddDomainModal=true" class="outline">Add Domain</button>
    </div>
  </main>
</template>

<script>
  import DomainsTable from '@/components/DomainsTable.vue';
  import AddDomainModal from '@/components/AddDomainModal.vue';

  export default {
    components: { DomainsTable, AddDomainModal },
    data() {
      return {
        domains: [],
        showAddDomainModal: false
      }
    },
    methods: {
      async getDomains() {
        const response = await fetch("/api/domains/list")
        this.domains = await response.json()
      }
    },
    mounted() {
      this.getDomains()
    }
  }
</script>