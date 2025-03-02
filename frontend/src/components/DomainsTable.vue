<template>
  <table class="striped">
    <thead>
      <tr>
        <th scope="col">Domain</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="domain in domains" :key="domain.domainId">
        <td>{{ domain.domainName }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    props: ["domains"],
    data() {
      return {

      }
    }
  }
</script>