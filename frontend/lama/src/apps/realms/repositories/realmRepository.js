import { RealmEndpoint } from '@/realms/api/lama'
import { RealmReposioryException } from '@/realms/exceptions/repository'
import httpClient from '@/authentication/clients/httpClient'

export default {
  async getRealm (id) {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  },
  async updateRealm (id, data) {
    try {
      const response = await httpClient.client.patch(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  },
  async deleteRealm (id) {
    try {
      const response = await httpClient.client.delete(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  }
}
