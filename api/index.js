const YOUTUBE_API_KEY = 'AIzaSyD9jUj4E5KyF6h7kd1GeFj8dR63HCmKmKg';
const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const url = req.url || '';
  
  // Search
  if (url.includes('/api/search')) {
    const q = new URL(url, 'https://example.com').searchParams.get('q') || '';
    
    try {
      const response = await fetch(
        `${YOUTUBE_API_BASE}/search?part=snippet&type=video&q=${encodeURIComponent(q)}&maxResults=20&key=${YOUTUBE_API_KEY}`
      );
      const data = await response.json();
      
      const results = (data.items || []).map(item => ({
        id: item.id.videoId,
        title: item.snippet.title,
        artist: item.snippet.channelTitle,
        thumbnail: item.snippet.thumbnails?.medium?.url || item.snippet.thumbnails?.default?.url || '',
        duration: 0
      }));
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Search error:', error);
      res.status(500).json({ error: 'Search failed' });
    }
    return;
  }
  
  // Trending - using mostPopular
  if (url.includes('/api/trending')) {
    try {
      const response = await fetch(
        `${YOUTUBE_API_BASE}/videos?part=snippet,contentDetails&chart=mostPopular&regionCode=US&maxResults=20&key=${YOUTUBE_API_KEY}`
      );
      const data = await response.json();
      
      const results = (data.items || []).map(item => ({
        id: item.id,
        title: item.snippet.title,
        artist: item.snippet.channelTitle,
        thumbnail: item.snippet.thumbnails?.medium?.url || '',
        duration: 0
      }));
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Trending error:', error);
      res.status(500).json({ error: 'Trending failed' });
    }
    return;
  }
  
  // Stream - get video details for duration
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    
    try {
      const response = await fetch(
        `${YOUTUBE_API_BASE}/videos?part=snippet,contentDetails&id=${videoId}&key=${YOUTUBE_API_KEY}`
      );
      const data = await response.json();
      const item = data.items?.[0];
      
      if (!item) {
        res.status(404).json({ error: 'Video not found' });
        return;
      }
      
      // Parse ISO 8601 duration
      const durationStr = item.contentDetails?.duration || 'PT0M0S';
      const match = durationStr.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
      const hours = parseInt(match?.[1] || '0') || 0;
      const minutes = parseInt(match?.[2] || '0') || 0;
      const seconds = parseInt(match?.[3] || '0') || 0;
      const duration = hours * 3600 + minutes * 60 + seconds;
      
      res.status(200).json({
        video_id: videoId,
        audio_url: null,
        title: item.snippet.title,
        thumbnail: item.snippet.thumbnails?.medium?.url || '',
        duration: duration,
        note: 'Use frontend player with YouTube embeds'
      });
    } catch (error) {
      console.error('Stream error:', error);
      res.status(500).json({ error: 'Failed to get video info' });
    }
    return;
  }
  
  // Playlists
  if (url.includes('/api/playlists') || url.includes('/api/recently-played') || url.includes('/api/likes')) {
    res.status(200).json([]);
    return;
  }
  
  // Auth status
  if (url.includes('/api/auth/status')) {
    res.status(200).json({ authenticated: false });
    return;
  }
  
  res.status(200).json({ status: 'ok', version: '3.0.0', source: 'youtube-data-api' });
}
