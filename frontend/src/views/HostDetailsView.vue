<template>
  <div class="container">
    <ErrorModal
      :open="deleteServiceError.showModal"
      @closeErrorModal="deleteServiceError.showModal = false"
      :error="deleteServiceError.responseError"
      :exception="deleteServiceError.responseException"
      :status="deleteServiceError.responseStatus"
    />

    <AddServiceModal
      :open="this.showAddServiceModal"
      :targetHost="this.host.hostname"
      :targetHostId="this.host.hostId"
      @closeModal="this.closeAddServiceModal()"
      @updateServices="this.getServicesOnHost()"
    />

    <YesNoModal
      :open="showDeleteServiceModal"
      header="Confirm Service Deletion"
      :message="`Do you want to delete ${this.serviceToDelete}?`"
      :highlightNo="true"
      @yesClick="deleteService()"
      @noClick="closeDeleteServiceModal()"
    />
    
    <YesNoModal 
      :open="showDeleteHostModal"
      header="Confirm Host Deletion"
      :message="`Do you want to delete ${this.host.hostname}?`"
      :highlightNo="true"
      @yesClick="deleteHost()"
      @noClick="this.showDeleteHostModal = false"
    />

    <hgroup>
      <h2>{{ this.host.hostname }}</h2>
      <h3><strong>{{ this.host.ipAddress }}</strong> - {{ this.host.dhcpScopeName }}</h3>
    </hgroup>
    <hr />
  </div>
  
  <main class="grid container">

    <div class="container">
      <table>
        
        <tbody>
          <tr>
            <td><strong>Hostname</strong></td>
            <td>{{ this.host.hostname }}</td>
          </tr>
          <tr>
            <td><strong>DHCP Scope</strong></td>
            <td>{{ this.host.dhcpScopeName }}</td>
          </tr>
          <tr>
            <td><strong>IP Address</strong></td>
            <td>{{ this.host.ipAddress }}/{{ this.host.dhcpNetmask }}</td>
          </tr>
          <tr>
            <td><strong>MAC Address</strong></td>
            <td>{{ this.host.macAddress ||  '—' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="grid">
        <button :disabled="this.services.length !== 0" @click="this.showDeleteHostModal = true" class="outline secondary">Delete host</button>
      </div>
    </div>

    <div class="container">
      <table>
        <thead>
          <tr>
            <th scope="col">Service address</th>
            <th scope="col">Description</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.serviceId">
            <th scope="row">{{ service.domainName }}</th>
            <th>{{ service.description || '—' }}</th>
            <th><button @click="openDeleteServiceModal(service.serviceId, service.domainName)" class="outline secondary">Delete</button></th>
          </tr>
        </tbody>
      </table>

      <div class="grid">
        <button @click="openAddServiceModal()" class="outline">Add Service</button>
      </div>

    </div>

  </main>
</template>

<script>
  import YesNoModal from '../components/YesNoModal.vue'
  import ErrorModal from '../components/ErrorModal.vue'
  import AddServiceModal from "../components/AddServiceModal.vue"

  export default {
    components: { YesNoModal, ErrorModal, AddServiceModal },
    data() {
      return {
        hostId: this.$route.params.hostId,
        host: {},
        services: [],
        showDeleteServiceModal: false,
        showAddServiceModal: false,
        serviceToDeleteId: null,
        serviceToDelete: "",
        deleteServiceError: {},
        showDeleteHostModal: false
      }
    },

    methods: {
      async getHostInfo() {
        const response = await fetch(`/api/hosts/${this.hostId}`)
        this.host = await response.json()
      },

      async getServicesOnHost() {
        const response = await fetch('/api/services/list?' + new URLSearchParams({
          hostId:   this.hostId
        }).toString())

        this.services = await response.json()
      },
      openAddServiceModal() {
        console.log("Open Add Service Modal")
        this.showAddServiceModal = true
      },
      closeAddServiceModal() {
        console.log("Close Add Service Modal")
        this.showAddServiceModal = false
      },
      openDeleteServiceModal(serviceId, domainName) {
        this.serviceToDeleteId = serviceId
        this.serviceToDelete = domainName
        this.showDeleteServiceModal = true
      },
      closeDeleteServiceModal() {
        this.serviceToDelete = null,
        this.serviceToDeleteId = null,
        this.showDeleteServiceModal = false
      },
      createErrorModal(error, exception, status) {
        this.deleteServiceError.responseError = error
        this.deleteServiceError.responseException = exception
        this.deleteServiceError.responseStatus = status
        this.deleteServiceError.showModal = true
      },
      closeErrorModal() {
        this.deleteServiceError.showModal = false
      },
      async deleteService() {
        const requestOptions = {
          method: "DELETE"
        }

        fetch(`/api/services/${this.serviceToDeleteId}`, requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Exception in service deletion")
            } else {
              console.log("OK")
              this.getServicesOnHost()
              this.closeDeleteServiceModal()
            }
          })
      },

      async deleteHost() {
        const requestOptions = {
          method: "DELETE"
        }

        this.showDeleteHostModal = false

        fetch(`/api/hosts/${this.hostId}`, requestOptions)
          .then(async response => {
            const data = await response.json()

            if (!response.ok) {
              console.log("Caught exception in host deletion")
              this.createErrorModal(data.error, data.exception, response.status)
            } else {
              console.log("OK")
              this.$router.push("/hosts")
            }
          })
      }
    },
    mounted() {
      this.getHostInfo(),
      this.getServicesOnHost()
    }
  }
</script>