import { UserEndpoint } from '@/apps/users/api/lama'
import { UserRepositoryException } from '@/apps/users/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'

export default {
  async getUser (id) {
    try {
      const response = await httpClient.client.get(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  },
  async updateUser (id, data) {
    try {
      const response = await httpClient.client.patch(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  },
  async deleteUser (id) {
    try {
      const response = await httpClient.client.delete(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }
}
