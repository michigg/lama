<template>
  <h1>{{ title }}</h1>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Headline',
  props: {
    title: {
      type: String,
      required: true
    }
  }
})
</script>

<style scoped>

</style>
