<template>
  <v-main class="d-flex flex-row">
    <v-tabs v-model="this.tab" >
      <v-tab prepend-icon="mdi-web" text="List services" value="servicesList"></v-tab>
      <v-tab prepend-icon="mdi-plus" text="Add Service" value="addService"></v-tab>
    </v-tabs>
    
    
    <v-container>
      <v-tabs-window v-model="this.tab">

        <v-tabs-window-item value="servicesList">
          <v-data-table :items="this.services" :headers="this.tableHeaders" ></v-data-table>
        </v-tabs-window-item>

        <v-tabs-window-item value="addService">
          <AddServiceForm />
        </v-tabs-window-item>

      </v-tabs-window>
    </v-container>
  </v-main>
</template>

<script>
  import AddServiceForm from '@/components/AddServiceForm.vue'

  export default {
    components: { AddServiceForm },
    data() {
      return {
        tab: null,
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