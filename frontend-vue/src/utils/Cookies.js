import Cookies from 'js-cookie'
import VueJwtDecode from 'vue-jwt-decode'

const TOKEN_NAME = 'token';

class Utils {
  static saveToken(token) {
    if (token) {
      let decodedToken= VueJwtDecode.decode(token.access)
      Cookies.set(TOKEN_NAME,  token.access)
      return {decodedToken, token}
    }
  }

  static setToken(token) {
    if (token) {
      let decodedToken= VueJwtDecode.decode(token)
      Cookies.set(TOKEN_NAME,  token)
      return {decodedToken, token}
    }
  }

  static getToken() {
    return Cookies.get(TOKEN_NAME)
  }

  static removeToken() {
    Cookies.remove(TOKEN_NAME)
  }

  static authTokenExists() {
    return !!this.getToken(TOKEN_NAME)
  }

  static decodeAuthToken() {
    const token = this.getToken(TOKEN_NAME)
    return VueJwtDecode.decode(token)
  }
}

export default Utils;