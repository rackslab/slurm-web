<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useHttp } from '@/plugins/http'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import { useGatewayAPI } from '@/composables/GatewayAPI'
//import Logo from '@/assets/logo/bitmaps/slurm-web_medium.png'

const http = useHttp()
const gateway = useGatewayAPI(http)

const username: Ref<string | null> = ref(null)
const password: Ref<string | null> = ref(null)
const disableSubmission: Ref<boolean> = ref(false)
const highlightLogin: Ref<boolean> = ref(false)
const highlightPassword: Ref<boolean> = ref(false)
const shakeLoginButton: Ref<boolean> = ref(false)

const authStore = useAuthStore()
const runtimeStore = useRuntimeStore()

function reportLoginError(message: string) {
  runtimeStore.reportError(message)
  setTrueFor(shakeLoginButton, 300)
}

function setTrueFor(reference: Ref<boolean>, timeout: number) {
  reference.value = true
  setTimeout(() => {
    reference.value = false
  }, timeout)
}

async function submitLogin() {
  if (username.value == null || username.value == '') {
    reportLoginError('Username is required')
    setTrueFor(highlightLogin, 2000)
    return
  }
  if (password.value == null || password.value == '') {
    reportLoginError('Password is required')
    setTrueFor(highlightPassword, 2000)
    return
  }
  try {
    let response = await gateway.login({ user: username.value, password: password.value })
    disableSubmission.value = true
    authStore.login(response.token)
    runtimeStore.availableClusters = []
    response.clusters.forEach((element) => {
      runtimeStore.addCluster(element)
    })
  } catch (error: any) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    if (error.response) {
      if (error.response.status == 403) {
        reportLoginError(`${error.response.data.name}: ${error.response.data.description}`)
      }
      console.log('errors: ' + error.response.status + ' ' + error.response.data.error)
    } else if (error.request) {
      // The request was made but no response was received `error.request` is an
      // instance of XMLHttpRequest in the browser and an instance of http.ClientRequest
      // in node.js
      console.log(error.request)
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message)
    }
    console.log(error.config)
    return
  }
}
</script>

<template>
  <main>
    <section class="bg-gray-50 dark:bg-gray-900">
      <div class="flex flex-col items-center justify-center px-6 py-4 mx-auto md:h-screen lg:py-0">
        <div
          class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
        >
          <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <img src="/logo/bitmaps/slurm-web_bgwhite_small.png" class="mb-8 m-auto" />
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
                  class="transition-colors border border-gray-300 text-gray-900 placeholder-gray-300 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-200 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  :class="{ 'bg-gray-50': !highlightLogin, 'bg-red-200': highlightLogin }"
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
                  class="border border-gray-300 text-gray-900 placeholder-gray-300 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-200 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  :class="{ 'bg-gray-50': !highlightPassword, 'bg-red-200': highlightPassword }"
                  placeholder="••••••••"
                />
              </div>
              <button
                type="submit"
                :disabled="disableSubmission"
                class="w-full text-white bg-sky-500 hover:bg-sky-600 disabled:bg-slate-300 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
                :class="{ 'animate-horizontal-shake': shakeLoginButton }"
              >
                Sign in
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
