<template>
  <b-container>
    <headline title="Gruppe"/>
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
    this.$store.dispatch('groups/fetchGroups', { realmId: realmId })
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
        { key: 'name', label: 'Name', sortable: true },
        { key: 'dn', label: 'Ldap Domain', sortable: true },
        { key: 'members', label: 'Mitgliederzahl', sortable: true }
      ]
    }
  },
  computed: {
    realms: function () {
      return this.$store.getters['groups/groups']
    },
    rows: function () {
      return this.$store.getters['groups/groups'].length
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
