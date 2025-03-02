<template>
  <div>
    <ErrorModal 
      :open="error.showModal"
      :error="error.response"
      :exception="error.exception"
      :status="error.status"
      @closeErrorModal="this.error.showModal=false"
    />
    <YesNoModal
      :open="showDeleteDomainModal"
      header="Confirm Domain Deletion"
      :message="`Do you want to delete domain ${this.domainToDelete}?`"
      :highlightNo="true"
      @noClick="this.showDeleteDomainModal=false"
      @yesClick="this.deleteDomainById(this.domainIdToDelete)"
    />
    <table class="striped">
      <thead>
        <tr>
          <th scope="col">Domain</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="domain in domains" :key="domain.domainId">
          <td>{{ domain.domainName }}</td>
          <td><div class="grid">
            <button @click="this.openDeleteDomainModal(domain.domainName, domain.domainId)" class="outline">Delete</button>
          </div></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import YesNoModal from './YesNoModal.vue'
  import ErrorModal from './ErrorModal.vue'

  export default {
    props: ["domains"],
    components : { YesNoModal, ErrorModal },
    data() {
      return {
        error: {},
        showDeleteDomainModal: false,
        domainToDelete: null,
        domainIdToDelete: null
      }
    },
    methods: {
      openDeleteDomainModal(domainName, domainId) {
        console.log(domainName, domainId)
        this.domainToDelete = domainName
        this.domainIdToDelete = domainId
        this.showDeleteDomainModal = true

      },
      createErrorModal(error, exception, status) {
        this.error.response = error
        this.error.exception = exception
        this.error.status = status
        this.error.showModal = true
      },
      deleteDomainById(domainId) {
        this.showDeleteDomainModal = false
        
        const requestOptions = {
          method: "DELETE"
        }

        fetch(`/api/domains/${domainId}`, requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in domain deletion")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.$emit("getDomains")
            }
          })
      }
    }
  }
</script>