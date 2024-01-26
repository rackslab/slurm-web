<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import type { Ref } from 'vue'
import { useGatewayAPI } from '@/composables/GatewayAPI'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const gateway = useGatewayAPI()

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
    canvas.value.height = 500
    var context = canvas.value.getContext('2d') as CanvasRenderingContext2D
    const image = await createImageBitmap(await gateway.infrastructureImagePng(props.cluster))
    const maxRatio = Math.max(image.height / canvas.value.height, image.width / canvas.value.width)
    console.log(`image width ${image.width} height ${image.height} ratio ${maxRatio} canvas width ${canvas.value.width} height ${canvas.value.height}`)
    const x = (canvas.value.width - (image.width / maxRatio)) / 2
    const y = (canvas.value.height - (image.height / maxRatio)) / 2
    context.drawImage(image, x, y, image.width / maxRatio, image.height / maxRatio)
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

watch(
  () => props.cluster,
  () => {
    updateCanvas()
  }
)

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
