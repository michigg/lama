<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand to="/">
        <img
          src="./assets/logo.svg"
          class="d-inline-block align-top"
          width="30"
          height="30"
          alt="Logo"
        >
        Lama
      </b-navbar-brand>
      <b-collapse id="nav-text-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/account-management">Accounting</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <auth-module></auth-module>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <admin-sidebar></admin-sidebar>
  </div>
</template>

<style>
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

</style>
<script>
import AuthModule from './components/AuthModule'
import AdminSidebar from './components/AdminSidebar'

export default {
  components: {
    AdminSidebar,
    AuthModule
  }
}
</script>
