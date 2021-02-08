// TODO: automatic set enpoint
const BaseUrl = 'http://localhost:8888/api/v1'
export const UserEndpoint = {
  User: (realmId, userDn) => `${BaseUrl}/realm/${realmId}/user/${userDn}/`,
  Users: realmId => `${BaseUrl}/realm/${realmId}/user/`
}
