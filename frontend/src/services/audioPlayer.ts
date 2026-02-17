let playerStoreGetter: (() => any) | null = null
let onPlayerReadyCallback: (() => void) | null = null

export function setPlayerStoreGetter(getter: () => any) {
  playerStoreGetter = getter
}

export function onPlayerReady(callback: () => void) {
  onPlayerReadyCallback = callback
}

class AudioPlayerService {
  private player: YT.Player | null = null
  private playerContainer: HTMLDivElement | null = null
  private isReady = false
  private isPlayingState = false
  private progressInterval: number | null = null

  private get playerStore() {
    return playerStoreGetter?.()
  }

  initialize() {
    this.createPlayerContainer()
    this.loadYouTubeAPI()
  }

  private createPlayerContainer() {
    if (document.getElementById('youtube-player-container')) return
    
    this.playerContainer = document.createElement('div')
    this.playerContainer.id = 'youtube-player-container'
    this.playerContainer.style.cssText = 'position: fixed; visibility: hidden; pointer-events: none;'
    document.body.appendChild(this.playerContainer)
  }

  private loadYouTubeAPI() {
    if ((window as any).YT) {
      this.initPlayer()
      return
    }

    const tag = document.createElement('script')
    tag.src = 'https://www.youtube.com/iframe_api'
    const firstScriptTag = document.getElementsByTagName('script')[0]
    firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag)

    ;(window as any).onYouTubeIframeAPIReady = () => {
      this.initPlayer()
    }
  }

  private initPlayer() {
    if (!this.playerContainer) return
    
    const origin = window.location.origin
    
    this.player = new (window as any).YT.Player(this.playerContainer, {
      height: '1',
      width: '1',
      playerVars: {
        autoplay: 1,
        controls: 0,
        disablekb: 1,
        fs: 0,
        modestbranding: 1,
        rel: 0,
        showinfo: 0,
        iv_load_policy: 3,
        playsinline: 1,
        widget_referrer: origin
      },
      events: {
        onReady: () => {
          this.isReady = true
          console.log('YouTube player ready')
          onPlayerReadyCallback?.()
        },
        onStateChange: (event: any) => {
          const YT = (window as any).YT
          if (event.data === YT.PlayerState.PLAYING) {
            this.isPlayingState = true
            this.startProgressTracking()
            this.updatePlayerStore()
          } else if (event.data === YT.PlayerState.PAUSED) {
            this.isPlayingState = false
            this.stopProgressTracking()
            this.updatePlayerStore()
          } else if (event.data === YT.PlayerState.ENDED) {
            this.isPlayingState = false
            this.stopProgressTracking()
            this.handleTrackEnd()
          }
        }
      }
    })
  }

  private startProgressTracking() {
    if (this.progressInterval) return
    this.progressInterval = window.setInterval(() => {
      this.updatePlayerStore()
    }, 1000)
  }

  private stopProgressTracking() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval)
      this.progressInterval = null
    }
  }

  private updatePlayerStore() {
    const store = this.playerStore
    if (!store) return
    
    const position = this.getPosition()
    const duration = this.getDuration()
    
    if (store.currentProgress !== undefined) {
      store.currentProgress = position
    }
    if (store.isPlaying !== undefined) {
      store.isPlaying = this.isPlayingState
    }
  }

  async waitForReady(): Promise<void> {
    if (this.isReady) return
    return new Promise((resolve) => {
      const check = () => {
        if (this.isReady) {
          resolve()
        } else {
          setTimeout(check, 100)
        }
      }
      check()
    })
  }

  async playTrack(track: any) {
    await this.waitForReady()
    
    if (!this.player) {
      console.error('Player not initialized')
      throw new Error('Player not initialized')
    }

    try {
      await this.player.loadVideoById({
        videoId: track.id,
        startSeconds: 0
      })
      this.isPlayingState = true
      this.startProgressTracking()
      console.log('Playing:', track.title)
    } catch (error) {
      console.error('Failed to play track:', error)
      throw error
    }
  }

  pause() {
    this.player?.pauseVideo()
    this.isPlayingState = false
    this.stopProgressTracking()
  }

  resume() {
    this.player?.playVideo()
    this.isPlayingState = true
    this.startProgressTracking()
  }

  stop() {
    this.player?.stopVideo()
    this.isPlayingState = false
    this.stopProgressTracking()
  }

  seek(position: number) {
    this.player?.seekTo(position, true)
  }

  getPosition(): number {
    try {
      return this.player?.getCurrentTime() || 0
    } catch {
      return 0
    }
  }

  getDuration(): number {
    try {
      return this.player?.getDuration() || 0
    } catch {
      return 0
    }
  }

  setVolume(volume: number) {
    try {
      this.player?.setVolume(volume * 100)
    } catch {}
  }

  setMute(muted: boolean) {
    try {
      if (muted) {
        this.player?.mute()
      } else {
        this.player?.unmute()
      }
    } catch {}
  }

  isPlaying(): boolean {
    return this.isPlayingState
  }

  private handleTrackEnd() {
    this.stopProgressTracking()
    this.playerStore?.nextTrack()
  }

  destroy() {
    this.stopProgressTracking()
    this.player?.destroy()
    this.playerContainer?.remove()
  }
}

export const audioPlayer = new AudioPlayerService()
