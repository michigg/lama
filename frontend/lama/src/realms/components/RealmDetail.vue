<template>
  <b-list-group
    flush
    class="w-100 text-left"
  >
    <b-list-group-item>
      LDAP Organisationseinheit: <span class="float-right">{{ realm.ldap_base_dn }}</span>
    </b-list-group-item>
    <!--          <b-list-group-item>Nutzeranzahl (Aktive/Inaktive): {{ realm.users_count }}-->
    <!--            ({{ realm.users_count.inactive_user_count }}/{{ realm.inactive_user_count }})-->
    <!--            <a href="#" class="float-right">Inaktive Nutzer löschen</a>-->
    <!--          </b-list-group-item>-->
    <b-list-group-item v-if="realm.email">
      Email: <span class="float-right">{{ realm.email }}</span>
    </b-list-group-item>
    <b-list-group-item v-else>
      Email: <span class="float-right text-danger"><b-icon-exclamation-triangle-fill /> Noch ausstehend</span>
    </b-list-group-item>
    <b-list-group-item v-if="realm.admin_group">
      Admin Gruppe: <a
        href="#"
        class="float-right badge badge-primary p-2"
      >{{ realm.admin_group }}</a>
    </b-list-group-item>
    <b-list-group-item v-else>
      Admin Gruppe: <span class="float-right text-warning">
        <b-icon-exclamation-triangle-fill /> Noch ausstehend
      </span>
    </b-list-group-item>
    <b-list-group-item v-if="realm.default_group">
      Default Gruppe: <a
        href="#"
        class="float-right badge badge-secondary p-2"
      >{{ realm.default_group }}</a>
    </b-list-group-item>
    <b-list-group-item v-else>
      Default Gruppe: <span class="float-right text-warning">
        <b-icon-exclamation-triangle-fill /> Noch ausstehend
      </span>
    </b-list-group-item>
  </b-list-group>
</template>
<script>
export default {
  name: 'RealmDetail',
  props: {
    realm: {}
  }
}
</script>
