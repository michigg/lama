<template>
  <b-container>
    <headline title="Bereiche"/>
    <b-row class="mb-0">
      <b-col cols="12" md="3">
        <div class="floating-label-input-group">
          <input
            class="form-control"
            v-model="filter"
            type="search"
            id="table-search-input"
            placeholder="Suche"
          />
          <label for="table-search-input" class="pr-5">Suche</label>
          <b-input-group-append>
            <b-button variant="danger" :disabled="!filter" @click="filter = ''">
              <b-icon-x/>
            </b-button>
          </b-input-group-append>
        </div>
      </b-col>
    </b-row>
    <b-row class="mb-2" align-h="between">
      <b-col cols="12" md="3" class="mb-2">
        <b-select v-model="perPage" :options="rowOptions" size="sm"/>
      </b-col>
      <b-col cols="12" md="3" class="mb-2">
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
          id="realms-table"
          hover
          :fields="fields"
          :items="realms"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          sort-by="realm.name"
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
          <template v-slot:cell(realm.admin_group)="data">
            <div v-if="data.value" class="text-center">
              <span>{{data.value}}</span>
            </div>
            <div v-else class="text-warning text-center">
              <b-icon-exclamation-triangle-fill/>
            </div>
          </template>
          <template v-slot:cell(realm.default_group)="data">
            <div v-if="data.value" class="text-center">
              <span>{{data.value}}</span>
            </div>
            <div v-else class="text-warning text-center">
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
      perPage: 25,
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
        { key: 'realm.admin_group', abel: 'Admingruppe', sortable: true },
        { key: 'realm.default_group', label: 'Defaultgruppe', sortable: true },
        { key: 'user_count', label: 'Nutzeranzahl', sortable: true },
        { key: 'group_count', label: 'Gruppenanzahl', sortable: true }
      ]
    }
  },
  computed: {
    realms: function () {
      return this.$store.getters['realms/realms']
    },
    rows: function () {
      return this.$store.getters['realms/realms'].length
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
