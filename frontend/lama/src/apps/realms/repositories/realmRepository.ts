import { RealmEndpoint } from '@/apps/realms/api/lama'
import { RealmRepositoryException } from '@/apps/realms/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { Realm } from '@/apps/realms/models/realm'

export class RealmRepository {
  async getRealm (id: number) {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realm(id))
      return new Realm(
        response.data.realm.id,
        response.data.realm.name,
        response.data.realm.email,
        response.data.realm.ldap_base_dn,
        response.data.realm.admin_group,
        response.data.realm.default_group,
        response.data.user_count,
        response.data.group_count
      )
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  }

  async updateRealm (id: number, data: Realm) {
    try {
      const response = await httpClient.client.patch(RealmEndpoint.Realm(id))
      return new Realm(
        response.data.realm.id,
        response.data.realm.name,
        response.data.realm.email,
        response.data.realm.ldap_base_dn,
        response.data.realm.admin_group,
        response.data.realm.default_group,
        response.data.user_count,
        response.data.group_count
      )
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  }

  async deleteRealm (id: number) {
    try {
      const response = await httpClient.client.delete(RealmEndpoint.Realm(id))
      return new Realm(
        response.data.realm.id,
        response.data.realm.name,
        response.data.realm.email,
        response.data.realm.ldap_base_dn,
        response.data.realm.admin_group,
        response.data.realm.default_group,
        response.data.user_count,
        response.data.group_count
      )
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  }
}
