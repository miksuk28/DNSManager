<template>
  <ErrorDialog 
    :error="this.error"
    v-model="this.error.showDialog"
    @close="this.error.showDialog = false"
  />

  <v-card title="New Service">
    <v-card-text>
      <v-sheet class="">
        <v-form @submit.prevent>
          <v-text-field v-model="newService.hostname" label="Short Hostname"></v-text-field>                
          <v-select v-model="newService.domain" :items="this.domains" label="Domain"></v-select>
          
          <v-text-field disabled v-model="this.fullNewDomain" label="Full domain name"></v-text-field>
          
          <v-btn @click="this.createHost()" class="mt-2 bg-blue" type="submit" block>Submit</v-btn>
        </v-form>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>

<script>
  import ErrorDialog from './ErrorDialog.vue';

  export default {
    components: { ErrorDialog },
    props: ["domains"],
    data() {
      return {
        newService: {},
        error: {}
      }
    },
    methods: {

    },
    computed: {
      fullNewDomain() {
        if (this.newService.hostname && this.newService.domain) {
          return `${this.newService.hostname}.${this.newService.domain}`
        } 
      }
    }
  }
</script>