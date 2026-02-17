class DownloadService {
  private cache: Map<string, any> = new Map()

  async getVideoInfo(videoId: string): Promise<any> {
    if (this.cache.has(videoId)) {
      return this.cache.get(videoId)
    }

    try {
      const response = await fetch(`/api/stream/${videoId}`)
      const data = await response.json()
      this.cache.set(videoId, data)
      return data
    } catch (error) {
      console.error('Failed to get video info:', error)
      throw error
    }
  }

  async downloadAudio(videoId: string): Promise<string | null> {
    const info = await this.getVideoInfo(videoId)
    return info.audio_url || null
  }

  clearCache() {
    this.cache.clear()
  }
}

export const downloadService = new DownloadService()
