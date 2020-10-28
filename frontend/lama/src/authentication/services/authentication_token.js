const AuthTokenService = (
  function () {
    const ACCESS_TOKEN_KEY = 'access_token'
    const REFRESH_TOKEN_KEY = 'refresh_token'

    function _setToken (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token.access)
      localStorage.setItem(REFRESH_TOKEN_KEY, token.refresh)
    }

    function _getAccessToken () {
      return localStorage.getItem(ACCESS_TOKEN_KEY)
    }

    function _getRefreshToken () {
      return localStorage.getItem(REFRESH_TOKEN_KEY)
    }

    function _clearToken () {
      localStorage.removeItem(ACCESS_TOKEN_KEY)
      localStorage.removeItem(REFRESH_TOKEN_KEY)
    }

    return {
      setToken: _setToken,
      getAccessToken: _getAccessToken,
      getRefreshToken: _getRefreshToken,
      clearToken: _clearToken
    }
  })()
export default AuthTokenService
