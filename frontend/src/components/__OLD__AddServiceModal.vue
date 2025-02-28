<template>
  <dialog>

    <dialog :open="false">
      <article>
        <header>
          <button aria-label="Close" rel="prev"></button>
          <p>
            <strong>Confirm service deletion</strong>
          </p>
        </header>

        <p>Are you sure you want to delete this service record?</p>

        <footer>
          <button class="primary">No</button>
          <button class="secondary">Yes</button>
        </footer>
      </article>
    </dialog>

    <article>
      <header>
        <button aria-label="Close" rel="prev"></button>
        <p>
          <strong>Services on host {{ hostId }}</strong>
        </p>
      </header>

      <p>Manage services pointing to <strong>{{ this.host.hostname }}</strong></p>

      <table>
        <thead>
          <tr>
            <th scope="col">Service</th>
            <th scope="col">Description</th>
            <th scope=""></th>
          </tr>
        </thead>
        <tbody>
          <tr  v-for="service in services" :key="service.serviceId">
            <th scope="row">{{ service.domainName }}</th>
            <td>{{ service.description || '—' }}</td>
            <th scope="col"><a class="secondary">Delete</a></th>
          </tr>
        </tbody>
      </table>

    </article>

  </dialog>
</template>

<script>
  export default {
    props: ["hostId"],
    data() {
      return {
        services: [],
        host: {}
      }
    },
    methods: {
      async getServicesForHost() {
        const response = await fetch(`/api/services/list?hostId=${this.hostId}`)
        this.services = await response.json()
        
        console.log(this.services)
      },

      async getHostInfo() {
        const response = await fetch(`/api/hosts/${hostId}`)
        this.host = await response.json()
      }
    },
    mounted() {
      this.getServicesForHost(),
      this.getHostInfo()
    }
  }
</script>