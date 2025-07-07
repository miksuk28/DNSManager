<template>
  <main class="container">
    <h3>Aliases</h3>
    <hr>

    <AliasesTable :aliasGroups="this.aliasGroups" />

    <RegisterAliasModal 
      :open="this.showImportAliasModal"
      @closeModal="this.showImportAliasModal = false"
      @updateAliasGroups="this.getAliasGroups()"
    />

    <div class="grid">
      <button @click="this.showImportAliasModal=true" class="outline">Import Alias Group</button>
    </div>
  </main>
</template>

<script>
  import AliasesTable from '@/components/AliasesTable.vue';
  import RegisterAliasModal from '@/components/RegisterAliasModal.vue';

  export default {
    components: { RegisterAliasModal, AliasesTable },
    data() {
      return {
        aliasGroups: [],
        showImportAliasModal: false
      }
    },
    methods: {
      async getAliasGroups() {
        const response = await fetch("/api/aliasgroups/list")
        this.aliasGroups = await response.json()
      }
    },
    mounted() {
      this.getAliasGroups()
    }
  }
</script>