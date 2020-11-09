<template>
  <b-nav-item-dropdown v-if="isLoggedIn"
                       right
  >
    <!-- Using 'button-content' slot -->
    <template #button-content>
      {{ user.username }}
    </template>
    <b-dropdown-item :to="{ name: 'Profil' }">Profil</b-dropdown-item>
    <b-dropdown-item @click="logout">Abmelden</b-dropdown-item>
  </b-nav-item-dropdown>
  <b-nav-item
    v-else
    :to="{ name: 'Login' }"
  >
    Anmelden
  </b-nav-item>
</template>

<script>

export default {
  name: 'AuthNavModule',
  computed: {
    isLoggedIn: function () {
      return this.$store.getters['authentication/isLoggedIn']
    },
    user: function () {
      return this.$store.getters['authentication/user']
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('authentication/logout')
        .then(() => {
          this.$router.push({ name: 'Login' })
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
