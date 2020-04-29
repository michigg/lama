<template>
  <div>
    <button v-on:click="active = !active" class="sidebar-activation-button btn btn-primary shadow"
            v-bind:class="{ active: active }">
      <b-icon-layers></b-icon-layers>
    </button>
    <div class="sidebar dynamic-sidebar border-right shadow" v-bind:class="{ active: active }">
      <div class="sidebar-top">
        Bereiche
        <b-list-group>
          <b-list-group-item href="#">Bereich 1 - 1</b-list-group-item>
          <b-list-group-item href="#">Bereich 1 - 2</b-list-group-item>
          <b-list-group-item href="#">Bereich 1 - 3</b-list-group-item>
        </b-list-group>
        Bereich
        <b-list-group>
          <b-list-group-item href="#">Nutzer</b-list-group-item>
          <b-list-group-item href="#">Gruppen</b-list-group-item>
        </b-list-group>
      </div>
      <div class="sidebar-bottom">
        <b-list-group>
          <b-list-group-item href="#" v-if="$can('add', 'realm')">Bereich hinzufügen</b-list-group-item>
          <b-list-group-item href="#">Django Adminbereich</b-list-group-item>
          <b-list-group-item href="#">Konfigurationen</b-list-group-item>
          <b-list-group-item href="#">Über</b-list-group-item>
        </b-list-group>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminSidebar',
  data () {
    return {
      active: false
    }
  },
  computed: {
    permissions: function () {
      return 'SUPER_USER'
    },
    realms: function () {
      return [{
        name: 'Test Bereich1',
        url: 'http://localhost:8000/api/v1/realm/1/'
      }, {
        name: 'Test Bereich2',
        url: 'http://localhost:8000/api/v1/realm/2/'
      }, {
        name: 'Test Bereich3',
        url: 'http://localhost:8000/api/v1/realm/3/'
      }]
    }
  }
}
</script>

<style scoped>
  .sidebar-activation-button {
    display: block;
    width: 50px;
    margin-top: -1.5rem !important;
    position: fixed;
    /*margin-left: calc(50px + var(--admin-bar-width)) !important;*/
    left: 0;
    border-radius: 0 !important;
    -webkit-transition: margin .25s ease-out;
    -moz-transition: margin .25s ease-out;
    -o-transition: margin .25s ease-out;
    transition: margin .25s ease-out;
  }

  .sidebar {
    display: -ms-flexbox !important;
    display: -webkit-box !important;
    display: flex !important;
    -ms-flex-direction: column !important;
    -webkit-box-orient: vertical !important;
    -webkit-box-direction: normal !important;
    flex-direction: column !important;
    top: var(--nav-height);
    min-height: calc(100vh - var(--nav-height) - var(--footer-height));
    width: var(--admin-bar-width);
    position: fixed;
    left: 0;
    z-index: 8000;
    background-color: var(--sidbar-background-color);
  }

  .dynamic-sidebar {
    margin-left: calc(0rem - var(--admin-bar-width));
    -webkit-transition: margin .25s ease-out;
    -moz-transition: margin .25s ease-out;
    -o-transition: margin .25s ease-out;
    transition: margin .25s ease-out;
  }

  .active.dynamic-sidebar {
    margin-left: 0;
  }

  .active.sidebar-activation-button {
    display: block;
    margin-left: calc(var(--admin-bar-width));
  }

  @media (min-width: 768px) {
    .dynamic-sidebar {
      margin-left: 0;
    }

    .sidebar-activation-button {
      display: none !important;
    }
  }

  .sidebar-bottom {
    margin-top: auto !important;
  }

  .list-group-item:first-child {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }

  .list-group-item:last-child {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .list-group-item {
    border-right: 0;
    text-align: left;
    background-color: var(--sidbar-background-color);
  }

</style>
