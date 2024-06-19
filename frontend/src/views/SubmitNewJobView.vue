<!--
  Copyright (c) 2023-2024 Rackslab

  This file is part of Slurm-web.

  SPDX-License-Identifier: GPL-3.0-or-later
-->

<script setup lang="ts">
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'
import CardTemplate from '@/components/CardTemplate.vue'
import { ChevronLeftIcon } from '@heroicons/vue/20/solid'
import { useClusterDataPoller } from '@/composables/DataPoller'
import type { Template } from '@/composables/GatewayAPI'

const { data } = useClusterDataPoller<Template[]>('templates', 5000)

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})
</script>

<template>
  <ClusterMainLayout
    :cluster="props.cluster"
    :viewDetails="[
      { titleView: 'Jobs', routeName: 'jobs' },
      { titleView: 'Submit a new job', routeName: 'submit-new-job' }
    ]"
  >
    <router-link :to="{ name: 'jobs' }"
      ><button
        type="button"
        class="mb-16 mt-8 inline-flex items-center gap-x-2 rounded-md bg-slurmweb px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slurmweb-dark focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slurmweb-dark"
      >
        <ChevronLeftIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
        Jobs
      </button></router-link
    >

    <div class="flex justify-center">
      <div class="flex flex-col pt-10">
        <p class="text-lg font-bold">Submit new job</p>
        <p>Select a template to submit a new job</p>

        <div class="flex">
          <div v-for="template in data" :key="template.name">
            <CardTemplate
              :title="template.name"
              :description="template.description"
              :idTemplate="template.id"
            />
          </div>
        </div>
      </div>
    </div>
  </ClusterMainLayout>
</template>
