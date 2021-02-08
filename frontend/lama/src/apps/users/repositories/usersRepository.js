import { RealmEndpoint } from '@/apps/realms/api/lama'
import { RealmRepositoryException } from '@/apps/realms/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'

export default {
  async getRealms () {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realms)
      return response.data.results
    } catch (error) {
      throw new RealmReposioryException(error.message)
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
      throw new RealmReposioryException(error.message)
    }
  }
}
