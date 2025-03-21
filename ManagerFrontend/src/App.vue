<template>
  <v-app>
    <Layout></Layout>
    <router-view />
  </v-app>
</template>

<script>
  import Layout from './components/Layout.vue';

  export default {
    components: { Layout }
  }
</script>
