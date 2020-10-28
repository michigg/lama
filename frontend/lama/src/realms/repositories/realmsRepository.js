import axios from 'axios'
import { RealmEndpoint } from '@/realms/api/lama'
import { RealmReposioryException } from '@/realms/exceptions/repository'

export default {
  async getRealms () {
    try {
      const response = await axios.get(RealmEndpoint.Realms)
      return response.data.results
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  },
  async addRealm (name, ldapBaseDn) {
    try {
      const response = await axios.post(RealmEndpoint.Realms, {
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
