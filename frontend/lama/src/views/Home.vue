<template>
  <div class="home">
    <div v-for="rule in rules" :key="rule.description">
      <b-list-group-item v-if="$can(rule.action, rule.subject)">{{rule.description}}</b-list-group-item>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  name: 'Home',
  computed: {
    rules: function () {
      console.log('Rules', this.$store.getters['authentication/rules'])
      return this.$store.getters['authentication/rules']
    }
  }
}
</script>
