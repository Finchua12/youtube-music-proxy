const PIPED_INSTANCES = [
  'https://pipedapi.kavin.rocks',
  'https://api.piped.yt',
  'https://pipedapi-libre.kavin.rocks',
  'https://watchapi.whatever.social'
];

async function fetchPiped(endpoint: string): Promise<any> {
  let lastError: Error | null = null;
  
  for (const baseUrl of PIPED_INSTANCES) {
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        signal: AbortSignal.timeout(5000)
      });
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      lastError = error as Error;
      console.log(`Failed to fetch from ${baseUrl}:`, error);
    }
  }
  
  throw lastError || new Error('All Piped instances failed');
}

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
      const data = await fetchPiped(`/search?q=${encodeURIComponent(q)}&filter=videos`);
      
      const results = (data.items || []).map((item: any) => ({
        id: item.url?.split('=')[1] || item.url?.split('/').pop() || '',
        title: item.title || 'Unknown',
        artist: item.uploaderName || item.author || 'Unknown',
        thumbnail: item.thumbnail?.[0]?.url || item.thumbnail || '',
        duration: item.duration || 0
      })).filter((item: any) => item.id);
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Search error:', error);
      res.status(200).json({ 
        error: 'Search temporarily unavailable',
        results: [
          { id: 'dQw4w9WgXcQ', title: `${q} - Rick Astley`, artist: 'Rick Astley', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 213 }
        ]
      });
    }
    return;
  }
  
  // Stream endpoint
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    try {
      const data = await fetchPiped(`/streams/${videoId}`);
      
      const audioStreams = data.audioStreams || [];
      const bestAudio = audioStreams.find((s: any) => s.quality === '128kbps') || audioStreams[0];
      
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
  
  // Trending
  if (url.includes('/api/trending')) {
    try {
      const data = await fetchPiped('/trending');
      
      const results = (data || []).slice(0, 20).map((item: any) => ({
        id: item.url?.split('=')[1] || item.url?.split('/').pop() || '',
        title: item.title || 'Unknown',
        artist: item.uploaderName || 'Unknown',
        thumbnail: item.thumbnail?.[0]?.url || item.thumbnail || '',
        duration: item.duration || 0
      })).filter((item: any) => item.id);
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Trending error:', error);
      res.status(200).json({ 
        error: 'Trending unavailable',
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
    backend: 'piped'
  });
}
