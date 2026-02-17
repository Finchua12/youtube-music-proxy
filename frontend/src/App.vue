<template>
  <div id="app">
    <div class="titlebar" data-tauri-drag-region v-if="isTauri">
      <div class="titlebar-title">YouTube Music Proxy</div>
      <div class="titlebar-controls">
        <button class="titlebar-button" @click="minimizeWindow">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <rect width="10" height="1" x="1" y="6" fill="currentColor"></rect>
          </svg>
        </button>
        <button class="titlebar-button" @click="toggleMaximize">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <rect width="9" height="9" x="1.5" y="1.5" fill="none" stroke="currentColor"></rect>
          </svg>
        </button>
        <button class="titlebar-button close" @click="closeWindow">
          <svg width="12" height="12" viewBox="0 0 12 12">
            <line x1="2" y1="2" x2="10" y2="10" stroke="currentColor" stroke-width="1.5"></line>
            <line x1="10" y1="2" x2="2" y2="10" stroke="currentColor" stroke-width="1.5"></line>
          </svg>
        </button>
      </div>
    </div>

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
    await playerStore.loadRecentlyPlayed()
    await playerStore.loadPlaylists()
    await playerStore.loadLikedTracks()
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

const isTauri = typeof window !== 'undefined' && window.__TAURI__

const minimizeWindow = () => {
  if (isTauri) {
    import('@tauri-apps/api/window').then(({ getCurrent }) => {
      getCurrent().minimize()
    })
  }
}

const toggleMaximize = async () => {
  if (isTauri) {
    const { getCurrent } = await import('@tauri-apps/api/window')
    const win = getCurrent()
    if (await win.isMaximized()) {
      win.unmaximize()
    } else {
      win.maximize()
    }
  }
}

const closeWindow = () => {
  if (isTauri) {
    import('@tauri-apps/api/window').then(({ getCurrent }) => {
      getCurrent().close()
    })
  }
}
</script>

<style>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.titlebar {
  height: 32px;
  background: var(--bg-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 8px;
  -webkit-app-region: drag;
  border-bottom: 1px solid var(--border-color);
}

.titlebar-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.titlebar-controls {
  display: flex;
  gap: 4px;
  -webkit-app-region: no-drag;
}

.titlebar-button {
  width: 32px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.titlebar-button:hover {
  background: var(--hover-bg);
}

.titlebar-button.close:hover {
  background: #ff5f57;
  color: white;
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
