<template>
  <b-container v-if="!loading">
    <headline :title="`Bereich ${realm.name}`" />
    <small>
      <a
        v-if="$can('delete', 'Realm')"
        href="#"
        class="h5 realm-delete-link"
      >
        <b-icon-trash-fill />
        <span class="d-none d-md-inline-block">Bereich löschen</span></a>
    </small>
    <b-row
      v-if="!isEditMode"
      class="neo-morph"
    >
      <b-col>
        <realm-detail :realm="realm" />
        <div class="d-flex mt-3">
          <button
            v-if="$can('change', 'Realm')"
            href="#"
            class="btn btn-primary mr-auto p-2"
            @click="isEditMode = !isEditMode"
          >
            Bereichsinformationen anpassen
          </button>
          <a
            v-if="realm.email && $can('change', 'Realm')"
            href="#"
            class="btn btn-secondary p-2"
          >
            Test Mail
          </a>
        </div>
      </b-col>
    </b-row>
    <b-row
      v-else
      class="neo-morph"
    >
      <b-col>
        <update-realm :realm="realm" />
      </b-col>
    </b-row>
  </b-container>
  <b-container v-else>
    <b-row>
      <b-col>
        <loading-info />
      </b-col>
    </b-row>
  </b-container>
</template>

<script lang="ts">
// @ is an alias to /src
import Headline from '../../../components/utils/Headline.vue'
import LoadingInfo from '../../../components/utils/LoadingInfo.vue'
import RealmDetail from '../components/RealmDetail.vue'
import UpdateRealm from '../components/UpdateRealm.vue'
import { useStore } from '@/store'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Realm',
  components: {
    UpdateRealm,
    RealmDetail,
    LoadingInfo,
    Headline
  },
  data () {
    return {
      isEditMode: false
    }
  },
  computed: {
    realm: function () {
      const store = useStore()
      return store.getters['realm/realm']
    },
    loading: function () {
      const store = useStore()
      return store.getters['realm/loading']
    }
  },
  watch: {
    '$route.params.realmId': function (realmId) {
      const store = useStore()
      store.dispatch('realm/fetchRealm', { realmId: realmId })
    }
  },
  mounted () {
    const realmId = this.$route.params.realmId
    const store = useStore()
    store.dispatch('realm/fetchRealm', { realmId: realmId })
  }
})
</script>
