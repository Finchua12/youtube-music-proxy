<template>
  <div class="library-page">
    <div class="header-section">
      <h1>Ваша бібліотека</h1>
      <div class="library-stats">
        <div class="stat-item">
          <span class="stat-value">{{ playlistCount }}</span>
          <span class="stat-label">Плейлисти</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ likedTracksCount }}</span>
          <span class="stat-label">Улюблені</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ downloadedCount }}</span>
          <span class="stat-label">Завантажені</span>
        </div>
      </div>
    </div>

    <!-- Library Navigation -->
    <div class="library-nav">
      <button
        v-for="tab in libraryTabs"
        :key="tab.id"
        class="nav-tab"
        :class="{ active: activeTab === tab.id }"
        @click="setActiveTab(tab.id)"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- Playlists Tab -->
    <div v-if="activeTab === 'playlists'" class="library-content">
      <div class="content-header">
        <h2>Плейлисти</h2>
        <button class="create-btn" @click="createPlaylist">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Створити плейлист
        </button>
      </div>

      <div class="playlists-grid">
        <div
          v-for="playlist in playlists"
          :key="playlist.id"
          class="playlist-card"
          @click="openPlaylist(playlist)"
        >
          <div class="playlist-image">
            <img :src="playlist.image" :alt="playlist.name" v-if="playlist.image">
            <div class="image-placeholder" v-else>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <button class="play-btn" @click.stop="playPlaylist(playlist)">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
              </svg>
            </button>
          </div>
          <div class="playlist-info">
            <h3 class="playlist-name">{{ playlist.name }}</h3>
            <p class="playlist-meta">{{ playlist.trackCount }} треків</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Liked Songs Tab -->
    <div v-if="activeTab === 'liked'" class="library-content">
      <div class="content-header">
        <h2>Улюблені треки</h2>
        <button class="play-all-btn" @click="playAllLiked">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
          </svg>
          Відтворити все
        </button>
      </div>

      <div class="tracks-list">
        <div
          v-for="(track, index) in likedTracks"
          :key="track.id"
          class="track-item"
          @click="playTrack(track)"
        >
          <div class="track-number">{{ index + 1 }}</div>
          <div class="track-info">
            <div class="track-title">{{ track.title }}</div>
            <div class="track-meta">{{ track.artist }} • {{ track.album }}</div>
          </div>
          <div class="track-duration">{{ formatDuration(track.duration) }}</div>
          <button class="track-action-btn" @click.stop="removeFromLiked(track)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" fill="#FF0000"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Downloaded Tab -->
    <div v-if="activeTab === 'downloaded'" class="library-content">
      <div class="content-header">
        <h2>Завантажені треки</h2>
        <div class="download-stats">
          <span class="used-space">{{ formatBytes(usedSpace) }} з {{ formatBytes(totalSpace) }} використано</span>
        </div>
      </div>

      <div class="tracks-list">
        <div
          v-for="(track, index) in downloadedTracks"
          :key="track.id"
          class="track-item"
          @click="playTrack(track)"
        >
          <div class="track-number">{{ index + 1 }}</div>
          <div class="track-info">
            <div class="track-title">{{ track.title }}</div>
            <div class="track-meta">{{ track.artist }} • {{ track.album }}</div>
          </div>
          <div class="track-duration">{{ formatDuration(track.duration) }}</div>
          <button class="track-action-btn" @click.stop="removeDownload(track)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 7L18.1327 19.1425C18.0579 20.1891 17.187 21 16.1378 21H7.86224C6.81296 21 5.94209 20.1891 5.86732 19.1425L5 7M10 11V17M14 11V17M15 7V4C15 3.44772 14.5523 3 14 3H10C9.44772 3 9 3.44772 9 4V7M4 7H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Recently Added Tab -->
    <div v-if="activeTab === 'recent'" class="library-content">
      <div class="content-header">
        <h2>Нещодавно додані</h2>
      </div>

      <div class="tracks-list">
        <div
          v-for="(track, index) in recentlyAdded"
          :key="track.id"
          class="track-item"
          @click="playTrack(track)"
        >
          <div class="track-number">{{ index + 1 }}</div>
          <div class="track-info">
            <div class="track-title">{{ track.title }}</div>
            <div class="track-meta">{{ track.artist }} • {{ track.album }}</div>
          </div>
          <div class="track-duration">{{ formatDuration(track.duration) }}</div>
          <button class="track-action-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

