<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useHttp } from '@/plugins/http'
import { useAuthStore } from '@/stores/auth'

const http = useHttp()
const username: Ref<string | null> = ref(null)
const password: Ref<string | null> = ref(null)
const authentication_error: Ref<string | null> = ref(null)
const authentication_succesful: Ref<boolean> = ref(false)
const submit_disabled: Ref<boolean> = ref(false)

const authStore = useAuthStore()

async function submitLogin() {
  if (username.value == null) {
    authentication_error.value = 'Username is required'
    return
  }
  if (password.value == null) {
    authentication_error.value = 'Password is required'
    return
  }
  try {
    let response = await http.post('/login', { user: username.value, password: password.value })
    authentication_error.value = null
    authentication_succesful.value = true
    submit_disabled.value = true
    authStore.login(response.data.token)
  } catch (error: any) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    if (error.response) {
      if (error.response.status == 403) {
        authentication_error.value = error.response.data.error
      }
      console.log('errors: ' + error.response.status + ' ' + error.response.data.error)
    } else if (error.request) {
      // The request was made but no response was received `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request)
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message)
    }
    console.log(error.config)
  }
}
</script>

<template>
  <main>
    <section class="bg-gray-50 dark:bg-gray-900">
      <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div
          class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
        >
          <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1
              class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
            >
              Sign in to your account
            </h1>
            <form class="space-y-4 md:space-y-6" action="#" @submit.prevent="submitLogin">
              <div>
                <label
                  for="user"
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >Login</label
                >
                <input
                  name="user"
                  id="user"
                  v-model="username"
                  class="login"
                  placeholder="Username"
                />
              </div>
              <div>
                <label
                  for="password"
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >Password</label
                >
                <input
                  type="password"
                  name="password"
                  id="password"
                  v-model="password"
                  class="login"
                  placeholder="••••••••"
                />
              </div>
              <button
                type="submit"
                :disabled="submit_disabled"
                class="w-full text-white bg-sky-500 hover:bg-sky-600 disabled:bg-slate-300 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
              >
                Sign in
              </button>
            </form>
            <div v-show="authentication_error" class="bg-red-200">{{ authentication_error }}</div>
            <div v-show="authentication_succesful" class="bg-emerald-200">
              Authentication is succesful
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
