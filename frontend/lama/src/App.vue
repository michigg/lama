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
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
  @import '../node_modules/bootstrap-vue/src/index.scss';

  :root {
    --admin-bar-width: 15rem;
    --nav-height: 3rem;
    --footer-height: 2.5rem;
  }

  @media (prefers-color-scheme: light) {
    :root {
      --background-color: #ffffff;
      --footer-background-color: #282828;
      --secondary: #fbb071 !important;
      --sidbar-background-color: #f6d76f;
      --sidbar-activation-button-background-color: #f6d76f;
      --sidbar-activation-button-color: #000;
      --page-background: #fbb071;
      --primary: #fbb071 !important;
      --text-color: #343a40;
    }
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --background-color: #222831;
      --page-background: #393e46;
      --primary-color: #b55400;
      --text-color: #eeeeee;
    }
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

  footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    height: var(--footer-height) !important;
    padding-top: 0.5rem;
    background-color: var(--footer-background-color);
  }

  nav {
    height: var(--nav-height);
  }

</style>
