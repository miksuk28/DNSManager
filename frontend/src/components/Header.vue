<template>
  <main class="container">
    <nav>
      <ul>
        <li><strong>{{ this.title }}</strong></li>
      </ul>
      <ul>
        <RouterLink to="/services"><li><a class="contrast">Services</a></li></RouterLink>
        <RouterLink to="/hosts"><li><a class="contrast">Hosts</a></li></RouterLink>
        <RouterLink to="/domains"><li><a class="contrast">Domains</a></li></RouterLink>
        <RouterLink to="/aliases"><li><a class="contrast">Aliases</a></li></RouterLink>
      </ul>
    </nav>
  </main>
</template>

<script>
  export default {
    data() {
      return {
        title: null
      }
    },
    methods: {
      async getHeader() {
        const response = await fetch("/api/header")
        this.title = await response.text()
        console.log(`Header is: ${this.title}`)
      }
    },
    created() {
      this.getHeader()
    }
  }
</script>