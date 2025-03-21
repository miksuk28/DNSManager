<template>
  <ErrorDialog 
    :error="this.error"
    v-model="this.error.showDialog"
    @close="this.error.showDialog = false"
  />

  <v-card title="New Domain">
    <v-card-text>
      <v-sheet class="">
        <v-form @submit.prevent>
          <v-text-field v-model="this.newDomain" label="Domain"></v-text-field> 
          <v-btn @click="this.createDomain()" class="mt-2 bg-blue" type="submit" block>Add Domain</v-btn>
        </v-form>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>

<script>
  import ErrorDialog from './ErrorDialog.vue';

  export default {
    components: { ErrorDialog },
    emits: ["domainCreated"],
    data() {
      return {
        newDomain: null,
        error: {}
      }
    },
    methods: {
      createErrorDialog(error, exception, status) {
        this.error.response = error
        this.error.exception = exception
        this.error.status = status
        this.error.showDialog = true
      },
      createDomain() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({
            domainName:     this.newDomain
          })
        }

        fetch("/api/domains", requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in domain creation process")
              this.createErrorDialog(data.error, data.exception, data.status)
            } else {
              console.log("Created domain")
              this.newDomain = null
              this.$emit("domainCreated")
            }
          })
      }
    }
  }
</script>