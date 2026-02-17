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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
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
  color: var(--text-secondary);
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
  padding: 10px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  font-weight: 600;
}

.error-screen button:hover {
  background: var(--accent-hover);
}
</style>
