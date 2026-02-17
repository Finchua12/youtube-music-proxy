<template>
  <div id="app">
    <div class="main-layout">
      <div v-if="isLoading" class="loading-screen">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      <div v-else-if="loadError" class="error-screen">
        <p>{{ loadError }}</p>
        <button @click="retryLoad">Retry</button>
      </div>
      <template v-else>
        <Sidebar />
        <main class="content">
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
    console.error('Failed to load initial data:', error)
    loadError.value = 'Failed to load data'
  } finally {
    isLoading.value = false
  }
}

const retryLoad = () => {
  loadData()
}
</script>

<style>
:root {
  --bg-primary: #121212;
  --bg-secondary: #1f1f1f;
  --bg-tertiary: #2d2d2d;
  --surface: #282828;
  --surface-hover: #3f3f3f;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
  --text-tertiary: #a7a7a7;
  --accent: #1db954;
  --accent-hover: #1ed760;
  --accent-active: #15853d;
  --border-color: #3f3f3f;
  --hover-bg: rgba(255, 255, 255, 0.1);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
}

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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.content {
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
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--bg-tertiary);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-screen button {
  padding: 8px 16px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
