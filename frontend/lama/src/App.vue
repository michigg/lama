<template>
  <div id="app">
    <navbar/>
    <div v-if="isLoggedIn">
      <admin-base-page/>
    </div>
    <div v-else>
      <user-base-page/>
    </div>

    <footer class="footer bg-dark">
      <a href="#">Impressum</a> |
      <a href="#">Datenschutz</a>
    </footer>
  </div>
</template>

<script>
import AdminBasePage from './views/base/Admin'
import UserBasePage from './views/base/User'
import Navbar from './components/utils/Navbar'

export default {
  components: {
    Navbar,
    UserBasePage,
    AdminBasePage
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters['authentication/isLoggedIn']
    }
  }
}
</script>

<style lang="scss">
  @import './assets/styles/custom.scss';

  :root {
    --admin-bar-width: 15rem;
    --nav-height: 3rem;
    --footer-height: 2.5rem;
  }

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }

  nav {
    height: var(--nav-height);
  }

</style>
