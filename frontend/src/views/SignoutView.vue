<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  authStore.logout()
  router.push({ name: 'login' })
})
</script>

<template>
  <main>Bye!</main>
</template>
