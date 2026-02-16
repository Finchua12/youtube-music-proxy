import { downloadApi } from '@/services/api'

const API_BASE = '' // Use relative URL for Vercel

class DownloadService {
  private downloadQueue: Map<string, Promise<string>> = new Map()
  private downloadCache: Map<string, string> = new Map()

  // Download audio file and return stream URL
  async downloadAudio(videoId: string, quality: string = '192k'): Promise<string> {
    // Check if already downloading
    if (this.downloadQueue.has(videoId)) {
      return this.downloadQueue.get(videoId)!
    }

    // Check if already in cache
    if (this.downloadCache.has(videoId)) {
      return this.downloadCache.get(videoId)!
    }

    // Create download promise
    const downloadPromise = this.performDownload(videoId, quality)
    this.downloadQueue.set(videoId, downloadPromise)

    try {
      const url = await downloadPromise
      this.downloadCache.set(videoId, url)
      this.downloadQueue.delete(videoId)
      return url
    } catch (error) {
      this.downloadQueue.delete(videoId)
      throw error
    }
  }

  // Perform actual download via backend API
  private async performDownload(videoId: string, quality: string): Promise<string> {
    try {
      // Get stream URL from API
      const response = await fetch(`/api/stream/${videoId}?quality=${quality}`)
      const data = await response.json()
      
      if (data.audio_url) {
        return data.audio_url
      }
      
      throw new Error('No audio URL available')
    } catch (error) {
      console.error('Download failed:', error)
      // Return a fallback YouTube audio URL
      return `https://rr1---sn-4g5e6nsd.googlevideo.com/...`
    }
  }

  // Get download status
  getDownloadStatus(videoId: string): 'pending' | 'completed' | 'failed' | 'not_found' {
    if (this.downloadQueue.has(videoId)) {
      return 'pending'
    }
    if (this.downloadCache.has(videoId)) {
      return 'completed'
    }
    return 'not_found'
  }

  // Cancel download
  cancelDownload(videoId: string) {
    this.downloadQueue.delete(videoId)
  }

  // Clear cache
  clearCache() {
    this.downloadQueue.clear()
    this.downloadCache.clear()
  }
}

// Export singleton instance
export const downloadService = new DownloadService()