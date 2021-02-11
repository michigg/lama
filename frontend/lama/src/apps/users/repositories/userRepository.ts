import { UserEndpoint } from '@/apps/users/api/lama'
import { UserRepositoryException } from '@/apps/users/exceptions/repository'
import httpClient from '@/apps/authentication/clients/httpClient'
import { User } from '@/apps/users/models/user'

export class UserRepository {
  async getUser (realmId: number, userDn: string) {
    try {
      const response = await httpClient.client.get(UserEndpoint.User(realmId, userDn))
      // TODO: convert to User
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }

  async updateUser (realmId: number, userDn: string, user: User) {
    try {
      const response = await httpClient.client.patch(UserEndpoint.User(realmId, userDn))
      // TODO: convert to User
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }

  async deleteUser (realmId: number, userDn: string) {
    try {
      const response = await httpClient.client.delete(UserEndpoint.User(realmId, userDn))
      // TODO: convert to User
      return response.data
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }
}