// Reactive state
const activeTab = ref('playlists')

const libraryTabs = [
  { id: 'playlists', name: 'Плейлисти' },
  { id: 'liked', name: 'Улюблені' },
  { id: 'downloaded', name: 'Завантажені' },
  { id: 'recent', name: 'Нещодавні' }
]

// Computed data from store
const playlists = computed(() => playerStore.playlists)
const likedTracks = computed(() => {
  // This would be implemented when we have the actual liked tracks data
  return []
})

// Mock data for now
const downloadedTracks = ref([
  {
    id: '1',
    title: 'We Will Rock You',
    artist: 'Queen',
    album: 'News of the World',
    duration: 125
  },
  {
    id: '2',
    title: 'Another One Bites the Dust',
    artist: 'Queen',
    album: 'The Game',
    duration: 215
  }
])

const recentlyAdded = ref([
  {
    id: '1',
    title: 'Don\'t Stop Me Now',
    artist: 'Queen',
    album: 'Jazz',
    duration: 209
  },
  {
    id: '2',
    title: 'Somebody to Love',
    artist: 'Queen',
    album: 'A Day at the Races',
    duration: 295
  }
])

const usedSpace = ref(1256789012) // bytes
const totalSpace = ref(5000000000) // bytes

// Stats
const playlistCount = computed(() => playlists.value.length)
const likedTracksCount = computed(() => playerStore.likedTracks.size)
const downloadedCount = computed(() => downloadedTracks.value.length)

// Load data on mount
onMounted(async () => {
  await playerStore.loadPlaylists()
  await playerStore.loadLikedTracks()
})

// Methods
const setActiveTab = (tabId: string) => {
  activeTab.value = tabId
}

const createPlaylist = () => {
  console.log('Create new playlist')
}

const openPlaylist = (playlist: any) => {
  console.log('Open playlist:', playlist.name)
}

const playPlaylist = (playlist: any) => {
  console.log('Play playlist:', playlist.name)
}

const playTrack = (track: any) => {
  playerStore.playTrack(track)
}

const playAllLiked = () => {
  console.log('Play all liked tracks')
}

const removeFromLiked = (track: any) => {
  playerStore.toggleLike(track.id)
}

const removeDownload = (track: any) => {
  console.log('Remove download:', track.title)
}

const formatDuration = playerStore.formatTime

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.library-page {
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
  margin-bottom: 16px;
  color: var(--text-primary);
}

.library-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.library-nav {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.nav-tab {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border: none;
  border-radius: 20px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-tab:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.nav-tab.active {
  background: var(--accent);
  color: white;
}

.library-content {
  margin-bottom: 40px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.content-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.create-btn, .play-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--accent);
  border: none;
  border-radius: 20px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn:hover, .play-all-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.download-stats {
  font-size: 14px;
  color: var(--text-secondary);
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

.playlist-card {
  background: var(--surface);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.playlist-card:hover {
  background: var(--surface-hover);
  transform: translateY(-4px);
}

.playlist-image {
  aspect-ratio: 1;
  position: relative;
}

.playlist-image img {
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

.playlist-card:hover .play-btn {
  opacity: 1;
  transform: translateY(0);
}

.playlist-info {
  padding: 16px;
}

.playlist-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 16px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.playlist-meta {
  font-size: 14px;
  color: var(--text-secondary);
}

.tracks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.track-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.track-item:hover {
  background: var(--hover-bg);
}

.track-number {
  width: 32px;
  font-size: 14px;
  color: var(--text-tertiary);
  text-align: center;
}

.track-info {
  flex: 1;
  min-width: 0;
  margin-right: 16px;
}

.track-title {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-meta {
  font-size: 14px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  font-size: 14px;
  color: var(--text-secondary);
  margin-right: 16px;
  min-width: 40px;
  text-align: right;
}

.track-action-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  opacity: 0;
}

.track-item:hover .track-action-btn {
  opacity: 1;
}

.track-action-btn:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}
</style>