<template>
  <div id="app">
    <div class="main-layout">
      <div v-if="isLoading" class="loading-screen">
        <div class="loader"></div>
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
    console.error('Failed to load initial data:', error)
    loadError.value = 'Не вдалося завантажити дані'
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

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
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
  background: linear-gradient(135deg, var(--bg-primary) 0%, #0f0f18 100%);
}

.loading-screen,
.error-screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
}

.loader {
  width: 48px;
  height: 48px;
  border: 3px solid var(--bg-tertiary);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-screen button {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
  color: white;
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.error-screen button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}
</style>
