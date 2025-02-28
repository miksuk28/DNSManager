<template>
  <dialog>
    <article>
      <header>
        <p><strong>An Error occured</strong></p>
      </header>
      <p>Manager returned with the following error message</p>
      <p>Response code: {{ status }}</p>
      <p><code>{{ exception }}: {{ error }}</code></p>

      <footer>
        <div class="grid">
          <button @click="closeModal()">OK</button>
        </div>
      </footer>
    </article>
  </dialog>
</template>

<script>
  export default {
    props: ["error", "exception", "status"],
    data() {

    },
    methods: {
      closeModal() {
        this.$emit("closeErrorModal")
      }
    }
  }
</script>