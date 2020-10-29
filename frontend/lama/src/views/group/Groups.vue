<template>
  <b-container>
    <headline title="Gruppen" />
    <b-row class="mb-0">
      <b-col
        cols="12"
        md="3"
      >
        <div class="floating-label-input-group">
          <input
            id="table-search-input"
            v-model="filter"
            class="form-control"
            type="search"
            placeholder="Suche"
          >
          <label
            for="table-search-input"
            class="pr-5"
          >Suche</label>
          <b-input-group-append>
            <b-button
              variant="danger"
              :disabled="!filter"
              @click="filter = ''"
            >
              <b-icon-x />
            </b-button>
          </b-input-group-append>
        </div>
      </b-col>
    </b-row>
    <b-row
      class="mb-2"
      align-h="between"
    >
      <b-col
        cols="12"
        md="3"
        class="mb-2"
      >
        <b-select
          v-model="perPage"
          :options="rowOptions"
          size="sm"
        />
      </b-col>
      <b-col
        cols="12"
        md="3"
        class="mb-2"
      >
        <b-pagination
          v-if="perPage && (rows - perPage) > 0"
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="realms-table"
          first-number
          size="sm"
          align="fill"
          class="mb-0"
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-table
          id="groups-table"
          hover
          :fields="fields"
          :items="groups"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          sort-by="realm.name"
          stacked="md"
          small
        >
          <template v-slot:cell(name)="data">
            <router-link :to="{name: 'Group', params: {realmId: realmId, groupDn: data.item.dn}}">
              {{ data.value }}
            </router-link>
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
  data () {
    return {
      realmId: -1,
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
        { key: 'members', label: 'Mitgliederzahl', formatter: 'getMemberCount', sortByFormatted: true, sortable: true }
      ]
    }
  },
  computed: {
    groups: function () {
      return this.$store.getters['groups/groups']
    },
    rows: function () {
      return this.$store.getters['groups/groups'].length
    }
  },
  watch: {
    '$route.params.realmId': function (realmId) {
      this.$store.dispatch('users/fetchGroups', { realmId: realmId })
    }
  },
  mounted () {
    const realmId = this.$route.params.realmId
    this.$store.dispatch('groups/fetchGroups', { realmId: realmId })
    this.realmId = realmId
  },
  methods: {
    getMemberCount (value, key, item) {
      const preparedString = value.replace(/'/g, '"')
      return JSON.parse(preparedString).length
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
