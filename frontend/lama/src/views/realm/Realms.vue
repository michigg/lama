<template>
  <b-container>
    <headline title="Bereiche"/>
    <b-row>
      <b-col>
        <b-table
          id="voucher-table"
          hover
          :fields="fields"
          :items="realms"
          :filter="filter"
          :filterIncludedFields="filterOn"
          :per-page="perPage"
          :current-page="currentPage"
          sort-by="code"
          stacked="md"
          small
        >
          <template v-slot:cell(realm.name)="data">
            <router-link :to="{name: 'Realm', params: {realmId: data.item.realm.id}}">{{data.value}}</router-link>
          </template>
          <template v-slot:cell(realm.email)="data">
            <div v-if="data.value" class="text-center">
              <a :href="`mailto:${data.value}`">{{data.value}}</a>
            </div>
            <div v-else class="text-danger text-center">
              <b-icon-exclamation-triangle-fill/>
            </div>
          </template>
        </b-table>
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
    this.$store.dispatch('realms/fetchRealms')
  },
  data () {
    return {
      filter: null,
      filterOn: ['code'],
      perPage: 10,
      currentPage: 1,
      rowOptions: [
        { text: '25 Zeilen', value: 25 },
        { text: '50 Zeilen', value: 50 },
        { text: '100 Zeilen', value: 100 },
        { text: '----------', value: null }
      ],
      fields: [
        { key: 'realm.name', label: 'Bereichsname', sortable: true },
        { key: 'realm.ldap_base_dn', label: 'Ldap Basis DN', sortable: true },
        { key: 'realm.email', label: 'Mailadresse', sortable: true },
        { key: 'realm.admin_group', label: 'Admingruppe', sortable: true },
        { key: 'realm.default_group', label: 'Defaultgruppe', sortable: true },
        { key: 'user_count', label: 'Nutzeranzahl', sortable: true },
        { key: 'group_count', label: 'Gruppenanzahl', sortable: true }
      ]
    }
  },
  computed: {
    realms: function () {
      return this.$store.getters['realms/realms']
    }
  }
}
</script>
