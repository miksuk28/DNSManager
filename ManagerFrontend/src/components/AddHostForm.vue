<template>
  <ErrorDialog
    :error="this.error"
    v-model="this.error.showDialog"
    @close="this.error.showDialog = false"
  />

  <v-card title="New Host">
  <v-card-text>
    <v-sheet class="">
      <v-form @submit.prevent>
        <v-text-field v-model="newHost.hostname" label="Short Hostname"></v-text-field>                
        <v-select v-model="newHost.domain" label="Domain" :items="this.domains"></v-select>
        
        <v-text-field disabled label="Full domain name" v-model="fullNewDomain"></v-text-field>
        
        <v-checkbox v-model="newHost.useNextAvailableAddress" label="Use next available IP Address"></v-checkbox>

        <v-text-field v-model="newHost.macAddress" label="MAC Address"></v-text-field>                
        <v-text-field v-show="!newHost.useNextAvailableAddress" v-model="newHost.ipAddress" label="IP Address"></v-text-field>                

        <v-select v-model="newHost.dhcpScope" label="DHCP Scope" :items="this.dhcpScopes"></v-select>

        <v-btn @click="this.createHost()" class="mt-2 bg-blue" type="submit" block>Submit</v-btn>
      </v-form>
    </v-sheet>
  </v-card-text>
</v-card>
</template>

<script>
  import ErrorDialog from './ErrorDialog.vue';

  export default {
    components: { ErrorDialog },
    props: [],
    data() {
      return {
        newHost: {
          useNextAvailableAddress: true
        },
        domains: [],
        dhcpScopes: [],
        error: {}
      }
    },
    methods: {
      reduceObjectToArray(obj, key) {
        return Object.values(obj).map(item => item[key]);
      },
      async getDomains() {
        const response = await fetch("/api/domains/list")
        this.domains = await response.json()

        this.domains = this.reduceObjectToArray(this.domains, 'domainName')
      },
      async getDhcpScopes() {
        const response = await fetch("/api/dhcpscopes/list")
        const scopes = await response.json()
        this.dhcpScopes = this.reduceObjectToArray(scopes.scopes, 'name')
      },
      createErrorDialog(error, exception, status) {
        this.error.response = error
        this.error.exception = exception
        this.error.status = status
        this.error.showDialog = true
      },
      createHost() {
        this.processingRequest = true

        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            hostname:     this.newHost.hostname,
            domain:       this.newHost.domain,
            managedDhcp:  true,
            ipAddress:    this.newHost.useNextAvailableAddress ? null : this.newHost.ipAddress,
            macAddress:   this.newHost.macAddress,
            dhcpScope:    this.dhcpScope
          })
        }

        fetch("/api/hosts", requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in host creation process")
              this.createErrorDialog(data.error, data.exception, data.status)
            } else {
              console.log("OK - host created")
              this.$emit("hostCreated")
            }
          })
        this.processingRequest = false
      }
    },
    mounted() {
      this.getDhcpScopes()
      this.getDomains()
    },
    computed: {
      fullNewDomain() {
        if (this.newHost.hostname && this.newHost.domain) {
          return `${this.newHost.hostname}.${this.newHost.domain}`
        } 
      }
    }
  }
</script>