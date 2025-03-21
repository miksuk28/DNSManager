<template>
  <v-container>
    <h1>{{ host.hostname }}</h1>
  </v-container>
  
  <v-container>
    <div>
      <v-toolbar flat>
        <v-toolbar-title>
          <v-icon color="medium-emphasis" icon="mdi-information" size="x-small" start></v-icon>
          Host Information
          
        </v-toolbar-title>
        <v-btn
          class="me-2"
          prepend-icon="mdi-delete"
          rounded="lg"
          text="Remove Host"
          border
          @click="console.log('Nothing yet')"
        ></v-btn>
      </v-toolbar>
      <v-table>
        <thead>
          <tr>
            <th><strong>Hostname</strong></th>
            <th>{{ this.host.hostname }}</th>
          </tr>
          <tr>
            <th><strong>DHCP Scope</strong></th>
            <th>{{ this.host.dhcpScopeName }}</th>
          </tr>
          <tr>
            <th><strong>IP Address</strong></th>
            <th>{{ this.host.ipAddress }}</th>
          </tr>
          <tr>
            <td><strong>MAC Address</strong></td>
            <td>{{ this.host.macAddress }}</td>
          </tr>
        </thead>
      </v-table>
    </div>
  </v-container>

  <v-container>
    <v-data-table :items="services" :headers="this.servicesTableHeaders" >
      <template v-slot:no-data>
        <p>No services pointing to host</p>
      </template>
      
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>
            <v-icon color="medium-emphasis" icon="mdi-web" size="x-small" start></v-icon>
            Services on host
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

  </v-container>
</template>

<script>
  export default {
    props: ["host", "services"],
    data() {
      return {
        servicesTableHeaders: [
          { title: "Service Address", value: "domainName" },
          { title: "Description",     value: "description"}
        ]
      }
    },
    methods: {

    }
  }
</script>