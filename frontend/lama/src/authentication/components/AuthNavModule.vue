<template>
  <b-nav-item
    v-if="this.isLoggedIn"
    @click="logout"
  >
    Logout
  </b-nav-item>
  <b-nav-item
    v-else
    :to="{ name: 'Login' }"
  >
    Login
  </b-nav-item>
</template>

<script>
import { RepositoryFactory } from '../repositories/RepositoryFactory'
console.log(RepositoryFactory)
// const AuthenticationRepository = RepositoryFactory.get('authentication')

export default {
  name: 'AuthNavModule',
  props: {
    msg: String
  },
  computed: {
    isLoggedIn: function () {
      // return AuthenticationRepository.isLoggedIn()
      return true
    }
  },
  created: function () {
    // Used in term of an expired Token case
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function () {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err
      })
    })
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
