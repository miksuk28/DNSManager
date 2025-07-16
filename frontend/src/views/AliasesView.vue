<template>
  <main class="container">
    <h3>Aliases</h3>
    <hr>

    <AliasListModal
      :open="this.showAliasListModal"
      @closeModal="this.showAliasListModal = false"
    />

    <AliasesTable :aliasGroups="this.aliasGroups" />

    <RegisterAliasModal 
      :open="this.showImportAliasModal"
      @closeModal="this.showImportAliasModal = false"
      @updateAliasGroups="this.getAliasGroups()"
    />

    <div class="grid">
      <button @click="this.showImportAliasModal=true" class="outline">Register Alias Group</button>
      <button @click="this.showAliasListModal=true" class="outline">Show Available Aliases</button>
    </div>
  </main>
</template>

<script>
  import AliasesTable from '@/components/AliasesTable.vue';
  import RegisterAliasModal from '@/components/RegisterAliasModal.vue';
  import AliasListModal from '@/components/AliasListModal.vue';

  export default {
    components: { RegisterAliasModal, AliasesTable, AliasListModal },
    data() {
      return {
        aliasGroups: [],
        showImportAliasModal: false,
        showAliasListModal: false
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