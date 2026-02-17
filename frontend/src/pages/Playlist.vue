<template>
  <div class="playlist-page">
    <!-- Playlist Header -->
    <div class="playlist-header">
      <div class="playlist-art">
        <img :src="playlist.image" :alt="playlist.name" v-if="playlist.image">
        <div class="art-placeholder" v-else>
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="1"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1"/>
          </svg>
        </div>
      </div>
      <div class="playlist-info">
        <div class="playlist-type">Плейлист</div>
        <h1 class="playlist-name">{{ playlist.name }}</h1>
        <div class="playlist-meta">
          <span class="creator">{{ playlist.creator }}</span>
          <span class="separator">•</span>
          <span class="track-count">{{ playlist.tracks.length }} треків</span>
          <span class="separator">•</span>
          <span class="duration">{{ formatTotalDuration(playlist.totalDuration) }}</span>
        </div>
        <div class="playlist-actions">
          <button class="play-btn" @click="playPlaylist">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
            </svg>
            Відтворити
          </button>
          <button class="action-btn" @click="shufflePlaylist">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 3H21V8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M4 20L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 16V21H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 15L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M4 4L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="action-btn" @click="toggleLike">
            <svg v-if="isLiked" width="20" height="20" viewBox="0 0 24 24" fill="#FF0000" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" />
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
          <button class="action-btn" @click="showMoreOptions">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="1" fill="currentColor"/>
              <circle cx="12" cy="5" r="1" fill="currentColor"/>
              <circle cx="12" cy="19" r="1" fill="currentColor"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Playlist Tracks -->
    <div class="playlist-tracks">
      <div class="tracks-header">
        <div class="header-cell">#</div>
        <div class="header-cell title-cell">Назва</div>
        <div class="header-cell album-cell">Альбом</div>
        <div class="header-cell date-cell">Дата додавання</div>
        <div class="header-cell duration-cell">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
      </div>

      <div
        v-for="(track, index) in playlist.tracks"
        :key="track.id"
        class="track-row"
        :class="{ playing: currentTrackId === track.id }"
        @click="playTrack(track)"
      >
        <div class="track-cell index-cell">
          <span class="track-index">{{ index + 1 }}</span>
          <button class="play-track-btn" v-if="currentTrackId === track.id">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
              <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
            </svg>
          </button>
          <button class="play-track-btn" v-else>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <div class="track-cell title-cell">
          <div class="track-title-info">
            <div class="track-title">{{ track.title }}</div>
            <div class="track-artist">{{ track.artist }}</div>
          </div>
        </div>
        <div class="track-cell album-cell">
          <div class="album-info">
            <img :src="track.albumArt" :alt="track.album" v-if="track.albumArt" class="album-thumb">
            <span class="album-name">{{ track.album }}</span>
          </div>
        </div>
        <div class="track-cell date-cell">{{ formatDate(track.addedDate) }}</div>
        <div class="track-cell duration-cell">
          <div class="track-actions">
            <button class="track-action-btn" @click.stop="toggleTrackLike(track)">
              <svg v-if="track.liked" width="16" height="16" viewBox="0 0 24 24" fill="#FF0000" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" />
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
            <span class="track-duration">{{ formatDuration(track.duration) }}</span>
            <button class="track-action-btn menu-btn" @click.stop="showTrackMenu(track)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="1" fill="currentColor"/>
                <circle cx="12" cy="5" r="1" fill="currentColor"/>
                <circle cx="12" cy="19" r="1" fill="currentColor"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

// Props
const props = defineProps<{
  id: string
}()

// Route
const route = useRoute()

// Reactive state
const playlist = ref<any>({
  id: props.id || '1',
  name: 'Плейлист',
  creator: 'Користувач',
  tracks: [],
  totalDuration: 0,
  image: ''
})

const isLiked = ref(false)

// Computed
const currentTrackId = computed(() => playerStore.currentTrack?.id || null)
const totalTracks = computed(() => playlist.value.tracks.length)

// Load playlist data
onMounted(async () => {
  // Check if this is favorites playlist
  if (props.id === 'favorites') {
    const likedTracks = playerStore.getLikedTracks ? playerStore.getLikedTracks() : []
    playlist.value = {
      id: 'favorites',
      name: 'Улюблені',
      creator: 'Користувач',
      tracks: likedTracks,
      totalDuration: likedTracks.reduce((sum: number, t: any) => sum + (t.duration || 0), 0),
      image: ''
    }
    isLiked.value = true
  } else if (props.id === 'recent') {
    playlist.value = {
      id: 'recent',
      name: 'Нещодавно',
      creator: 'Користувач',
      tracks: playerStore.recentlyPlayed || [],
      totalDuration: (playerStore.recentlyPlayed || []).reduce((sum: number, t: any) => sum + (t.duration || 0), 0),
      image: ''
    }
  } else {
    playlist.value = {
      id: props.id || '1',
      name: 'Плейлист',
      creator: 'Користувач',
      tracks: [],
      totalDuration: 0,
      image: ''
    }
  }
})

