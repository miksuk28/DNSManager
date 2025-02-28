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
        <td>{{ service.domainName }}</td>
        <td>{{ service.description || '—' }}</td>
        <td>{{ service.target }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    props: ["services"]
  }
</script>
