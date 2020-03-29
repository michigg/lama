<template>
  <div class="d-flex wrapper">
    <div class="bg-light border-right sidebar-wrapper text-left">
      <div class="border-top w-100"></div>
      <div v-if="permissions === 'SUPER_USER' || permissions === 'MULTI_REALM_ADMIN'">
        <div v-if="realms.length !== 1">
          <h2 class="sidebar-heading">Bereiche</h2>
          <div
            class="list-group list-group-flush">
            <a v-for="realm in realms" :key="realm.id"
               :href="realm.url"
               class="list-group-item list-group-item-action bg-light">
              {{realm.name}}
            </a>
          </div>
        </div>
        <div v-else>
          <div class="list-group list-group-flush">
            <a class="list-group-item list-group-item-action bg-light">
              <b-icon-inboxes></b-icon-inboxes>
              Bereichsübersicht
            </a>
          </div>
          <h2 class="sidebar-heading">Bereich {{ realms[0].name }}</h2>
          <div class="list-group list-group-flush">
            <a class="list-group-item list-group-item-action bg-light">
              <b-icon-info-square></b-icon-info-square>
              Bereichsinformationen
            </a>
            <a class="list-group-item list-group-item-action bg-light">
              <b-icon-people-fill></b-icon-people-fill>
              Nutzer
            </a>
            <a class="list-group-item list-group-item-action bg-light">Gruppen</a>
          </div>
        </div>
        <div class="sidebar-bottom list-group-flush border-top">
        </div>
      </div>

      <!--  BOTTOM-->
      <div v-if="permissions === 'SUPER_USER' && realms" class="list-group list-group-flush">
        <a class="list-group-item list-group-item-action bg-light">
          <b-icon-plus-square-fill></b-icon-plus-square-fill>
          Bereich hinufügen
        </a>
      </div>
      <div v-if="permissions === 'SUPER_USER'"
           class="list-group list-group-flush"
      >
        <a class="list-group-item list-group-item-action bg-light">
          <b-icon-shield></b-icon-shield>
          Adminbereich
        </a>
      </div>
      <div v-if="permissions === 'SUPER_USER'"
           class="list-group list-group-flush">
        <a class="list-group-item list-group-item-action bg-light">
          <b-icon-gear></b-icon-gear>
          Konfigurationen
        </a>
      </div>
      <a class="list-group-item list-group-item-action bg-light">
        <b-icon-question-square></b-icon-question-square>
        Über
      </a>
    </div>

    <div class="page-content-wrapper">
      <div class="container-fluid">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminSidebar',
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
  .sidebar-bottom {
    position: fixed;
    width: 15rem;
    bottom: 0;
  }

  .sidebar-wrapper {
    min-height: calc(100vh - 56px);
    margin-left: -15rem;
    -webkit-transition: margin .25s ease-out;
    -moz-transition: margin .25s ease-out;
    -o-transition: margin .25s ease-out;
    transition: margin .25s ease-out;
  }

  .sidebar-wrapper .sidebar-heading {
    padding: 0.875rem 1.25rem;
    margin-bottom: 0;
    font-size: 1.2rem;
  }

  .sidebar-wrapper .list-group {
    width: 15rem;
  }

  @media (min-width: 768px) {
    .sidebar-wrapper {
      margin-left: 0;
    }

    .page-content-wrapper {
      min-width: 0;
      width: 100%;
    }

    .wrapper.toggled .sidebar-wrapper {
      margin-left: -15rem;
    }
  }

  .page-content-wrapper {
    width: 100vw;
  }

  .wrapper.toggled .sidebar-wrapper {
    margin-left: 0;
  }
</style>
