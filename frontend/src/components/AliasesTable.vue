<template>
  <div>
    <table class="striped">
      <thead>
        <tr>
          <th scope="col">Display Name</th>
          <th scope="col">Alias Name</th>
          <th scope="col">Description</th>
          <th scope="col">ID</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="aliasGroup in aliasGroups" :key="aliasGroup.aliasId">
          <td>{{ aliasGroup.aliasDisplayName }}</td>
          <td>{{ aliasGroup.aliasName }}</td>
          <td>{{ aliasGroup.aliasDescription }}</td>
          <td>{{ aliasGroup.aliasId }}</td>
        </tr>
      </tbody>

    </table>
  </div>
</template>

<script>
  export default {
    props: ["aliasGroups"],
    methods: {

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