const PIPED_API = 'https://pipedapi.kavin.rocks';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const url = req.url || '';
  const searchParams = new URL(url, 'https://example.com').searchParams;
  
  // Search endpoint - use Piped API
  if (url.includes('/api/search')) {
    const q = searchParams.get('q') || '';
    try {
      const response = await fetch(`${PIPED_API}/search?q=${encodeURIComponent(q)}&filter=videos`);
      const data = await response.json();
      
      const results = (data.items || []).map(item => ({
        id: item.url.split('=')[1] || item.url.split('/').pop(),
        title: item.title,
        artist: item.uploaderName || item.author || 'Unknown',
        thumbnail: item.thumbnail || `https://i.ytimg.com/vi/${item.url.split('=')[1] || item.url.split('/').pop()}/mqdefault.jpg`,
        duration: item.duration || 0
      }));
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Search error:', error);
      res.status(500).json({ error: 'Search failed', results: [] });
    }
    return;
  }
  
  // Stream endpoint - get audio URL from Piped
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    try {
      const response = await fetch(`${PIPED_API}/streams/${videoId}`);
      const data = await response.json();
      
      // Find best audio stream
      const audioStreams = data.audioStreams || [];
      const bestAudio = audioStreams.find(s => s.quality === '128kbps') || audioStreams[0];
      
      res.status(200).json({
        video_id: videoId,
        audio_url: bestAudio?.url || null,
        title: data.title,
        thumbnail: data.thumbnailUrl
      });
    } catch (error) {
      console.error('Stream error:', error);
      res.status(500).json({ error: 'Failed to get stream' });
    }
    return;
  }
  
  // Trending / Home
  if (url.includes('/api/trending')) {
    try {
      const response = await fetch(`${PIPED_API}/trending`);
      const data = await response.json();
      
      const results = (data || []).slice(0, 20).map(item => ({
        id: item.url.split('=')[1] || item.url.split('/').pop(),
        title: item.title,
        artist: item.uploaderName || 'Unknown',
        thumbnail: item.thumbnail || `https://i.ytimg.com/vi/${item.url.split('=')[1] || item.url.split('/').pop()}/mqdefault.jpg`,
        duration: item.duration || 0
      }));
      
      res.status(200).json({ results });
    } catch (error) {
      res.status(500).json({ error: 'Failed to get trending', results: [] });
    }
    return;
  }
  
  // Playlists - store in memory for now
  if (url.includes('/api/playlists')) {
    res.status(200).json([]);
    return;
  }
  
  // Recently Played
  if (url.includes('/api/recently-played')) {
    res.status(200).json([]);
    return;
  }
  
  // Likes
  if (url.includes('/api/likes')) {
    res.status(200).json([]);
    return;
  }
  
  // Auth
  if (url.includes('/api/auth/url')) {
    res.status(200).json({ auth_url: 'https://accounts.google.com/o/oauth2/auth' });
    return;
  }
  
  if (url.includes('/api/auth/status')) {
    res.status(200).json({ authenticated: false });
    return;
  }
  
  // Root
  res.status(200).json({ 
    status: 'ok', 
    message: 'YouTube Music Proxy API',
    version: '2.0.0',
    backend: 'piped'
  });
}
