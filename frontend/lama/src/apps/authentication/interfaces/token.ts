import { User } from '@/apps/authentication/models/user'
import { ClaimRawRule, RawRuleFrom } from '@casl/ability'

export interface RawTokenInterface {
  accessToken: string
  refreshToken: string
}

export interface ApiTokenUserInterface {
  username: string
  email: string
  rules: Array<any>
}

export interface ApiTokenInterface {
  user: ApiTokenUserInterface
  exp: string
}
