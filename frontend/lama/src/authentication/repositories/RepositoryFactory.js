import AuthRepository from '@/authentication/repositories/authRepository'
import RealmsRepository from '@/realms/repositories/realmsRepository'
import RealmRepository from '@/realms/repositories/realmRepository'

class RepositoryFactory {
  constructor () {
    this.repositoryMap = {
      authentication: AuthRepository,
      realm: RealmRepository,
      realms: RealmsRepository
    }
  }

  get (id) {
    return this.repositoryMap[id]
  }
}

const instance = new RepositoryFactory()
Object.freeze(instance)
export default instance
