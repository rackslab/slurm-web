<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import type { Ref } from 'vue'
import { useHttp } from '@/plugins/http'
import { useRacksDBAPI } from '@/composables/RacksDBAPI'

const http = useHttp()
const racksDBAPI = useRacksDBAPI(http)

const container: Ref<HTMLDivElement | null> = ref(null)
const loading: Ref<HTMLSpanElement | null> = ref(null)
const canvas: Ref<HTMLCanvasElement | null> = ref(null)
let timeout: number = -1 // holder for timeout id
const delay = 250 // delay after event is "complete" to run callback

async function updateCanvas() {
  if (container.value !== null && loading.value !== null && canvas.value !== null) {
    let width = container.value.clientWidth as number
    loading.value.style.visibility = 'hidden'
    canvas.value.style.visibility = 'visible'
    canvas.value.width = width
    var context = canvas.value.getContext('2d') as CanvasRenderingContext2D
    const image = await createImageBitmap(await racksDBAPI.infrastructureImagePng('mercury'))
    context.drawImage(image, 0, 0, canvas.value.width as number, canvas.value.height as number)
  }
}

// window.resize event listener
function updateCanvasDimensions() {
  if (loading.value !== null && canvas.value !== null) {
    loading.value.style.visibility = 'visible'
    canvas.value.style.visibility = 'hidden'
    // clear the timeout
    clearTimeout(timeout)
    // start timing for event "completion"
    timeout = setTimeout(updateCanvas, delay)
  }
}

onMounted(() => {
  updateCanvas()
  window.addEventListener('resize', updateCanvasDimensions)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateCanvasDimensions)
})
</script>

<template>
  <div ref="container" class="min-w-full">
    <span ref="loading">loading</span>
    <canvas ref="canvas">Cluster canvas</canvas>
  </div>
</template>
