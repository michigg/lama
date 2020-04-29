<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light" class="shadow fixed-top">
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
    <div class="content">
      <router-view></router-view>
    </div>
    <footer class="footer">
      <a href="#">Impressum</a> |
      <a href="#">Datenschutz</a>
    </footer>
  </div>
</template>

<style>
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
      --page-background: #fbb071 ;
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

  .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12, .col, .col-auto, .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12, .col-sm, .col-sm-auto, .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12, .col-md, .col-md-auto, .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12, .col-lg, .col-lg-auto, .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12, .col-xl, .col-xl-auto {
    -webkit-transition: max-width .5s ease-out;
    -moz-transition: max-width .5s ease-out;
    -o-transition: max-width .5s ease-out;
    transition: max-width .5s ease-out;
  }

  .content {
    -webkit-transition: margin-top .5s ease-out;
    -moz-transition: margin-top .5s ease-out;
    -o-transition: margin-top .5s ease-out;
    transition: margin-top .5s ease-out;
  }

  @media (max-width: 767px) {
    .content {
      margin-top: calc(var(--nav-height) + 1.5rem);
    }
  }

  @media (min-width: 768px) {
    .content {
      margin-top: var(--nav-height);
      margin-left: var(--admin-bar-width);
    }
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
