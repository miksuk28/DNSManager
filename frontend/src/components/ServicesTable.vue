<template>
  <table class="striped">
    <thead>
      <tr>
        <th scope="col">Domain name</th>
        <th scope="col">Description</th>
        <th scope="col">Target</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="service in services" :key="service.serviceId">
        <td><a :href="`http://${service.domainName}`" target="_blank">{{ service.domainName }}</a></td>
        <td>{{ service.description || '—' }}</td>
        <td><a @click="this.$router.push(`/hosts/${service.targetHostId}`)">{{ service.target }}</a></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    props: ["services"]
  }
</script>
