<template>
  <dialog>
    <article>
      <header>
        <button @click="this.closeModal()" aria-label="Close" rel="prev"></button>
        <p><strong>Available Aliases</strong></p>
      </header>

      <!--
      <div class="container-fluid">
        <table class="striped">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Button</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alias in aliases" :key="alias.name">
              <td>{{ alias.name }}</td>
              <td>{{ alias.description ||  '—' }}</td>
              <td><button @click="" class="outline secondary">Register</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      -->

      <form>
        <fieldset>

          <label>
            OPNsense Alias
            <select v-model="this.aliasToRegister">
              <option required v-for="alias in this.aliases" :key="alias.name">
                {{ alias.name }}
              </option>
            </select>
          </label>

          <label>
            Display Name
            <input :value="this.aliasDisplayName" placeholder="Display name (optional)" type="text">
          </label>

          <label>
            Description
            <input :value="this.getAliasDescription" disabled type="text">
          </label>

          <label>
            <input v-model="this.availableForAllScopes" type="checkbox" role="switch">
            Available for all address scopes
          </label>

          <label v-if="!this.availableForAllScopes">
            Available for Scopes
            <select aria-label="Select scopes" multiple size="4">
              <option v-for="scope in this.dhcpScopes.scopes" :key="scope.name">
                {{ scope.name }}
              </option>
            </select>
          </label>

        </fieldset>
      </form>

      <footer>
        <button @click="console.log(this.dhcpScopes)">Chud Button</button>
      </footer>

    </article>
  </dialog>
</template>

<script>
import { toHandlers } from 'vue'

  export default {
    props: [],
    data() {
      return {
        aliases: [],
        dhcpScopes: [],
        aliasToRegister: null,
        availableForAllScopes: true
      }
    },
    methods: {
      async getAliases() {
        const response = await fetch("/api/aliasgroups/listAvailable")
        this.aliases = await response.json()
      },
      async getDhcpScopes() {
        const response = await fetch("/api/dhcpscopes/list")
        this.dhcpScopes = await response.json()
      },
      closeModal() {
        this.$emit("closeModal")
      }
    },
    mounted() {
      this.getAliases()
      this.getDhcpScopes()
    },

    computed: {
      getAliasDescription() {
        if (this.aliasToRegister) {
          let description = this.aliases[this.aliasToRegister].description

          if (description) {
            return description
          }

          return '—'
        }
      }
    }
  }
</script>