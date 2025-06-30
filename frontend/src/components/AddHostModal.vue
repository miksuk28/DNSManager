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
            <input v-model="this.newHost.createAlias" name="createAlias" type="checkbox" role="switch" />
            Create alias on FW
          </label>

          <label>
            <input v-model="this.newHost.isManaged" name="isManaged" type="checkbox" role="switch" />
            Use next available address in range
          </label>

          <label>
            MAC Address
            <input v-model="this.newHost.macAddress" required type="text" name="macAddress" placeholder="FF:FF:FF:FF:FF:FF">
            <small>MAC Address used for static DHCP reservation</small>
          </label>

          <label v-if="!this.newHost.isManaged">
            IP Address
            <input v-model="this.newHost.ipAddress" required type="text" name="ipAddress" placeholder="X.X.X.X">
            <small>Manually set an address</small>
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

      <!--<progress v-if="this.processingRequest" />-->
      
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
          isManaged: true,
          createAlias: true
        }
      }
    },

    methods: {
      closeAddHostModal() {
        this.$emit('closeModal')
      },

      setLoadingState(state) {
        console.log(`Loading state: ${this.processingRequest}`)
        this.processingRequest = state
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
          isManaged: true,
          createAlias: true
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
        this.setLoadingState(true)

        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            hostname:       this.newHost.hostname,
            domain:         this.newHost.domain,
            managedDhcp:    true,
            ipAddress:      this.newHost.isManaged ? null : this.newHost.ipAddress,
            macAddress:     this.newHost.macAddress,
            dhcpScope:      this.newHost.dhcpScope,
            createAlias:    this.newHost.createAlias
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
            this.setLoadingState(false)
          })
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