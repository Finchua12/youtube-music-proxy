import { downloadApi } from '@/services/api'

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
      // Start download on backend
      const response = await downloadApi.download(videoId, quality) as { status: string; video_id: string; quality: string }
      
      if (response.status === 'cached') {
        // File already cached, return stream URL
        return `http://127.0.0.1:8000/api/stream/${videoId}?quality=${quality}`
      }
      
      if (response.status === 'started') {
        // Download started, wait for it to complete
        await this.waitForDownload(videoId, quality)
        return `http://127.0.0.1:8000/api/stream/${videoId}?quality=${quality}`
      }
      
      throw new Error(`Unexpected download status: ${response.status}`)
    } catch (error) {
      console.error('Download failed:', error)
      throw new Error('Failed to download audio')
    }
  }

  // Poll backend to check if download is complete
  private async waitForDownload(videoId: string, quality: string, maxAttempts: number = 30): Promise<void> {
    const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))
    
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      await delay(1000) // Wait 1 second between checks
      
      try {
        // Try to access stream endpoint - if successful, download is complete
        const response = await fetch(`http://127.0.0.1:8000/api/stream/${videoId}?quality=${quality}`, {
          method: 'HEAD'
        })
        
        if (response.ok) {
          return // Download complete
        }
      } catch (error) {
        // Continue polling
      }
    }
    
    throw new Error('Download timeout')
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