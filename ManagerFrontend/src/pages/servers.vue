<template>
  <v-main class="d-flex flex-row">
    <v-tabs v-model="this.tab" direction="vertical">
      <v-tab
        prepend-icon="mdi-server"
        text="Servers"
        value="serverList">
      </v-tab>
      <v-tab
        prepend-icon="mdi-shield-refresh"
        text="Patching Groups"
        values="patchingGroups">
      </v-tab>
      <v-tab
        prepend-icon="mdi-history"
        text="Logs"
        values="domains">
      </v-tab>
    </v-tabs>
  </v-main>
</template>

<script>

</script>