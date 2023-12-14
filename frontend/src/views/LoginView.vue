<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import { useGatewayAPI, AuthenticationError } from '@/composables/GatewayAPI'

const gateway = useGatewayAPI()

const username: Ref<string | null> = ref(null)
const password: Ref<string | null> = ref(null)
const disableSubmission: Ref<boolean> = ref(false)
const highlightLogin: Ref<boolean> = ref(false)
const highlightPassword: Ref<boolean> = ref(false)
const shakeLoginButton: Ref<boolean> = ref(false)

const authStore = useAuthStore()
const runtimeStore = useRuntimeStore()

function reportAuthenticationError(message: string) {
  runtimeStore.reportError(`Authentication error: ${message}`)

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
    reportAuthenticationError('Username is required')
    setTrueFor(highlightLogin, 2000)
    return
  }
  if (password.value == null || password.value == '') {
    reportAuthenticationError('Password is required')
    setTrueFor(highlightPassword, 2000)
    return
  }
  try {
    let response = await gateway.login({ user: username.value, password: password.value })
    disableSubmission.value = true
    authStore.login(response.token, username.value, response.fullname, response.groups)
  } catch (error: any) {
    if (error instanceof AuthenticationError) {
      reportAuthenticationError(error.message)
    } else {
      runtimeStore.reportError(`Other error: ${error.message}`)
    }
  }
}
</script>

<template>
  <main>
    <section class="bg-slurmweb-light dark:bg-gray-900">
      <div class="flex flex-col items-center justify-center px-6 py-4 mx-auto h-screen lg:py-0">
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
                  class="transition-colors border border-gray-300 text-gray-900 placeholder-gray-300 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-slurmweb block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
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
                  class="border border-gray-300 text-gray-900 placeholder-gray-300 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-slurmweb block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  :class="{ 'bg-gray-50': !highlightPassword, 'bg-red-200': highlightPassword }"
                  placeholder="••••••••"
                />
              </div>
              <button
                type="submit"
                :disabled="disableSubmission"
                class="w-full text-white bg-slurmweb hover:bg-slurmweb-dark disabled:bg-slate-300 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
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
