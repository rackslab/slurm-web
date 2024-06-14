<!--
  Copyright (c) 2023-2024 Rackslab

  This file is part of Slurm-web.

  SPDX-License-Identifier: GPL-3.0-or-later
-->

<script setup lang="ts">
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'
import { ChevronLeftIcon } from '@heroicons/vue/20/solid'
import { useClusterDataPoller } from '@/composables/DataPoller'
import type { Template } from '@/composables/GatewayAPI'
import { ref, onMounted, watch } from 'vue'

const { data } = useClusterDataPoller<Template[]>('templates', 5000)

const templateTitle = ref()
const templateDescription = ref()

function getSelectedTemplate() {
  if (data.value) {
    data.value.forEach((template) => {
      if (template.id == props.idTemplate) {
        templateTitle.value = template.name
        templateDescription.value = template.description
      }
    })
  }
}

const props = defineProps({
  cluster: {
    type: String,
    required: true
  },
  idTemplate: {
    type: Number
  }
})
watch([() => props.idTemplate, data], getSelectedTemplate)

onMounted(() => {
  getSelectedTemplate()
})
</script>

<template>
  <ClusterMainLayout :cluster="props.cluster">
    <router-link :to="{ name: 'submit-new-job' }"
      ><button
        type="button"
        class="mb-16 mt-8 inline-flex items-center gap-x-2 rounded-md bg-slurmweb px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slurmweb-dark focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slurmweb-dark"
      >
        <ChevronLeftIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
        Back to templates
      </button></router-link
    >

    <div class="flex justify-center">
      <div class="flex flex-col pt-10">
        <p class="text-lg font-bold">{{ templateTitle }}</p>
        <p>{{ templateDescription }}</p>
      </div>
    </div>
  </ClusterMainLayout>
</template>
