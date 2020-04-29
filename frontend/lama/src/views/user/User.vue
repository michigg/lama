<template>
  <b-container>
    <headline title="User"/>
    <b-row class="mb-0">
      <b-col cols="12" md="3">
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
// @ is an alias to /src
import Headline from '../../components/utils/Headline'

export default {
  name: 'Realms',
  components: { Headline },
  mounted () {
    const realmId = this.$route.params.realmId
    this.$store.dispatch('users/fetchUsers', { realmId: realmId })
  },
  data () {
    return {
      filter: null,
      perPage: 25,
      currentPage: 1,
      rowOptions: [
        { text: '25 Zeilen', value: 25 },
        { text: '50 Zeilen', value: 50 },
        { text: '100 Zeilen', value: 100 },
        { text: '----------', value: null }
      ],
      fields: [
        { key: 'user.username', label: 'Nutzername', sortable: true },
        { key: 'user.email', label: 'E-Mail', sortable: true },
        { key: 'user.first_name', label: 'Vorname', sortable: true },
        { key: 'user.last_name', abel: 'Nachname', sortable: true },
        { key: 'active', label: 'Aktiv', sortable: true },
        { key: 'user.last_login', label: 'Letzter Login', sortable: true },
        { key: 'user.deleted_user', label: 'Löschdatum', sortable: true }
      ]
    }
  },
  computed: {
    users: function () {
      return this.$store.getters['users/users']
    },
    rows: function () {
      return this.$store.getters['users/users'].length
    }
  }
}
</script>

<style scoped>
  .floating-label-input-group {
    display: -webkit-box !important;
    display: -ms-flexbox !important;
    display: flex !important;
  }

  .floating-label-input-group > .form-control {
    min-width: 0;
  }
</style>
