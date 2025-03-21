<template>
  <v-dialog width="auto">
    <v-card prepent-icon="mdi-alert-circle" title="An Error Occured">
      <v-card-text>
        <p>Manager returned the following exception with the code {{ error.status }}</p>
      </v-card-text>

      <v-card-text>
        <code>{{ error.exception }}: {{ error.response }}</code>
      </v-card-text>

      <template v-slot:actions>
        <v-btn
          class="ms-auto"
          text="OK"
          @click="$emit('close')"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props: ["error"]
  }
</script>