<template>
  <div class="">
    <table class="striped">
      <thead>
        <tr>
          <th scope="col">Hostname</th>
          <th scope="col">IP Address</th>
          <th scope="col">Managed</th>
          <th scope="col">MAC Address</th>
          <th scope="col">DHCP Scope</th>
          <!--<th scope="col"></th>-->
        </tr>
      </thead>
      <tbody>
        <tr v-for="host in hosts" :key="host.hostId">
          <td><a @click="this.$router.push(`/hosts/${host.hostId}`)">{{ host.hostname }}</a></td>
          <td>{{ host.ipAddress }}</td>
          <td>{{ host.managedDhcp === 1 ? "Yes" : "No" }}</td>
          <td>{{ host.macAddress || '—'}}</td>
          <td>{{ host.dhcpScopeName }}</td>
          <!--<td><small><button class="outline primary">+</button></small></td>-->
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
  export default {
    props: ["hosts"],
    methods: {
      openAddServiceModal(hostId) {
        this.$emit('addServiceModal', hostId)
      },
      openHostDetailPage(hostId) {
        return
      }
    }
  }
</script>

<style>
.table-height {
  width: fit-content;
  max-height: 500px;
  overflow: scroll;
}
</style>