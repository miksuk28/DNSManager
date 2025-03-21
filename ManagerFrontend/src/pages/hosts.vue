<template>
  <v-main class="d-flex flex-row">
    <v-tabs v-model="this.tab" direction="vertical">
      <v-tab prepend-icon="mdi-server" text="List hosts" value="hostList"></v-tab>
      <v-tab prepend-icon="mdi-plus" text="Add host" value="addHost"></v-tab>
    </v-tabs>
    <v-container>
      <v-tabs-window v-model="this.tab">

        <v-tabs-window-item value="hostList">
          <v-data-table :items="this.hosts" :headers="this.tableHeaders" ></v-data-table>
        </v-tabs-window-item>

        <v-tabs-window-item value="addHost" variant="tonal" text="Enter host information">
          <AddHostForm />
        </v-tabs-window-item>

      </v-tabs-window>
    </v-container>
  </v-main>
</template>

<script>
  import AddHostForm from '@/components/AddHostForm.vue';

  export default {
    components: { AddHostForm },
    data() {
      return {
        tab: null,
        hosts: [],
        domains: [],
        dhcpScopes: [],
        newHost: {
          useNextAvailableAddress: true
        },
        tableHeaders: [
          { title: "Hostname",    value: "hostname"},
          { title: "MAC Address", value: "macAddress"},
          { title: "IP Address",  value: "ipAddress"},
          { title: "DHCP Scope",  value: "dhcpScopeName"}
        ]
      }
    },
    methods: {
      reduceObjectToArray(obj, key) {
        return Object.values(obj).map(item => item[key]);
      },
      async getHosts() {
        const response = await fetch("/api/hosts/list")
        this.hosts = await response.json()

        console.log(this.hosts)
      }
    },
    mounted() {
      this.getHosts()
    }
  }
</script>