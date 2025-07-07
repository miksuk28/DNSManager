<template>
  <dialog>
    <ErrorModal @closeErrorModal="closeErrorModal()" :open="this.error.showErrorModal" :error="this.error.responseError" :exception="this.error.responseException" :status="this.error.responseStatus" />

    <article>
      <header>
        <button @click="closeRegisterAliasModal()" aria-label="Close" rel="prev" ></button>
        <p>
            <strong>Register Firewall Alias group</strong>
        </p>
      </header>

      <p>Add alias configuration below</p>

      <form>
        <fieldset>
          <label>
            OPNsense Alias UUID
            <input v-model="this.newAlias.uuid" type="text" name="uuid" placeholder="UUID">
          </label>

          <label>
            Display Name
            <input v-model="this.newAlias.displayName" type="text" name="displayname" placeholder="Display Name">
          </label>
        </fieldset>
      </form>

      <div class="grid">
        <button @click="this.registerAlias()" :aria-busy="this.processingRequest">Register Alias</button>
      </div>

    </article>
  </dialog>
</template>

<script>
  import ErrorModal from './ErrorModal.vue';

  export default {
    components: { ErrorModal },

    data() {
      return {
        processingRequest: false,
        error: {
          showErrorModal: false,
          responseError: null,
          responseException: null,
          responseStatus: null
        },
        newAlias: { }
      }
    },
    methods: {
      closeRegisterAliasModal() {
        this.$emit("closeModal")
      },
      closeErrorModal() {
        this.error.showErrorModal = false
      },
      createErrorModal(error, exception, status) {
        this.error.responseError = error
        this.error.responseException = exception
        this.error.responseStatus = status
        this.error.showErrorModal = true
      },
      resetNewAlias() {
        this.newAlias = {}
      },
      registerAlias() {
        this.processingRequest = true
        
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            "aliasId":        this.newAlias.uuid,
            "displayName":    this.newAlias.displayName
          })
        }

        fetch("/api/aliasgroups/register", requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in alias registration")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.$emit("updateAliasGroups")
              this.closeRegisterAliasModal()
              this.resetNewAlias()
            }
            this.processingRequest = false
          })
      }
    }
  }
</script>