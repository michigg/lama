<template>
  <b-container v-if="!loading">
    <headline :title="`Bereich ${realm.name}`"/>
    <small>
      <a v-if="$can('delete', 'Realm')" href="#" class="h5 realm-delete-link">
        <b-icon-trash-fill/>
        <span class="d-none d-md-inline-block">Bereich löschen</span></a>
    </small>
    <b-row>
      <b-col>
        <realm-detail :realm="realm"/>
        <div class="d-flex mt-3">
          <a v-if="$can('change', 'Realm')" href="#" class="btn btn-primary mr-auto p-2">
            Bereichsinformationen anpassen
          </a>
          <a v-if="realm.email && $can('change', 'Realm')" href="#" class="btn btn-secondary p-2">
            Test Mail
          </a>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
       <update-realm></update-realm>
      </b-col>
    </b-row>
  </b-container>
  <b-container v-else>
    <b-row>
      <b-col>
        <loading-info/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
// @ is an alias to /src
import Headline from '../../components/utils/Headline'
import LoadingInfo from '../../components/utils/LoadingInfo'
import RealmDetail from '../../components/realm/RealmDetail'
import UpdateRealm from '../../components/realm/UpdateRealm'

export default {
  name: 'Realm',
  components: {
    UpdateRealm,
    RealmDetail,
    LoadingInfo,
    Headline
  },
  mounted () {
    const realmId = this.$route.params.realmId
    this.$store.dispatch('realm/fetchRealm', { realmId: realmId })
  },
  computed: {
    realm: function () {
      return this.$store.getters['realm/realm']
    },
    loading: function () {
      return this.$store.getters['realm/loading']
    }
  },
  watch: {
    '$route.params.realmId': function (realmId) {
      this.$store.dispatch('realm/fetchRealm', { realmId: realmId })
    }
  }
}
</script>
