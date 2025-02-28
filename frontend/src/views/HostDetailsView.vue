<template>
  <main class="container">
    <div class="grid">

      <article>
        <header>Host information</header>
        Information about the host
      </article>

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

    </div>
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
    }
  }
</script>