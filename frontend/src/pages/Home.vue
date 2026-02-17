<template>
  <div class="home-page">
    <div class="header-section">
      <h1>YouTube Music</h1>
      <div class="greeting">Популярні відео з YouTube</div>
    </div>

    <!-- Trending -->
    <section class="section">
      <div class="section-header">
        <h2>Популярні</h2>
      </div>
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Завантаження...</p>
      </div>
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="loadTrending">Повторити</button>
      </div>
      <div v-else class="cards-grid">
        <div
          v-for="track in trendingTracks"
          :key="track.id"
          class="card track-card"
          @click="playTrack(track)"
        >
          <div class="card-image">
            <img :src="track.thumbnail" :alt="track.title" v-if="track.thumbnail">
            <div class="image-placeholder" v-else>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <path d="M12 3V16M12 16L16 12M12 16L8 12" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <button class="play-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5V19L19 12L8 5Z"/>
              </svg>
            </button>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ track.title }}</h3>
            <p class="card-subtitle">{{ track.artist }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePlayerStore } from '@/stores/player'
import { trendingApi } from '@/services/api'

const playerStore = usePlayerStore()

const trendingTracks = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await loadTrending()
})

const loadTrending = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await trendingApi.getTrending()
    trendingTracks.value = response.results || []
  } catch (e) {
    console.error('Failed to load trending:', e)
    error.value = 'Не вдалося завантажити'
  } finally {
    loading.value = false
  }
}

const playTrack = (track: any) => {
  playerStore.playTrack(track)
}
</script>

<style scoped>
.home-page {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}

.header-section {
  margin-bottom: 32px;
}

.header-section h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.greeting {
  font-size: 18px;
  color: var(--text-secondary);
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.see-all-btn {
  background: transparent;
  border: none;
  color: var(--accent);
  font-weight: 600;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 20px;
}

.see-all-btn:hover {
  background: var(--hover-bg);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
}

.card {
  background: var(--surface);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  cursor: pointer;
}

.card:hover {
  background: var(--surface-hover);
  transform: translateY(-4px);
}

.card-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.play-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 40px;
  height: 40px;
  background: var(--accent);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  cursor: pointer;
}

.card:hover .play-btn {
  opacity: 1;
  transform: translateY(0);
}

.card-content {
  padding: 16px;
}

.card-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 16px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  color: var(--text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--bg-tertiary);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state button {
  margin-top: 16px;
  padding: 8px 16px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
