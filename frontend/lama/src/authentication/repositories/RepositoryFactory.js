import AuthRepository from '@/authentication/repositories/authRepository'
import RealmsRepository from '@/realms/repositories/realmsRepository'
import RealmRepository from '@/realms/repositories/realmRepository'

const repositories = {
  authentication: AuthRepository,
  realms: RealmsRepository,
  realm: RealmRepository
}

export const RepositoryFactory = {
  get: name => repositories[name]
}
