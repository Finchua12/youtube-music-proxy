import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { searchApi, playlistApi, recentlyPlayedApi, likesApi, downloadApi } from '@/services/api'
import { audioPlayer, setPlayerStoreGetter, onPlayerReady } from '@/services/audioPlayer'

export const usePlayerStore = defineStore('player', () => {
  // State
  const isPlaying = ref(false)
  const currentTrack = ref<any>(null)
  const queue = ref<any[]>([])
  const currentIndex = ref(0)
  const volume = ref(0.8)
  const isMuted = ref(false)
  const repeatMode = ref<'off' | 'all' | 'one'>('off')
  const isShuffled = ref(false)
  const searchResults = ref<any[]>([])
  const playlists = ref<any[]>([])
  const recentlyPlayed = ref<any[]>([])
  const likedTracks = ref<Set<string>>(new Set())
  const playerReady = ref(false)
  const currentProgress = ref(0)

  // Set getter for audio player
  setPlayerStoreGetter(() => usePlayerStore())
  
  // Listen for player ready
  onPlayerReady(() => {
    playerReady.value = true
    console.log('Player ready in store')
  })

  // Initialize audio player
  audioPlayer.initialize()

  // Getters
  const duration = computed(() => currentTrack.value?.duration || 0)
  const progressPercent = computed(() => {
    return duration.value > 0 ? (currentProgress.value / duration.value) * 100 : 0
  })
  const volumePercent = computed(() => volume.value * 100)
  const hasNext = computed(() => currentIndex.value < queue.value.length - 1)
  const hasPrevious = computed(() => currentIndex.value > 0)

  // Actions
  const playTrack = async (track: any, newQueue?: any[]) => {
    if (newQueue) {
      queue.value = [...newQueue]
      currentIndex.value = newQueue.findIndex(t => t.id === track.id)
    }

    // Fetch video details to get duration
    try {
      const response = await fetch(`/api/stream/${track.id}`)
      const data = await response.json()
      if (data.duration) {
        track.duration = data.duration
      }
      if (data.thumbnail && !track.thumbnail) {
        track.thumbnail = data.thumbnail
      }
    } catch (e) {
      console.log('Could not fetch video details')
    }

    currentTrack.value = track

    // Play the track using audio player service
    try {
      await audioPlayer.playTrack(track)
      isPlaying.value = true

      // Add to recently played (localStorage)
      addToRecentlyPlayed(track)

      // Update recently played list
      await loadRecentlyPlayed()
    } catch (error) {
      console.error('Failed to play track:', error)
      isPlaying.value = false
    }
  }

  const pause = () => {
    audioPlayer.pause()
    isPlaying.value = false
  }

  const play = () => {
    audioPlayer.resume()
    isPlaying.value = true
  }

  const togglePlayPause = () => {
    if (isPlaying.value) {
      pause()
    } else {
      play()
    }
  }

  const nextTrack = async () => {
    if (currentIndex.value < queue.value.length - 1) {
      currentIndex.value++
      currentTrack.value = queue.value[currentIndex.value]
      await playTrack(currentTrack.value)
    }
  }

  const previousTrack = async () => {
    if (currentIndex.value > 0) {
      currentIndex.value--
      currentTrack.value = queue.value[currentIndex.value]
      await playTrack(currentTrack.value)
    }
  }

  const seekTo = (percent: number) => {
    const newPosition = (percent / 100) * duration.value
    currentProgress.value = Math.floor(newPosition)
    audioPlayer.seek(newPosition)
  }

  const setVolume = (percent: number) => {
    const newVolume = Math.max(0, Math.min(1, percent / 100))
    volume.value = newVolume
    audioPlayer.setVolume(newVolume)
  }

  const toggleMute = () => {
    isMuted.value = !isMuted.value
    audioPlayer.setMute(isMuted.value)
  }

  const toggleRepeat = () => {
    const modes: Array<'off' | 'all' | 'one'> = ['off', 'all', 'one']
    const currentIndex = modes.indexOf(repeatMode.value)
    repeatMode.value = modes[(currentIndex + 1) % modes.length]
  }

  const toggleShuffle = () => {
    isShuffled.value = !isShuffled.value
  }

  const toggleLike = (track: any) => {
    const trackId = track.id || track
    const existing = likedTracks.value.get(trackId)
    
    if (existing) {
      likedTracks.value.delete(trackId)
    } else {
      // Store full track info
      likedTracks.value.set(trackId, {
        id: trackId,
        title: track.title || 'Unknown',
        artist: track.artist || 'Unknown',
        thumbnail: track.thumbnail || '',
        duration: track.duration || 0
      })
    }
    // Save to localStorage
    const tracksArray = Array.from(likedTracks.value.values())
    localStorage.setItem('likedTracks', JSON.stringify(tracksArray))
  }

  const getLikedTracks = () => {
    return Array.from(likedTracks.value.values())
  }

  const search = async (query: string, maxResults: number = 10) => {
    try {
      const response = await searchApi.search(query, maxResults)
      searchResults.value = response.results || []
      return searchResults.value
    } catch (error) {
      console.error('Search failed:', error)
      searchResults.value = []
      return []
    }
  }

  const loadPlaylists = () => {
    try {
      const saved = localStorage.getItem('playlists')
      if (saved) {
        playlists.value = JSON.parse(saved)
      } else {
        // Default playlists
        playlists.value = [
          { id: 'favorites', name: 'Улюблені', tracks: [] },
          { id: 'recent', name: 'Нещодавно', tracks: [] }
        ]
        savePlaylists()
      }
    } catch (error) {
      console.error('Failed to load playlists:', error)
    }
  }

  const savePlaylists = () => {
    localStorage.setItem('playlists', JSON.stringify(playlists.value))
  }

  const createPlaylist = (name: string) => {
    const newPlaylist = {
      id: 'playlist_' + Date.now(),
      name: name,
      tracks: []
    }
    playlists.value.push(newPlaylist)
    savePlaylists()
    return newPlaylist
  }

  const addToPlaylist = (playlistId: string, track: any) => {
    const playlist = playlists.value.find(p => p.id === playlistId)
    if (playlist && !playlist.tracks.find(t => t.id === track.id)) {
      playlist.tracks.push(track)
      savePlaylists()
    }
  }

  const removeFromPlaylist = (playlistId: string, trackId: string) => {
    const playlist = playlists.value.find(p => p.id === playlistId)
    if (playlist) {
      playlist.tracks = playlist.tracks.filter(t => t.id !== trackId)
      savePlaylists()
    }
  }

  const loadRecentlyPlayed = () => {
    try {
      const saved = localStorage.getItem('recentlyPlayed')
      if (saved) {
        recentlyPlayed.value = JSON.parse(saved)
      }
    } catch (error) {
      console.error('Failed to load recently played:', error)
    }
  }

  const addToRecentlyPlayed = (track: any) => {
    const filtered = recentlyPlayed.value.filter(t => t.id !== track.id)
    recentlyPlayed.value = [track, ...filtered].slice(0, 50)
    localStorage.setItem('recentlyPlayed', JSON.stringify(recentlyPlayed.value))
  }

  const loadLikedTracks = () => {
    try {
      const saved = localStorage.getItem('likedTracks')
      if (saved) {
        const tracks = JSON.parse(saved)
        likedTracks.value = new Map(tracks.map((t: any) => [t.id, t]))
      }
    } catch (error) {
      console.error('Failed to load liked tracks:', error)
    }
  }

  const isTrackLiked = (trackId: string) => {
    return likedTracks.value.has(trackId)
  }
  }

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // Initialize audio player
  const initialize = () => {
    audioPlayer.initialize()
  }

  return {
    // State
    isPlaying,
    currentTrack,
    queue,
    currentIndex,
    volume,
    isMuted,
    repeatMode,
    isShuffled,
    searchResults,
    playlists,
    recentlyPlayed,
    likedTracks,
    currentProgress,
    playerReady,

    // Getters
    duration,
    progressPercent,
    volumePercent,
    hasNext,
    hasPrevious,

    // Actions
    playTrack,
    pause,
    play,
    togglePlayPause,
    nextTrack,
    previousTrack,
    seekTo,
    setVolume,
    toggleMute,
    toggleRepeat,
    toggleShuffle,
    toggleLike,
    getLikedTracks,
    search,
    loadPlaylists,
    loadRecentlyPlayed,
    loadLikedTracks,
    isTrackLiked,
    formatTime,
    initialize
  }
})