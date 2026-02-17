<template>
  <div class="search-page">
    <div class="search-header">
      <h1>Пошук</h1>
      <div class="search-container">
        <div class="search-input-wrapper">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Введіть назву пісні, виконавця або альбом..."
            @input="handleSearch"
          >
          <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Search Filters -->
    <div class="search-filters">
      <button
        v-for="filter in searchFilters"
        :key="filter.id"
        class="filter-btn"
        :class="{ active: activeFilter === filter.id }"
        @click="setActiveFilter(filter.id)"
      >
        {{ filter.name }}
      </button>
    </div>

    <!-- Search Results -->
    <div v-if="searchQuery" class="search-results">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Пошук результатів...</p>
      </div>

      <div v-else-if="searchResults.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <p>За запитом "{{ searchQuery }}" нічого не знайдено</p>
      </div>

      <div v-else>
        <!-- Tracks -->
        <section v-if="activeFilter === 'all' || activeFilter === 'tracks'" class="results-section">
          <h2>Треки</h2>
          <div class="tracks-list">
            <div
              v-for="(track, index) in searchResults.tracks"
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
        </section>

        <!-- Artists -->
        <section v-if="activeFilter === 'all' || activeFilter === 'artists'" class="results-section">
          <h2>Виконавці</h2>
          <div class="artists-grid">
            <div
              v-for="artist in searchResults.artists"
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

        <!-- Playlists -->
        <section v-if="activeFilter === 'all' || activeFilter === 'playlists'" class="results-section">
          <h2>Плейлисти</h2>
          <div class="playlists-grid">
            <div
              v-for="playlist in searchResults.playlists"
              :key="playlist.id"
              class="playlist-card"
              @click="openPlaylist(playlist)"
            >
              <div class="playlist-image">
                <img :src="playlist.image" :alt="playlist.title" v-if="playlist.image">
                <div class="image-placeholder" v-else>
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </div>
              </div>
              <div class="playlist-info">
                <div class="playlist-title">{{ playlist.title }}</div>
                <div class="playlist-meta">{{ playlist.trackCount }} треків</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Recent Searches -->
    <div v-else class="recent-searches">
      <h2>Останні пошуки</h2>
      <div class="recent-searches-list">
        <div
          v-for="search in recentSearches"
          :key="search.id"
          class="recent-search-item"
          @click="setSearchQuery(search.query)"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>{{ search.query }}</span>
        </div>
      </div>

      <!-- Trending Searches -->
      <h2>Популярні запити</h2>
      <div class="trending-searches">
        <div
          v-for="trend in trendingSearches"
          :key="trend.id"
          class="trending-item"
          @click="setSearchQuery(trend.query)"
        >
          {{ trend.query }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

// Reactive state
const searchQuery = ref('')
const activeFilter = ref('all')
const isLoading = ref(false)

const searchFilters = [
  { id: 'all', name: 'Все' },
  { id: 'tracks', name: 'Треки' },
  { id: 'artists', name: 'Виконавці' },
  { id: 'playlists', name: 'Плейлисти' }
]

const recentSearches = ref<{id: string, query: string}[]>([])

const loadRecentSearches = () => {
  try {
    const saved = localStorage.getItem('searchHistory')
    if (saved) {
      recentSearches.value = JSON.parse(saved)
    }
  } catch (e) {
    console.error('Failed to load search history')
  }
}

const saveRecentSearch = (query: string) => {
  const filtered = recentSearches.value.filter(s => s.query !== query)
  recentSearches.value = [{ id: Date.now().toString(), query }, ...filtered].slice(0, 10)
  localStorage.setItem('searchHistory', JSON.stringify(recentSearches.value))
}

const clearRecentSearches = () => {
  recentSearches.value = []
  localStorage.removeItem('searchHistory')
}

const removeRecentSearch = (id: string) => {
  recentSearches.value = recentSearches.value.filter(s => s.id !== id)
  localStorage.setItem('searchHistory', JSON.stringify(recentSearches.value))
}

const trendingSearches = ref([
  { id: '1', query: 'The Beatles' },
  { id: '2', query: 'Led Zeppelin' },
  { id: '3', query: 'Pink Floyd' },
  { id: '4', query: 'Classic Rock' },
  { id: '5', query: 'Guitar Hero' }
])

const searchResults = reactive({
  tracks: [] as any[],
  artists: [] as any[],
  playlists: [] as any[]
})

onMounted(() => {
  loadRecentSearches()
})

// Methods
const handleSearch = async () => {
  if (searchQuery.value.length > 2) {
    isLoading.value = true
    try {
      const results = await playerStore.search(searchQuery.value, 20)
      searchResults.tracks = results.slice(0, 10)
      searchResults.artists = []
      searchResults.playlists = []
      // Save to search history
      saveRecentSearch(searchQuery.value)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      isLoading.value = false
    }
  } else {
    searchResults.tracks = []
    searchResults.artists = []
    searchResults.playlists = []
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.tracks = []
  searchResults.artists = []
  searchResults.playlists = []
}

const setActiveFilter = (filterId: string) => {
  activeFilter.value = filterId
}

const setSearchQuery = (query: string) => {
  searchQuery.value = query
  handleSearch()
}

const playTrack = (track: any) => {
  playerStore.playTrack(track)
}

const viewArtist = (artist: any) => {
  console.log('View artist:', artist.name)
}

const openPlaylist = (playlist: any) => {
  console.log('Open playlist:', playlist.title)
}

const formatDuration = playerStore.formatTime
</script>

<style scoped>
.search-page {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}

.search-header h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.search-container {
  margin-bottom: 32px;
}

.search-input-wrapper {
  position: relative;
  max-width: 600px;
}

.search-input-wrapper svg {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 16px 56px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 16px;
  padding-left: 56px;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
}

.clear-btn {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
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
}

.clear-btn:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.search-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border: none;
  border-radius: 20px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.filter-btn.active {
  background: var(--accent);
  color: white;
}

.loading-state {
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
  border-top: 4px solid var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  color: var(--text-secondary);
  text-align: center;
}

.empty-state svg {
  margin-bottom: 16px;
  color: var(--text-tertiary);
}

.results-section {
  margin-bottom: 40px;
}

.results-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
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

.artists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 24px;
}

.artist-card {
  text-align: center;
  cursor: pointer;
}

.artist-image {
  width: 140px;
  height: 140px;
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

.image-placeholder {
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

.playlist-image .image-placeholder {
  width: 100%;
  height: 100%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.playlist-info {
  padding: 16px;
}

.playlist-title {
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

.recent-searches h2,
.trending-searches h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.recent-searches-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 40px;
}

.recent-search-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.recent-search-item:hover {
  background: var(--hover-bg);
}

.recent-search-item svg {
  color: var(--text-secondary);
}

.recent-search-item span {
  color: var(--text-primary);
  font-weight: 500;
}

.trending-searches {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.trending-item {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border-radius: 20px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.trending-item:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}
</style>