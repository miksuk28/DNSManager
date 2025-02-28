<template>
  <dialog>
    <article>
      <header v-show="header">
        <button @click="noClick()" aria-label="Close" rel="prev"></button>
        <p><strong>{{ header }}</strong></p>
      </header>
      <p>{{ message }}</p>
      <footer>
        <button @click="noClick()"  :class="{ secondary: !highlightNo }">No</button>
        <button @click="yesClick()" :class="{ secondary: highlightNo }">Yes</button>
      </footer>
    </article>
  </dialog>
</template>

<script>
  export default {
    props: [ "header", "message", "highlightNo" ],
    methods: {
      yesClick() {
        this.$emit('yesClick')
      },
      noClick() {
        this.$emit('noClick')
      }
    }
  }
</script>