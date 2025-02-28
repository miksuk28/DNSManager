<template>
  <main class="container">
    <hgroup>
      <h2>{{ this.host.hostname }}</h2>
      <h3><strong>{{ this.host.ipAddress }}</strong> - {{ this.host.dhcpScopeName }}</h3>
    </hgroup>

    <table>
      <thead>
        <tr>
          <th scope="col">Service address</th>
          <th scope="col">Service address</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">TEST</th>
          <th>Service address</th>
        </tr>
        <tr>
          <th scope="row">TEST</th>
          <th>Service address</th>
        </tr>
      </tbody>
    </table>

  </main>
</template>

<script>
  export default {
    data() {
      return {
        hostId: this.$route.params.hostId,
        host: {}
      }
    },

    methods: {
      async getHostInfo() {
        const response = await fetch(`/api/hosts/${this.hostId}`)
        this.host = await response.json()
      }
    },
    mounted() {
      this.getHostInfo()
    }
  }
</script>