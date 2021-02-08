<template>
  <div>
    <button
      class="sidebar-activation-button btn btn-primary shadow"
      :class="{ active: active }"
      @click="active = !active"
    >
      <b-icon-layers/>
    </button>
    <div
      class="sidebar dynamic-sidebar border-right shadow"
      :class="{ active: active }"
    >
      <div class="sidebar-top">
        <p class="h4 p-2 mb-0">
          Bereiche
        </p>
        <b-list-group>
          <b-list-group-item
            v-for="realmItem in realms"
            :key="realmItem.id"
            :to="{name: 'Realm', params: {realmId: realmItem.id}}"
          >
            {{ realmItem.name }}
          </b-list-group-item>
        </b-list-group>
        Hallo {{ realm }}
        <div v-if="!!realm.id">
          <p class="h4 p-2 mb-0">
            Bereich {{ realm.name }}
          </p>
          <b-list-group>
            <b-list-group-item :to="{name: 'Realm', params: {realmId: realm.id}}">
              <b-icon-gear/>
              Einstellungen
            </b-list-group-item>
            <b-list-group-item :to="{name: 'Users', params: {realmId: realm.id}}">
              <b-icon-person/>
              Nutzer
            </b-list-group-item>
            <b-list-group-item :to="{name: 'Groups', params: {realmId: realm.id}}">
              <b-icon-people/>
              Gruppen
            </b-list-group-item>
          </b-list-group>
        </div>
      </div>
      <div class="sidebar-bottom">
        <b-list-group>
          <b-list-group-item
            v-if="$can('add', 'realm')"
            href="#"
          >
            Bereich hinzufügen
          </b-list-group-item>
          <b-list-group-item href="#">
            Django Adminbereich
          </b-list-group-item>
          <b-list-group-item href="#">
            Konfigurationen
          </b-list-group-item>
          <b-list-group-item href="#">
            Über
          </b-list-group-item>
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
    realms: function () {
      return this.$store.getters['realms/realms']
    },
    realm: function () {
      return this.$store.getters['realm/realm']
    }
  },
  mounted () {
    this.$store.dispatch('realms/fetchRealms')
  }
}
</script>

<style lang="scss" scoped>
@import "src/assets/styles/variables";

.sidebar-activation-button {
  display: block;
  width: 50px;
  margin-top: var(--nav-height) !important;
  left: 0;
  border-radius: 0 !important;
  -webkit-transition: margin .25s ease-out;
  -moz-transition: margin .25s ease-out;
  -o-transition: margin .25s ease-out;
  transition: margin .25s ease-out;

  &.active {
    display: block;
    margin-left: calc(var(--admin-bar-width));
  }
}

.dynamic-sidebar {
  margin-left: calc(0rem - var(--admin-bar-width));
  -webkit-transition: margin .25s ease-out;
  -moz-transition: margin .25s ease-out;
  -o-transition: margin .25s ease-out;
  transition: margin .25s ease-out;

  &.active {
    margin-left: 0;
  }
}

@media (min-width: 768px) {
  .dynamic-sidebar {
    margin-left: 0;
  }

  .sidebar-activation-button {
    display: none !important;
  }
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
  background-color: $body-bg;

  .list-group-item {
    border-right: 0;
    text-align: left;
    background-color: $body-bg;

    &:first-child {
      border-top-left-radius: 0;
      border-top-right-radius: 0;
    }

    &:last-child {
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
    }
  }

  .sidebar-bottom {
    margin-top: auto !important;
  }
}
</style>
