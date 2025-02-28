<template>
  <dialog>
    <ErrorModal @closeErrorModal="closeErrorModal()" :open="this.showErrorModal" :error="this.responseError" :exception="this.responseException" :status="this.responseStatus" />

    <article>
      <header>
        <button @click="closeAddHostModal()" aria-label="Close" rel="prev"></button>
        <p>
          <strong>Add new host</strong>
        </p>
      </header>
      
      <p>Add host configuration below</p>

      <form>
        <fieldset>
          <label>
            Hostname
            <input v-model="this.newHost.hostname" type="text" name="hostname" placeholder="Short hostname without domain">
          </label>

          <label>
            Domain
            <select v-model="this.newHost.domain" required name="domain" id="domain">
              <option v-for="domain in this.availableDomains" :key="domain.domainId">
                {{ domain.domainName }}
              </option>
            </select>
          </label>
  
          <label>
            Domain preview
            <input disabled :value="fullNewDomain" type="text">
          </label>

          <label>
            <input v-model="this.newHost.isManaged" name="isManaged" type="checkbox" role="switch" />
            Managed address
          </label>

          <label v-if="this.newHost.isManaged">
            MAC Address
            <input v-model="this.newHost.macAddress" required type="text" name="macAddress" placeholder="FF:FF:FF:FF:FF:FF">
            <small>Static DHCP reservation with the next available IP will be made within the desired DHCP scope</small>
          </label>

          <label v-if="!this.newHost.isManaged">
            IP Address
            <input v-model="this.newHost.ipAddress" required type="text" name="ipAddress" placeholder="X.X.X.X">
            <small>Unmanaged hosts will be added to database to avoid address collision, but no DHCP lease will be created</small>
          </label>

          <label>
            Addres Scope
            <select v-model="this.newHost.dhcpScope">
              <option required v-for="scope in this.availableDhcpScopes" :key="scope.name">
                {{ scope.name }}
              </option>
            </select>
          </label>
        </fieldset>
      </form>

      <footer>
        <button @click="resetNewHost()" class="secondary">Clear fields</button>
        <button @click="createHost()" :aria-busy="this.processingRequest" class="primary">Add</button>
      </footer>

    </article>
  </dialog>
</template>

<script>
  import ErrorModal from './ErrorModal.vue';

  export default {
    components: { ErrorModal },

    data() {
      return {
        availableDomains:     [],
        availableDhcpScopes:  [],
        responseError:        "",
        responseException:    "",
        responseStatus:       0,
        showErrorModal: false,
        processingRequest: false,
        newHost: {
          isManaged: true
        }
      }
    },

    methods: {
      closeAddHostModal() {
        this.$emit('closeModal')
      },

      async getDomains() {
        const response = await fetch("/api/domains/list")
        this.availableDomains = await response.json()
      },

      async getDhcpScopes() {
        const response = await fetch("/api/dhcpscopes/list")
        const scopes = await response.json()
        this.availableDhcpScopes = scopes.scopes
      },
      resetNewHost() {
        this.newHost = {
          isManaged: true
        }
      },

      createErrorModal(error, exception, status) {
        this.responseError = error
        this.responseException = exception
        this.responseStatus = status
        this.showErrorModal = true
      },

      closeErrorModal() {
        this.showErrorModal = false
      },

      createHost() {
        this.processingRequest = true

        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            hostname:       this.newHost.hostname,
            domain:         this.newHost.domain,
            managedDhcp:    this.newHost.isManaged,
            ipAddress:      this.newHost.ipAddress,
            macAddress:     this.newHost.macAddress,
            dhcpScope:      this.newHost.dhcpScope
          })
        }

        fetch("/api/hosts", requestOptions)
          .then(async response => {
            const data = await response.json()
            
            if (!response.ok) {
              console.log("Caught exception somewhere")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.$emit('updateHosts')
              this.closeAddHostModal()
              this.resetNewHost()
            }
          })
        this.processingRequest = false
      }
    },

    computed: {
      fullNewDomain() {
        if (this.newHost.hostname && this.newHost.domain) {
          return `${this.newHost.hostname}.${this.newHost.domain}`
        }
      }
    },

    mounted() {
      this.getDomains(),
      this.getDhcpScopes()
    }
  }
</script>