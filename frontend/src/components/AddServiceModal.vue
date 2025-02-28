<template>
  <dialog>
    <ErrorModal
      :open="this.showErrorModal"
      :error="this.responseError"
      :exception="this.responseException"
      :statis="this.responseStatus"
      @closeErrorModal="closeErrorModal()"
    />

    <article>
      <header>
        <button @click="closeAddServiceModal()" aria-label="Close" rel="prev"></button>
        <p><strong>Define new Service</strong></p>
      </header>

      <form>
        <fieldset>
          <label>
            Service name
            <input v-model="this.newHostname" type="text">
          </label>

          <label>
            Domain
            <select v-model="this.newDomain">
              <option required v-for="domain in this.availableDomains" :key="domain.domainId">
                {{ domain.domainName }}
              </option>
            </select>
          </label>

          <label>
            Domain preview
            <input :value="this.fullNewDomain" disabled type="text">
          </label>

          <label>
            Target host
            <input :value="this.targetHost" disabled type="text">
          </label>

          <label>
            Description
            <textarea v-model="this.newDescription" name="description" placeholder="Optional description" aria-label="description"></textarea>
          </label>
        </fieldset>
      </form>

      <footer>
        <button @click="console.log(this.availableDomains)" class="secondary">Clear Fields</button>
        <button @click="this.createService()" >Add</button>
      </footer>

    </article>
  </dialog>
</template>

<script>
  import ErrorModal from './ErrorModal.vue'
  
  export default {
    components: { ErrorModal },
    props: [ "targetHost", "targetHostId" ],
    data() {
      return {
        newHostname: null,
        newDomain: null,
        newDescription: null,
        availableDomains: [],
        showErrorModal: false,
        responseError: null,
        responseException: null,
        responseStatus: null,
        showErrorModal: false
      }
    },
    methods: {
      async getDomains() {
        const response = await fetch("/api/domains/list")
        this.availableDomains = await response.json()
      },

      closeAddServiceModal() {
        this.$emit("closeModal")
      },

      createErrorModal(error, exception, status) {
        this.responseError = error,
        this.responseException = exception
        this.responseStatus = status
        this.showErrorModal = true
      },
      closeErrorModal() {
        this.showErrorModal = false
      },
      createService() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            "serviceName":      this.newHostname,
            "domain":           this.newDomain,
            "hostId":           this.targetHostId,
            "description":      this.newDescription
          })
        }

        fetch("/api/services", requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught Exception in creation of service")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.$emit("updateServices")
              this.$emit("closeModal")
              this.newHostname = null,
              this.newDomain = null,
              this.newDescription = null
            }
          })
      }
    },

    mounted() {
      this.getDomains()
    },

    computed: {
      fullNewDomain() {
        if (this.newHostname && this.newDomain) {
          return `${this.newHostname}.${this.newDomain}`
        }
      }
    }
  }
</script>