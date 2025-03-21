<template>
  <v-app-bar title="Buppy DNS Manager"></v-app-bar>

  <v-navigation-drawer>
    <v-list nav>
      <v-list-item @click="this.$router.push('/services')" title="Services" link></v-list-item>
      <v-list-item @click="this.$router.push('/hosts')" title="Hosts" link></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
</script>