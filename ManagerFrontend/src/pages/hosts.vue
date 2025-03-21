<template>
  <v-main class="d-flex flex-row">
    <v-tabs v-model="this.tab" direction="vertical">
      <v-tab prepend-icon="mdi-server"  text="Hosts"    value="hostList"></v-tab>
      <v-tab prepend-icon="mdi-web"     text="Services" values="servicesList"></v-tab>
    </v-tabs>
    <v-container>
      <v-tabs-window v-model="this.tab">

        <v-tabs-window-item value="hostList">
          <v-data-table :items="this.hosts" :headers="this.hostTableHeaders" >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>
                  <v-icon color="medium-emphasis" icon="mdi-server" size="x-small" start></v-icon>
                  Hosts
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn
                  class="me-2"
                  prepend-icon="mdi-plus"
                  rounded="lg"
                  text="Add Host"
                  border
                  @click="this.tab = 'addHost'"
                ></v-btn>
              </v-toolbar>
            </template>
          </v-data-table>
        </v-tabs-window-item>
        
        <v-tabs-window-item value="servicesList">
          <v-data-table :items="this.services" :headers="this.servicesTableHeaders">
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>
                  <v-icon color="medium-emphasis" icon="mdi-web" size="x-small" start></v-icon>
                  Services
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn
                  class="me-2"
                  prepend-icon="mdi-plus"
                  rounded="lg"
                  text="Add Service"
                  border
                  @click="this.tab = 'addService'"
                ></v-btn>
              </v-toolbar>
            </template>
          </v-data-table>
        </v-tabs-window-item>
        
        <v-tabs-window-item value="addHost" variant="tonal">
          <AddHostForm @hostCreated="this.getHosts(); this.tab = 'hostList'" :domains="this.domainsList"/>
        </v-tabs-window-item>

        <v-tabs-window-item value="addService" variant="tonal">
          <AddServiceForm :domains="this.domainsList" />
        </v-tabs-window-item>

        <v-tabs-window-item value="hostDetails">
          awdawda
        </v-tabs-window-item>

      </v-tabs-window>
    </v-container>
  </v-main>
</template>

<script>
  import AddHostForm from '@/components/AddHostForm.vue';
  import AddServiceForm from '@/components/AddServiceForm.vue';

  export default {
    components: { AddHostForm, AddServiceForm },
    data() {
      return {
        tab: null,
        hosts: [],
        services: [],
        domains: [],
        dhcpScopes: [],
        newHost: {
          useNextAvailableAddress: true
        },
        hostTableHeaders: [
          { title: "Hostname",    value: "hostname"},
          { title: "MAC Address", value: "macAddress"},
          { title: "IP Address",  value: "ipAddress"},
          { title: "DHCP Scope",  value: "dhcpScopeName"}
        ],
        servicesTableHeaders: [
          { title: "FQDN", value: "domainName"},
          { title: "Target Host", value: "target"}
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
      },
      async getServices() {
        const response = await fetch("/api/services/list")
        this.services = await response.json()
      },
      async getDomains() {
        const response = await fetch("/api/domains/list")
        this.domains = await response.json()
      }
    },
    mounted() {
      this.getHosts()
      this.getServices()
      this.getDomains()
    },
    computed: {
      domainsList() {
        return this.reduceObjectToArray(this.domains, "domainName")
      }
    }
  }
</script>