<template>
  <main class="container">
    <h3>Domains</h3>
    <hr>
    <!--YesNo prompt for domain deletion-->
    <AddDomainModal 
      :open="this.showAddDomainModal"
      @updateDomains="this.getDomains()"
      @closeModal="this.showAddDomainModal=false"
    />
    <h4 v-show="this.domains.length === 0">No Domains Defined</h4>
      <DomainsTable v-show="this.domains.length !== 0" :domains="this.domains" @getDomains="this.getDomains()" />

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
      },
      createErrorModal(error, exception, status) {
        this.error.response = error
        this.error.exception = exception
        this.error.status = status
        this.error.showModal = true
      },
      openDeleteDomainModal() {
        this.showDeleteDomainModal = true
      },
      deleteDomainById(domainId) {
        const requestOptions = {
          method: "POST"
        }

        fetch(`/api/domains/${domainId}`, requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in domain deletion")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.getDomains()
            }
          })
      }
    },
    mounted() {
      this.getDomains()
    }
  }
</script>