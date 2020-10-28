import axios from 'axios'
import { RealmEndpoint } from '@/realms/api/lama'
import { RealmReposioryException } from '@/realms/exceptions/repository'

export default {
  async getRealm (id) {
    try {
      const response = await axios.get(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  },
  async updateRealm (id, data) {
    try {
      const response = await axios.patch(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  },
  async deleteRealm (id) {
    try {
      const response = await axios.delete(RealmEndpoint.Realm(id))
      return response.data
    } catch (error) {
      throw new RealmReposioryException(error.message)
    }
  }
}
