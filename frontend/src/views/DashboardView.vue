<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import { useRuntimeStore } from '@/stores/runtime'
import MainLayout from '@/components/MainLayout.vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const cluster: Ref<string> = ref(props.cluster)
const clusterNotFound: Ref<boolean> = ref(false)
const runtimeStore = useRuntimeStore()

onMounted(() => {
  if (!runtimeStore.checkClusterAvailable(cluster.value)) {
    clusterNotFound.value = true
  }
})

</script>

<template>
  <MainLayout>
    <div v-if="clusterNotFound">
      Cluster not found
    </div>
    <div v-else class="home">
      <h1>Dashboard cluster {{ cluster }}</h1>
    </div>
  </MainLayout>
</template>
