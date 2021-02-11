<template>
  <b-form @submit.prevent="login">
    {{ realm }}
    <div class="floating-label-input-group">
      <input
        id="ldap-base-dn-input"
        v-model="form.ldapBaseDn"
        class="form-control"
        type="text"
        placeholder="LDAP Base DN"
      >
      <label for="ldap-base-dn-input">LDAP Base DN</label>
    </div>
    <div class="floating-label-input-group">
      <input
        id="name-input"
        v-model="form.name"
        class="form-control"
        type="text"
        placeholder="Bereichsname"
      >
      <label for="name-input">Bereichsname</label>
    </div>
    <div class="floating-label-input-group">
      <input
        id="email-input"
        v-model="form.email"
        class="form-control"
        type="email"
        placeholder="Bereichs-E-Mail-Adresse"
      >
      <label for="email-input">Bereichs-E-Mail-Adresse</label>
    </div>
    Admin Gruppe
    <b-form-select
      v-model="adminGroup"
      :options="adminGroupOptions"
    />
    Default Gruppe
    <b-form-select
      v-model="defaultGroup"
      :options="defaultGroupOptions"
    />
    <div class="d-flex mt-4">
      <b-btn
        type="submit"
        class="btn btn-primary mr-auto p-2"
      >
        Speichern
      </b-btn>
      <!--      TODO: abort-->
      <a
        href="#"
        class="btn btn-secondary p-2"
      >Abbrechen</a>
    </div>
  </b-form>
</template>

<script>
export default {
  name: 'UpdateRealm',
  props: {
    realm: {}
  },
  data () {
    return {
      form: {
        ldapBaseDn: '',
        name: '',
        email: '',
        adminGroup: null,
        adminGroupOptions: [
          {
            value: null,
            text: '----------'
          }
        ],
        defaultGroup: null,
        defaultGroupOptions: [
          {
            value: null,
            text: '----------'
          }
        ]
      }
    }
  },
  created () {
    this.form.name = this.realm.name
    this.form.email = this.realm.email
    this.form.ldapBaseDn = this.realm.ldap_base_dn
    this.form.name = this.realm.name
    this.form.name = this.realm.name
    this.form.name = this.realm.name
  }
}
</script>

<style scoped>

</style>
