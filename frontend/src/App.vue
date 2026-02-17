<template>
  <div id="app">
    <div class="main-layout">
      <div v-if="isLoading" class="loading-screen">
        <div class="spinner"></div>
        <p>Завантаження...</p>
      </div>
      <div v-else-if="loadError" class="error-screen">
        <p>{{ loadError }}</p>
        <button @click="retryLoad" class="btn btn-primary">Повторити</button>
      </div>
      <template v-else>
        <Sidebar />
        <main class="main-content">
          <PlayerBar />
          <router-view />
        </main>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePlayerStore } from '@/stores/player'
import Sidebar from './components/Sidebar.vue'
import PlayerBar from './components/PlayerBar.vue'

const playerStore = usePlayerStore()
const isLoading = ref(true)
const loadError = ref<string | null>(null)

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  isLoading.value = true
  loadError.value = null
  try {
    await Promise.all([
      playerStore.loadRecentlyPlayed(),
      playerStore.loadPlaylists(),
      playerStore.loadLikedTracks()
    ])
  } catch (error) {
    console.error('Failed to load:', error)
    loadError.value = 'Помилка завантаження'
  } finally {
    isLoading.value = false
  }
}

const retryLoad = () => {
  loadData()
}
</script>

<style>
@import './styles/main.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

body {
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.loading-screen,
.error-screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: var(--text-secondary);
}
</style>
