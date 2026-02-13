<template>
  <div class="home-page">
    <div class="header-section">
      <h1>Головна</h1>
      <div class="greeting">Вітаємо вас, Користувачу</div>
    </div>

    <!-- Recently Played -->
    <section class="section">
      <div class="section-header">
        <h2>Нещодавно прослухані</h2>
        <button class="see-all-btn">Дивитись все</button>
      </div>
      <div class="cards-grid">
        <div
          v-for="track in recentlyPlayed"
          :key="track.id"
          class="card track-card"
          @click="playTrack(track)"
        >
          <div class="card-image">
            <img :src="track.image" :alt="track.title" v-if="track.image">
            <div class="image-placeholder" v-else>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3V16M12 16L16 12M12 16L8 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <button class="play-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
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

    <!-- Made for You -->
    <section class="section">
      <div class="section-header">
        <h2>Створено для вас</h2>
        <button class="see-all-btn">Дивитись все</button>
      </div>
      <div class="cards-grid">
        <div
          v-for="playlist in recommendedPlaylists"
          :key="playlist.id"
          class="card playlist-card"
          @click="openPlaylist(playlist)"
        >
          <div class="card-image">
            <img :src="playlist.image" :alt="playlist.title" v-if="playlist.image">
            <div class="image-placeholder" v-else>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <button class="play-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
              </svg>
            </button>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ playlist.title }}</h3>
            <p class="card-subtitle">{{ playlist.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Popular Artists -->
    <section class="section">
      <div class="section-header">
        <h2>Популярні виконавці</h2>
        <button class="see-all-btn">Дивитись все</button>
      </div>
      <div class="artists-grid">
        <div
          v-for="artist in popularArtists"
          :key="artist.id"
          class="artist-card"
          @click="viewArtist(artist)"
        >
          <div class="artist-image">
            <img :src="artist.image" :alt="artist.name" v-if="artist.image">
            <div class="image-placeholder" v-else>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2"/>
                <path d="M7 20C7 17.2386 9.23858 15 12 15C14.7614 15 17 17.2386 17 20" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
          </div>
          <div class="artist-name">{{ artist.name }}</div>
        </div>
      </div>
    </section>

    <!-- Quick Playlists -->
    <section class="section">
      <div class="section-header">
        <h2>Швидкі плейлисти</h2>
      </div>
      <div class="quick-playlists">
        <div
          v-for="playlist in quickPlaylists"
          :key="playlist.id"
          class="quick-playlist"
          :class="{ active: playlist.id === activeQuickPlaylist }"
          @click="setActiveQuickPlaylist(playlist.id)"
        >
          {{ playlist.name }}
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

// Reactive data
const recentlyPlayed = ref<any[]>([])
const recommendedPlaylists = ref<any[]>([])
const popularArtists = ref<any[]>([])
const quickPlaylists = ref([
  { id: 'favorites', name: 'Улюблені' },
  { id: 'recent', name: 'Нещодавні' },
  { id: 'downloads', name: 'Завантажені' },
  { id: 'discover', name: 'Відкрити' }
])

const activeQuickPlaylist = ref('favorites')

// Load data on mount
onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  // Load recently played
  await playerStore.loadRecentlyPlayed()
  recentlyPlayed.value = playerStore.recentlyPlayed

  // Load playlists
  await playerStore.loadPlaylists()
  recommendedPlaylists.value = playerStore.playlists.slice(0, 4)

  // Mock popular artists data
  popularArtists.value = [
    {
      id: '1',
      name: 'Queen',
      image: ''
    },
    {
      id: '2',
      name: 'The Beatles',
      image: ''
    },
    {
      id: '3',
      name: 'Pink Floyd',
      image: ''
    },
    {
      id: '4',
      name: 'Led Zeppelin',
      image: ''
    },
    {
      id: '5',
      name: 'Radiohead',
      image: ''
    }
  ]
}

// Methods
const playTrack = (track: any) => {
  playerStore.playTrack(track)
}

const openPlaylist = (playlist: any) => {
  console.log('Open playlist:', playlist.title)
}

const viewArtist = (artist: any) => {
  console.log('View artist:', artist.name)
}

const setActiveQuickPlaylist = (id: string) => {
  activeQuickPlaylist.value = id
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
  transition: all 0.2s ease;
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
  color: white;
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

.artists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 24px;
}

.artist-card {
  text-align: center;
  cursor: pointer;
}

.artist-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 12px;
  position: relative;
}

.artist-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.artist-image .image-placeholder {
  width: 100%;
  height: 100%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.artist-name {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

.quick-playlists {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-playlist {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border-radius: 20px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-playlist:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.quick-playlist.active {
  background: var(--accent);
  color: white;
}
</style>