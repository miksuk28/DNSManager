<template>
  <main class="container">
    <ServicesTable :services="this.services" />
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