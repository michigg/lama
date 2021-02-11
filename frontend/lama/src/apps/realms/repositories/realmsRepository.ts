import { RealmEndpoint } from '@/apps/realms/api/lama'
import { RealmRepositoryException } from '@/apps/realms/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { Realm } from '@/apps/realms/models/realm'

interface RawRealm {
  realm: {
    id: number
    name: string
    email: string
    // eslint-disable-next-line camelcase
    ldap_base_dn: string
    // eslint-disable-next-line camelcase
    admin_group: object
    // eslint-disable-next-line camelcase
    default_group: object
  }
  // eslint-disable-next-line camelcase
  user_count: number
  // eslint-disable-next-line camelcase
  group_count: number
}

export class RealmsRepository {
  async getRealms () {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realms)
      console.log('Realms', response.data.results)
      const realms = response.data.results.map((rawRealm: RawRealm) => {
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
  }

  async addRealm (name: string, ldapBaseDn: string) {
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
