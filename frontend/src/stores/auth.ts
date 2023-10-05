import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token: Ref<string | null> = ref(localStorage.getItem('token'))
  const returnUrl: Ref<string | null> = ref(null)

  function login(_token: string) {
    // update pinia state
    token.value = _token

    // store user details and jwt in local storage to keep user logged in between page refreshes
    localStorage.setItem('token', _token)

    // redirect to previous url or default to home page
    router.push(returnUrl.value || '/')
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  return { token, returnUrl, login, logout }
})
