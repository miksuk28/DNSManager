<template>
  <dialog>
    <ErrorModal 
      @closeErrorModal="this.error.showModal=false"
      :open="this.error.showModal"
      :error="this.error.response"
      :exception="this.error.exception"
      :status="this.error.status"
    />

    <article>
      <header>
        <button @click="this.$emit('closeModal')" aria-label="Close" rel="prev"></button>
        <p>
          <strong>Add a New Domain</strong>
        </p>
      </header>

      <form>
        <fieldset>
          <input v-model="this.newDomain" placeholder="Base domain name" type="text">
        </fieldset>
      </form>
      <div @click="addDomain()" class="grid">
        <button >Add Domain</button>
      </div><
    </article>
  </dialog>
</template>

<script>
  import ErrorModal from './ErrorModal.vue';

  export default {
    components: { ErrorModal },
    data() {
      return {
        error: {},
        newDomain: null
      }
    },
    methods: {
      createErrorModal(error, exception, status) {
        this.error.response = error
        this.error.exception = exception
        this.error.status = status
        this.error.showModal = true
      },
      addDomain() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            "domainName": this.newDomain
          })
        }

        fetch("/api/domains", requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in domain creation")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.newDomain = null
              this.$emit("updateDomains")
              this.$emit("closeModal")
            }
          })
      }
    }
  }
</script>