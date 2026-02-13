import { downloadApi } from '@/services/api'

class DownloadService {
  private downloadQueue: Map<string, Promise<string>> = new Map()
  private downloadCache: Map<string, string> = new Map()

  // Download audio file and return URL
  async downloadAudio(videoId: string, quality: string = '192k'): Promise<string> {
    // Check if already downloading
    if (this.downloadQueue.has(videoId)) {
      return this.downloadQueue.get(videoId)!
    }

    // Check if already downloaded
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

  // Perform actual download
  private async performDownload(videoId: string, quality: string): Promise<string> {
    try {
      // In a real implementation, this would:
      // 1. Call the backend API to start download
      // 2. Wait for download completion
      // 3. Return a URL to the downloaded file

      // For now, we'll simulate with a mock URL
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate download time
      return `http://127.0.0.1:8000/audio/${videoId}_${quality}.mp3`
    } catch (error) {
      console.error('Download failed:', error)
      throw new Error('Failed to download audio')
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
    // In a real implementation, this would cancel the backend download
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