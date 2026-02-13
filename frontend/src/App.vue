<template>
  <div id="app">
    <div class="titlebar" data-tauri-drag-region>
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
      <Sidebar />
      <main class="content">
        <PlayerBar />
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getCurrent } from '@tauri-apps/api/window'
import { onMounted } from 'vue'
import { usePlayerStore } from '@/stores/player'
import Sidebar from './components/Sidebar.vue'
import PlayerBar from './components/PlayerBar.vue'

const playerStore = usePlayerStore()
const appWindow = getCurrent()

// Load initial data
onMounted(async () => {
  await playerStore.loadRecentlyPlayed()
  await playerStore.loadPlaylists()
  await playerStore.loadLikedTracks()
})

const minimizeWindow = () => {
  appWindow.minimize()
}

const toggleMaximize = async () => {
  if (await appWindow.isMaximized()) {
    appWindow.unmaximize()
  } else {
    appWindow.maximize()
  }
}

const closeWindow = () => {
  appWindow.close()
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
</style>