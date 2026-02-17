<template>
  <div id="app">
    <div class="main-layout">
      <h1>YouTube Music Proxy</h1>
      <p>Loading: {{ isLoading }}</p>
      <p v-if="loadError">Error: {{ loadError }}</p>
      <p v-if="!isLoading && !loadError">Ready!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const isLoading = ref(true)
const loadError = ref<string | null>(null)

onMounted(() => {
  console.log('App mounted!')
  setTimeout(() => {
    isLoading.value = false
  }, 1000)
})
</script>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #121212;
  color: #ffffff;
}

.main-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 16px;
}

h1 {
  color: #1db954;
}
</style>
