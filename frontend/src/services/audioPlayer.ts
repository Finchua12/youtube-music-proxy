import { usePlayerStore } from '@/stores/player'

class AudioPlayerService {
  private player: YT.Player | null = null
  private playerContainer: HTMLDivElement | null = null
  private _playerStore: ReturnType<typeof usePlayerStore> | null = null
  private isReady = false

  private get playerStore() {
    if (!this._playerStore) {
      this._playerStore = usePlayerStore()
    }
    return this._playerStore
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
        },
        onStateChange: (event: any) => {
          if (event.data === (window as any).YT.PlayerState.ENDED) {
            this.handleTrackEnd()
          }
        }
      }
    })
  }

  async playTrack(track: any) {
    if (!this.isReady || !this.player) {
      console.error('Player not ready')
      throw new Error('Player not ready')
    }

    try {
      await this.player.loadVideoById({
        videoId: track.id,
        startSeconds: 0
      })
      console.log('Playing:', track.title)
    } catch (error) {
      console.error('Failed to play track:', error)
      throw error
    }
  }

  pause() {
    this.player?.pauseVideo()
  }

  resume() {
    this.player?.playVideo()
  }

  stop() {
    this.player?.stopVideo()
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
    return this.player?.getPlayerState() === 1
  }

  private handleTrackEnd() {
    this.playerStore.nextTrack()
  }

  destroy() {
    this.player?.destroy()
    this.playerContainer?.remove()
  }
}

export const audioPlayer = new AudioPlayerService()
