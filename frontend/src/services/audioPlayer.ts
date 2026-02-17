import { Howl, Howler } from 'howler'
import { usePlayerStore } from '@/stores/player'
import { downloadService } from '@/services/downloadService'

class AudioPlayerService {
  private sound: Howl | null = null
  private _playerStore: ReturnType<typeof usePlayerStore> | null = null

  private get playerStore() {
    if (!this._playerStore) {
      this._playerStore = usePlayerStore()
    }
    return this._playerStore
  }

  // Initialize audio player
  initialize() {
    // Set up Howler global settings
    Howler.volume(this.playerStore.volume)
    Howler.mute(this.playerStore.isMuted)
  }

  // Play audio for a track
  async playTrack(track: any) {
    try {
      // Download the audio file
      const url = await downloadService.downloadAudio(track.id, '192k')

      // Stop current sound if playing
      if (this.sound) {
        this.sound.stop()
        this.sound.unload()
      }

      // Create new sound
      this.sound = new Howl({
        src: [url],
        html5: true, // Use HTML5 Audio for streaming
        volume: this.playerStore.volume,

        onplay: () => {
          console.log('Audio started playing')
        },

        onpause: () => {
          console.log('Audio paused')
        },

        onstop: () => {
          console.log('Audio stopped')
        },

        onend: () => {
          console.log('Audio finished')
          this.handleTrackEnd()
        },

        onload: () => {
          console.log('Audio loaded')
        },

        onloaderror: (id, error) => {
          console.error('Audio load error:', error)
        },

        onplayerror: (id, error) => {
          console.error('Audio play error:', error)
        }
      })

      // Play the sound
      this.sound.play()
    } catch (error) {
      console.error('Failed to play track:', error)
      throw error
    }
  }

  // Play audio from URL (for backward compatibility)
  async play(url: string) {
    // Stop current sound if playing
    if (this.sound) {
      this.sound.stop()
      this.sound.unload()
    }

    // Create new sound
    this.sound = new Howl({
      src: [url],
      html5: true, // Use HTML5 Audio for streaming
      volume: this.playerStore.volume,

      onplay: () => {
        console.log('Audio started playing')
      },

      onpause: () => {
        console.log('Audio paused')
      },

      onstop: () => {
        console.log('Audio stopped')
      },

      onend: () => {
        console.log('Audio finished')
        this.handleTrackEnd()
      },

      onload: () => {
        console.log('Audio loaded')
      },

      onloaderror: (id, error) => {
        console.error('Audio load error:', error)
      },

      onplayerror: (id, error) => {
        console.error('Audio play error:', error)
      }
    })

    // Play the sound
    this.sound.play()
  }

  // Pause current audio
  pause() {
    if (this.sound && this.sound.playing()) {
      this.sound.pause()
    }
  }

  // Resume current audio
  resume() {
    if (this.sound && !this.sound.playing()) {
      this.sound.play()
    }
  }

  // Stop current audio
  stop() {
    if (this.sound) {
      this.sound.stop()
    }
  }

  // Seek to position (in seconds)
  seek(position: number) {
    if (this.sound) {
      this.sound.seek(position)
    }
  }

  // Get current position (in seconds)
  getPosition(): number {
    if (this.sound) {
      return this.sound.seek() as number
    }
    return 0
  }

  // Get duration (in seconds)
  getDuration(): number {
    if (this.sound) {
      return this.sound.duration()
    }
    return 0
  }

  // Set volume (0-1)
  setVolume(volume: number) {
    Howler.volume(volume)
    if (this.sound) {
      this.sound.volume(volume)
    }
  }

  // Mute/unmute
  setMute(muted: boolean) {
    Howler.mute(muted)
  }

  // Check if playing
  isPlaying(): boolean {
    return this.sound ? this.sound.playing() : false
  }

  // Handle track end
  private handleTrackEnd() {
    // If repeat mode is 'one', replay current track
    if (this.playerStore.repeatMode === 'one') {
      if (this.playerStore.currentTrack) {
        // Replay current track
        // In a real implementation, this would trigger a download and play
        console.log('Repeating current track')
      }
    }
    // If repeat mode is 'all' or no repeat, go to next track
    else {
      this.playerStore.nextTrack()
    }
  }

  // Clean up resources
  destroy() {
    if (this.sound) {
      this.sound.stop()
      this.sound.unload()
      this.sound = null
    }
  }
}

// Export singleton instance
export const audioPlayer = new AudioPlayerService()