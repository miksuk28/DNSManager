<template>
  <main class="container">
    <h4 v-show="this.services.length === 0">No Services Defined</h4>
    <ServicesTable v-show="this.services.length !== 0" :services="this.services" />
  </main>
</template>

<script>
  import ServicesTable from '@/components/ServicesTable.vue';

  export default {
    components: { ServicesTable },
    data() {
      return {
        services: []
      }
    },

    methods: {
      async getServices() {
        const response = await fetch("/api/services/list")
        this.services = await response.json()
      }
    },
    mounted() {
      this.getServices()
    }
  }
</script>