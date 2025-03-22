<template>
</template>

<script>
  export default {
    methods: {
      goToHosts() {
        this.$router.push("/hosts")
      }
    },
    mounted() {
      this.goToHosts()
    }
  }
</script>
