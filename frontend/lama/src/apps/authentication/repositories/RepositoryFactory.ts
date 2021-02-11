import AuthRepository from '@/apps/authentication/repositories/authRepository'
import { UserRepository } from '@/apps/users/repositories/userRepository'
import { UsersRepository } from '@/apps/users/repositories/usersRepository'
import { RealmRepository } from '@/apps/realms/repositories/realmRepository'
import { RealmsRepository } from '@/apps/realms/repositories/realmsRepository'

class RepositoryFactory {
  private readonly repositoryMap: Record<string, any>
  constructor () {
    this.repositoryMap = {
      authentication: AuthRepository,
      realm: new RealmRepository(),
      realms: new RealmsRepository(),
      users: new UsersRepository(),
      user: new UserRepository()
    }
  }

  get (id: string) {
    return this.repositoryMap[id]
  }
}

const instance = new RepositoryFactory()
Object.freeze(instance)
export default instance
