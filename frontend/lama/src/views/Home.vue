<template>
  <div class="home">
    <!--    <img alt="Vue logo" src="../assets/logo.png">-->
    <HelloWorld msg="Welcome to Your Vue.js App" />
    <div v-for="rule in rules" :key="rule.description">
      <b-list-group-item v-if="$can(rule.action, rule.subject)">{{rule.description}}</b-list-group-item>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  },
  computed: {
    rules: function () {
      console.log('Rules', this.$store.getters['authentication/rules'])
      return this.$store.getters['authentication/rules']
    }
  }
}
</script>