// Methods
const playPlaylist = () => {
  if (playlist.value.tracks.length > 0) {
    playerStore.playTrack(playlist.value.tracks[0], playlist.value.tracks)
  }
}

const shufflePlaylist = () => {
  playerStore.toggleShuffle()
  console.log('Shuffle playlist:', playlist.value.name)
}

const toggleLike = () => {
  isLiked.value = !isLiked.value
  console.log('Toggle playlist like')
}

const showMoreOptions = () => {
  console.log('Show more options')
}

const playTrack = (track: any) => {
  playerStore.playTrack(track, playlist.value.tracks)
}

const toggleTrackLike = (track: any) => {
  playerStore.toggleLike(track.id)
  console.log('Toggle track like:', track.title)
}

const showTrackMenu = (track: any) => {
  console.log('Show track menu:', track.title)
}

const formatDuration = playerStore.formatTime

const formatTotalDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)

  if (hours > 0) {
    return `${hours} год ${mins} хв`
  }
  return `${mins} хв`
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('uk-UA', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}
</script>

<style scoped>
.playlist-page {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}

.playlist-header {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
  align-items: flex-end;
}

.playlist-art {
  width: 230px;
  height: 230px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.playlist-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.art-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.playlist-info {
  flex: 1;
}

.playlist-type {
  font-size: 14px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.playlist-name {
  font-size: 48px;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 16px;
  line-height: 1.1;
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 16px;
  margin-bottom: 32px;
}

.separator {
  color: var(--text-tertiary);
}

.playlist-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.play-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 32px;
  background: var(--accent);
  border: none;
  border-radius: 24px;
  font-weight: 700;
  font-size: 16px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.play-btn:hover {
  background: var(--accent-hover);
  transform: scale(1.05);
}

.action-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  border: none;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--surface-hover);
  transform: scale(1.1);
}

.playlist-tracks {
  margin-top: 24px;
}

.tracks-header {
  display: flex;
  padding: 8px 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.header-cell {
  padding: 0 16px;
  text-align: left;
}

.index-cell {
  width: 60px;
}

.title-cell {
  flex: 3;
  min-width: 200px;
}

.album-cell {
  flex: 2;
  min-width: 150px;
}

.date-cell {
  flex: 1;
  min-width: 120px;
}

.duration-cell {
  width: 120px;
  text-align: right;
  padding-right: 32px;
}

.track-row {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.track-row:hover {
  background: var(--hover-bg);
}

.track-row.playing {
  background: rgba(29, 185, 84, 0.1);
}

.track-cell {
  padding: 8px 16px;
  display: flex;
  align-items: center;
}

.index-cell {
  width: 60px;
  position: relative;
}

.track-index {
  font-size: 14px;
  color: var(--text-tertiary);
}

.track-row:hover .track-index {
  display: none;
}

.play-track-btn {
  position: absolute;
  left: 16px;
  background: transparent;
  border: none;
  color: var(--accent);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.track-row:hover .play-track-btn {
  opacity: 1;
}

.title-cell {
  flex: 3;
  min-width: 200px;
}

.track-title-info {
  display: flex;
  flex-direction: column;
}

.track-title {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  font-size: 14px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.album-cell {
  flex: 2;
  min-width: 150px;
}

.album-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.album-thumb {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.album-name {
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date-cell {
  flex: 1;
  min-width: 120px;
  color: var(--text-secondary);
  font-size: 14px;
}

.duration-cell {
  width: 120px;
  text-align: right;
  padding-right: 16px;
}

.track-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  justify-content: flex-end;
}

.track-action-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  opacity: 0;
}

.track-row:hover .track-action-btn {
  opacity: 1;
}

.track-action-btn:hover {
  color: var(--text-primary);
  background: var(--hover-bg);
}

.menu-btn {
  opacity: 0;
}

.track-row:hover .menu-btn {
  opacity: 1;
}

.track-duration {
  font-size: 14px;
  color: var(--text-secondary);
  min-width: 40px;
  text-align: right;
}
</style>