import { RealmEndpoint } from '@/apps/realms/api/lama'
import { RealmRepositoryException } from '@/apps/realms/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { Realm } from '@/apps/realms/models/realm'

export default {
  async getRealm (id) {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realm(id))
      return new Realm(...response.data)
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  },
  async updateRealm (id, data) {
    try {
      const response = await httpClient.client.patch(RealmEndpoint.Realm(id))
      return new Realm(...response.data)
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  },
  async deleteRealm (id) {
    try {
      const response = await httpClient.client.delete(RealmEndpoint.Realm(id))
      return new Realm(...response.data)
    } catch (error) {
      throw new RealmRepositoryException(error.message)
    }
  }
}
