import { RealmEndpoint } from '@/apps/realms/api/lama'
import { RealmRepositoryException } from '@/apps/realms/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { Realm } from '@/apps/realms/models/realm'

export default {
  async getRealms () {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realms)
      console.log('Realms', response.data.results)
      const realms = response.data.results.map(rawRealm => {
        return new Realm(rawRealm.realm.id,
          rawRealm.realm.name,
          rawRealm.realm.email,
          rawRealm.realm.ldap_base_dn,
          rawRealm.realm.admin_group,
          rawRealm.realm.default_group,
          rawRealm.user_count,
          rawRealm.group_count
        )
      })
      console.log('Realms', realms)
      return realms
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  },
  async addRealm (name, ldapBaseDn) {
    try {
      const response = await httpClient.client.post(RealmEndpoint.Realms, {
        name: name,
        ldap_base_dn: ldapBaseDn
      })
      const data = response.data
      return {
        name: data.name,
        ldapBaseDn: data.ldap_base_dn
      }
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  }
}
