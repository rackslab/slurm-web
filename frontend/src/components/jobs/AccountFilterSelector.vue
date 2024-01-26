<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRuntimeStore } from '@/stores/runtime'
import {
  useGatewayAPI,
  type AccountDescription
} from '@/composables/GatewayAPI'
import { AuthenticationError, PermissionError } from '@/composables/HTTPErrors'
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/20/solid'

import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions
} from '@headlessui/vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const runtimeStore = useRuntimeStore()
const router = useRouter()
const gateway = useGatewayAPI()
const unable = ref(false)
const query = ref('')

const accounts: Ref<Array<AccountDescription>> = ref([])
const filteredAccounts = computed(() =>
  query.value === ''
    ? accounts.value
    : accounts.value.filter((account) => {
        return account.name.toLowerCase().includes(query.value.toLowerCase())
      })
)

function queryPlaceholder() {
  if (runtimeStore.jobs.filters.accounts.length == 0) {
    return 'Search account…'
  } else {
    return runtimeStore.jobs.filters.accounts.join(', ')
  }
}

function reportAuthenticationError(error: AuthenticationError) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportPermissionError(error: PermissionError) {
  runtimeStore.reportError(`Permission error: ${error.message}`)
  unable.value = true
}

function reportOtherError(error: Error) {
  runtimeStore.reportError(`Server error: ${error.message}`)
  unable.value = true
}

async function getAccounts() {
  try {
    unable.value = false
    accounts.value = await gateway.accounts(props.cluster)
  } catch (error: any) {
    if (error instanceof AuthenticationError) {
      reportAuthenticationError(error)
    } else if (error instanceof PermissionError) {
      reportPermissionError(error)
    } else {
      reportOtherError(error)
    }
  }
}

onMounted(() => {
  getAccounts()
})
</script>

<template>
  <div class="relative mt-2">
    <Combobox as="div" v-model="runtimeStore.jobs.filters.accounts" multiple>
      <ComboboxInput
        class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-slurmweb sm:text-sm sm:leading-6"
        @change="query = $event.target.value"
        :placeholder="queryPlaceholder()"
      />
      <ComboboxButton
        class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none"
      >
        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </ComboboxButton>

      <ComboboxOptions
        v-if="filteredAccounts.length > 0"
        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
      >
        <ComboboxOption
          v-for="account in filteredAccounts"
          :key="account.name"
          :value="account.name"
          as="template"
          v-slot="{ active, selected }"
        >
          <li
            :class="[
              'relative cursor-default select-none py-2 pl-3 pr-9',
              active ? 'bg-slurmweb text-white' : 'text-gray-900'
            ]"
          >
            <div class="flex">
              <span :class="['truncate', selected && 'font-semibold']">
                {{ account.name }}
              </span>
            </div>

            <span
              v-if="selected"
              :class="[
                'absolute inset-y-0 right-0 flex items-center pr-4',
                active ? 'text-white' : 'text-slurmweb'
              ]"
            >
              <CheckIcon class="h-5 w-5" aria-hidden="true" />
            </span>
          </li>
        </ComboboxOption>
      </ComboboxOptions>
    </Combobox>
  </div>
</template>
