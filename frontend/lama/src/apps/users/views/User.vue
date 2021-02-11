<template>
  <b-container>
    <headline :title="`Nutzer ${user.user.username}`" />
    <b-row class="mb-0">
      <b-col
        cols="12"
        class="neo-morph p-3"
      >
        <b-list-group class="text-left">
          <b-list-group-item>Ldap Domain: <span class="float-right">{{ user.user.dn }}</span></b-list-group-item>
          <b-list-group-item>
            Anzeigename: <span
              v-if="user.user.display_name"
              class="float-right"
            >{{ user.user.display_name }}</span>
            <span
              v-else
              class="float-right text-warning"
            >Noch nicht generiert</span>
          </b-list-group-item>
          <b-list-group-item v-if="user.user.first_name">
            Vorname: <span
              class="float-right"
            >{{ user.user.first_name }}</span>
          </b-list-group-item>
          <b-list-group-item v-if="user.user.last_name">
            Nachname: <span
              class="float-right"
            >{{ user.user.last_name }}</span>
          </b-list-group-item>
          <b-list-group-item>Email: <span class="float-right">{{ user.user.email }}</span></b-list-group-item>
          <!--           TODO: add password reset href-->
          <b-list-group-item>
            Passwort: <a
              href="#"
              class="float-right"
            >Nutzerpasswort zurücksetzen</a>
          </b-list-group-item>
          <b-list-group-item v-if="user.user.phone">
            Telefon: <span class="float-right">{{ user.user.phone }}</span>
          </b-list-group-item>
          <b-list-group-item v-if="user.user.mobile_phone">
            Mobiltelefon: <span class="float-right">{{ user.user.mobile_phone }}</span>
          </b-list-group-item>
          <b-list-group-item>
            Gruppen:
            <span
              v-if="user.groups.length !== 0"
              class="float-right"
            >
              <!--                TODO: add group detail link-->
              <router-link
                v-for="group in user.groups"
                :key="group.dn"
                :to="{name: 'Group', params: {realmId: realmId, groupDn: group.dn}}"
                class="badge badge-secondary p-1"
              >
                {{ group.name }}
              </router-link>
            </span>
            <span
              v-else
              class="text-warning"
            >Keine zugewiesen</span>
            <!--              TODO: add users gorup update view link-->
            <a
              v-if="!user.deleted_user && $can('change', 'Ldapuser')"
              href="#"
            >Gruppen zuweisen</a>
          </b-list-group-item>
          <b-list-group-item>
            Zuletzt eingeloggt:
            <span
              v-if="user.user.last_login"
              class="float-right"
            >{{ user.user.last_login }}</span>
            <span
              v-else
              class="float-right"
            >Kein login vorhanden<span
              class="d-none"
            >+</span></span>
          </b-list-group-item>
          <b-list-group-item
            v-if="user.deleted_user"
            class="text-danger"
          >
            <span>Löschvorgang: {{ user.deleted_user.deletion_date }}</span>
            <span class="float-right">
              <!--                  TODO: users direkt delete link/action-->
              <a
                v-if="$can('delete', 'Ldapuser')"
                class="btn btn-danger"
                href="#"
              >Sofort löschen</a>
              <!--             TODO: users delete cancel     -->
              <a
                v-if="$can('change', 'Ldapuser')"
                class="btn btn-outline-dark"
                href="#"
              >Löschvorgang abbrechen</a></span>
          </b-list-group-item>
        </b-list-group>
        <div class="d-flex mt-3">
          <!--          TODO: users update link-->
          <a
            v-if="!user.deleted_user && $can('change', 'Ldapuser')"
            href="#"
            class="btn btn-primary mr-auto p-2"
          >Nutzer
            bearbeiten</a>
          <!--TODO: users resend welcome mail-->
          <a
            v-if="!user.user.last_login && $can('change', 'Ldapuser')"
            href="#"
            class="btn btn-secondary p-2 mr-2"
          >Wilkommensmail
            erneut senden</a>
          <!--TODO: users delete confirm link-->
          <a
            v-if="$can('delete', 'Ldapuser')"
            href="#"
            class="btn btn-danger p-2"
          >Nutzer löschen</a>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script lang="ts">
// @ is an alias to /src
import Headline from '@/components/utils/Headline.vue'
import { defineComponent } from 'vue'
import { useStore } from '@/store'

export default defineComponent({
  name: 'User',
  components: { Headline },
  data () {
    return {
      realmId: -1
    }
  },
  computed: {
    user: function () {
      const store = useStore()
      return store.getters['user/user']
    }
  },
  mounted () {
    const realmId = this.$route.params.realmId
    const userDn = this.$route.params.userDn
    const store = useStore()
    store.dispatch('user/fetchUser', {
      realmId: realmId,
      userDn: userDn
    })
    this.realmId = +realmId
  }
})
</script>

<style scoped>
</style>
