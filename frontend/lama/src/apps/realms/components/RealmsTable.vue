<template>
  <div>
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
            data-test="realms-table-search-input"
          >
          <label
            for="table-search-input"
            class="pr-5"
          >Suche</label>
          <b-input-group-append>
            <b-button
              variant="danger"
              :disabled="!filter"
              data-test="realms-table-search-input-clear-button"
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
          data-test="realms-table-page-count-selector"
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
          data-test="realms-table-pagination"
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
          data-test="realms-table"
        >
          <template #cell(name)="data">
            <router-link :to="{name: 'Realm', params: {realmId: data.item.id}}">
              {{ data.value }}
            </router-link>
          </template>
          <template #cell(adminGroup)="data">
            <div
              v-if="data.value"
              class="text-center"
            >
              <span>{{ data.value }}</span>
            </div>
            <div
              v-else
              class="text-warning text-center"
            >
              <b-icon-exclamation-triangle-fill />
            </div>
          </template>
          <template #cell(defaultGroup)="data">
            <div
              v-if="data.value"
              class="text-center"
            >
              <span>{{ data.value }}</span>
            </div>
            <div
              v-else
              class="text-warning text-center"
            >
              <b-icon-exclamation-triangle-fill />
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { useStore } from '@/store'

export default {
  name: 'RealmsTable',
  data () {
    return {
      filter: null,
      perPage: 25,
      currentPage: 1,
      rowOptions: [
        {
          text: '25 Zeilen',
          value: 25
        },
        {
          text: '50 Zeilen',
          value: 50
        },
        {
          text: '100 Zeilen',
          value: 100
        },
        {
          text: '----------',
          value: null
        }
      ],
      fields: [
        {
          key: 'name',
          label: 'Bereichsname',
          sortable: true
        },
        {
          key: 'ldapBaseDn',
          label: 'Ldap Basis DN',
          sortable: true
        },
        {
          key: 'adminGroup',
          label: 'Admingruppe',
          sortable: true
        },
        {
          key: 'defaultGroup',
          label: 'Defaultgruppe',
          sortable: true
        },
        {
          key: 'userCount',
          label: 'Nutzeranzahl',
          sortable: true
        },
        {
          key: 'groupCount',
          label: 'Gruppenanzahl',
          sortable: true
        }
      ]
    }
  },
  computed: {
    realms: function () {
      const store = useStore()
      return store.getters['realms/realms']
    },
    rows: function () {
      const store = useStore()
      return store.getters['realms/realms'].length
    }
  }
}
</script>

<style scoped>

</style>
