export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const url = req.url || '';
  
  // Search endpoint
  if (url.includes('/api/search')) {
    const urlObj = new URL(url, 'https://example.com');
    const q = urlObj.searchParams.get('q') || '';
    
    // Use mock data for now
    const mockResults = [
      { id: 'dQw4w9WgXcQ', title: `${q} - Song 1`, artist: 'Artist 1', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 180 },
      { id: 'test2', title: `${q} - Song 2`, artist: 'Artist 2', thumbnail: '', duration: 240 },
      { id: 'test3', title: `${q} - Song 3`, artist: 'Artist 3', thumbnail: '', duration: 200 }
    ];
    
    res.status(200).json({ results: mockResults });
    return;
  }
  
  // Playlists
  if (url.includes('/api/playlists')) {
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
  
  // Stream
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    res.status(200).json({
      video_id: videoId,
      audio_url: `https://rr1---sn-4g5e6nsd.googlevideo.com/...`
    });
    return;
  }
  
  // Root
  res.status(200).json({ 
    status: 'ok', 
    message: 'YouTube Music Proxy API',
    version: '1.0.0'
  });
}
