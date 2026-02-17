const PIPED_API = 'https://pipedapi-libre.kavin.rocks';

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
  
  // Search endpoint
  if (url.includes('/api/search')) {
    const q = searchParams.get('q') || '';
    try {
      const response = await fetch(`${PIPED_API}/search?q=${encodeURIComponent(q)}&filter=videos`);
      const data = await response.json();
      
      const results = (data.items || []).map(item => ({
        id: item.url?.split('=')[1] || item.url?.split('/').pop() || '',
        title: item.title || 'Unknown',
        artist: item.uploaderName || 'Unknown',
        thumbnail: item.thumbnail?.[0]?.url || item.thumbnail || '',
        duration: item.duration || 0
      })).filter(item => item.id);
      
      res.status(200).json({ results });
    } catch (error) {
      res.status(200).json({ 
        results: [
          { id: 'dQw4w9WgXcQ', title: `${q} - Demo`, artist: 'Demo Artist', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 180 }
        ]
      });
    }
    return;
  }
  
  // Stream endpoint
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    try {
      const response = await fetch(`${PIPED_API}/streams/${videoId}`);
      const data = await response.json();
      
      const audioStreams = data.audioStreams || [];
      const bestAudio = audioStreams.find(s => s.quality === '128kbps') || audioStreams[0];
      
      res.status(200).json({
        video_id: videoId,
        audio_url: bestAudio?.url || null,
        title: data.title,
        thumbnail: data.thumbnailUrl
      });
    } catch (error) {
      res.status(500).json({ error: 'Failed to get stream' });
    }
    return;
  }
  
  // Trending
  if (url.includes('/api/trending')) {
    try {
      const response = await fetch(`${PIPED_API}/trending`);
      const data = await response.json();
      
      const results = (data || []).slice(0, 20).map(item => ({
        id: item.url?.split('=')[1] || item.url?.split('/').pop() || '',
        title: item.title || 'Unknown',
        artist: item.uploaderName || 'Unknown',
        thumbnail: item.thumbnail?.[0]?.url || item.thumbnail || '',
        duration: item.duration || 0
      })).filter(item => item.id);
      
      res.status(200).json({ results });
    } catch (error) {
      res.status(200).json({ 
        results: [
          { id: 'dQw4w9WgXcQ', title: 'Never Gonna Give You Up', artist: 'Rick Astley', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 213 }
        ]
      });
    }
    return;
  }
  
  // Playlists
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
    version: '2.1.0',
    backend: 'piped-libre'
  });
}
