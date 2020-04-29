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
          id="users-table"
          hover
          :fields="fields"
          :items="users"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          sort-by="realm.name"
          stacked="md"
          small
        >
          <template v-slot:cell(user.username)="data">
            <router-link :to="{name: 'User', params: {realmId: realmId, userDn: data.item.user.dn}}">{{data.value}}</router-link>
          </template>
          <template v-slot:cell(user.email)="data">
            <div class="text-center">
              <a :href="`mailto:${data.value}`">{{data.value}}</a>
            </div>
          </template>
           <template v-slot:cell(active)="data">
            <div v-if="data.value" class="text-center text-success">
              <b-icon-check-circle/>
            </div>
             <div v-else class="text-center text-warning">
              <b-icon-x-circle-fill/>
            </div>
          </template>
          <template v-slot:cell(user.last_login)="data">
            <div v-if="data.value" class="text-center">
<!--              TODO: filter date -->
              {{data.value}}
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
    const realmId = this.$route.params.realmId
    this.$store.dispatch('users/fetchUsers', { realmId: realmId })
    this.realmId = realmId
  },
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
