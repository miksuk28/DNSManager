<template>
  <v-main>
    <v-container>
      <v-data-table :items="this.services" :headers="this.tableHeaders" ></v-data-table>
    </v-container>
  </v-main>
</template>

<script>
  export default {
    data() {
      return {
        services: [],
        tableHeaders: [
          { title: "FQDN", value: "domainName"},
          { title: "Target Host", value: "target"}
        ]
      }
    },
    methods: {
      async getServices() {
        const response = await fetch("/api/services/list")
        this.services = await response.json()

        console.log(this.services)
      }
    },
    mounted() {
      this.getServices()
    }
  }
</script>