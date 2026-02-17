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
  private isPlaying = false

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
    this.playerContainer.style.display = 'none'
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
    
    this.player = new (window as any).YT.Player(this.playerContainer, {
      height: '0',
      width: '0',
      playerVars: {
        autoplay: 1,
        controls: 0,
        disablekb: 1,
        fs: 0,
        modestbranding: 1,
        rel: 0,
        showinfo: 0,
        iv_load_policy: 3
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
            this.isPlaying = true
          } else if (event.data === YT.PlayerState.PAUSED || event.data === YT.PlayerState.ENDED) {
            this.isPlaying = false
            if (event.data === YT.PlayerState.ENDED) {
              this.handleTrackEnd()
            }
          }
        }
      }
    })
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
      this.isPlaying = true
      console.log('Playing:', track.title)
    } catch (error) {
      console.error('Failed to play track:', error)
      throw error
    }
  }

  pause() {
    this.player?.pauseVideo()
    this.isPlaying = false
  }

  resume() {
    this.player?.playVideo()
    this.isPlaying = true
  }

  stop() {
    this.player?.stopVideo()
    this.isPlaying = false
  }

  seek(position: number) {
    this.player?.seekTo(position, true)
  }

  getPosition(): number {
    return this.player?.getCurrentTime() || 0
  }

  getDuration(): number {
    return this.player?.getDuration() || 0
  }

  setVolume(volume: number) {
    this.player?.setVolume(volume * 100)
  }

  setMute(muted: boolean) {
    if (muted) {
      this.player?.mute()
    } else {
      this.player?.unmute()
    }
  }

  isPlaying(): boolean {
    return this.isPlaying
  }

  private handleTrackEnd() {
    this.playerStore?.nextTrack()
  }

  destroy() {
    this.player?.destroy()
    this.playerContainer?.remove()
  }
}

export const audioPlayer = new AudioPlayerService()
