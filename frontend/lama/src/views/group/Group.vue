<template>
  <b-container>
    <headline :title="`Gruppe ${group.name}`" />
    <b-row class="mb-0">
      <b-col cols="12">
        <b-list-group class="w-100 mb-3">
          <b-list-group-item>Ldap Domain: <span class="float-right">{{ group.dn }}</span></b-list-group-item>
          <b-list-group-item v-if="group.description">
            Beschreibung: <span class="float-right">{{ group.description }}</span>
          </b-list-group-item>
        </b-list-group>
        <h3>Mitglieder</h3>
        <!--        TODO: render users table-->
        <div class="d-flex mt-3">
          <!--          TODO: group update link-->
          <a
            href="#"
            class="btn btn-primary mr-auto p-2"
          >Gruppe bearbeiten</a>
          <!--          TODO: group delete action-->
          <a
            href="#"
            class="btn btn-danger p-2"
          ><span class="d-sm-none d-md-inline-block">Gruppe löschen</span></a>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
// @ is an alias to /src
import Headline from '../../components/utils/Headline'

export default {
  name: 'Group',
  components: { Headline },
  data () {
    return {}
  },
  computed: {
    group: function () {
      return this.$store.getters['group/group']
    }
  },
  mounted () {
    const realmId = this.$route.params.realmId
    const groupDn = this.$route.params.groupDn
    this.$store.dispatch('group/fetchGroup', { realmId: realmId, groupDn: groupDn })
  }
}
</script>

<style scoped>
</style>
