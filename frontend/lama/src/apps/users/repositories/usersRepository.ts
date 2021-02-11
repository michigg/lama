import httpClient from '@/apps/authentication/clients/httpClient'
import { UserEndpoint } from '@/apps/users/api/lama'
import { UserRepositoryException } from '@/apps/users/exceptions/repository'
import { User } from '@/apps/users/models/user'

export class UsersRepository {
  async getUsers (realmId: number) {
    try {
      const response = await httpClient.client.get(UserEndpoint.Users(realmId))
      // TODO: convert to User
      return response.data.results
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }

  async addUser (realmId: number, user: User) {
    try {
      const response = await httpClient.client.post(UserEndpoint.Users(realmId), user)
      // TODO: convert to User
      const data = response.data
      return {
        name: data.name,
        ldapBaseDn: data.ldap_base_dn
      }
    } catch (error) {
      throw new UserRepositoryException(error.message)
    }
  }
}
