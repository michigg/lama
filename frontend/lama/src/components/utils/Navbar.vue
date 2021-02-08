<template>
  <b-navbar
    toggleable="lg"
    type="light"
    variant="light"
    class="fixed-top content"
  >
    <b-navbar-brand to="/">
      <img
        src="../../assets/logo.svg"
        class="d-inline-block align-top"
        width="30"
        height="30"
        alt="Logo"
      >
      Lama
    </b-navbar-brand>
    <b-collapse
      id="nav-text-collapse"
      is-nav
    >
      <b-navbar-nav>
        <b-nav-item to="/about">
          About
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <auth-nav-module />
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import AuthNavModule from '../../apps/authentication/components/AuthNavModule'

export default {
  name: 'Navbar',
  components: { AuthNavModule }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
