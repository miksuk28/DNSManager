<template>
  <v-card title="New Service">
    <v-card-text>
      <v-sheet class="">
        <v-form @submit.prevent>
          <v-text-field label="Short Hostname"></v-text-field>                
          <v-select label="Domain"></v-select>
          
          <v-text-field disabled label="Full domain name"></v-text-field>
          
          <v-checkbox label="Use next available IP Address"></v-checkbox>

          <v-btn @click="this.createHost()" class="mt-2 bg-blue" type="submit" block>Submit</v-btn>
        </v-form>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    data() {
      return {
        newService: {}
      }
    }
  }
</script>