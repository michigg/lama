const BaseUrl = 'http://localhost:8888/api'.concat('/auth')

export const AuthenticationEnpoint = {
  Token: BaseUrl + '/token/',
  RefreshToken: BaseUrl + '/token/refresh/'
}
