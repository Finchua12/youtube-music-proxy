const PIPED_API = 'https://pipedapi-libre.kavin.rocks';

const DEMO_TRENDING = [
  { id: 'dQw4w9WgXcQ', title: 'Never Gonna Give You Up', artist: 'Rick Astley', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 213 },
  { id: 'JGwWNGJdvx8', title: 'Ed Sheeran - Shape of You', artist: 'Ed Sheeran', thumbnail: 'https://i.ytimg.com/vi/JGwWNGJdvx8/mqdefault.jpg', duration: 233 },
  { id: 'kJQP7kiw5Fk', title: 'Luis Fonsi - Despacito', artist: 'Luis Fonsi', thumbnail: 'https://i.ytimg.com/vi/kJQP7kiw5Fk/mqdefault.jpg', duration: 282 },
  { id: '2Vv-BfVoq4g', title: 'Ed Sheeran - Perfect', artist: 'Ed Sheeran', thumbnail: 'https://i.ytimg.com/vi/2Vv-BfVoq4g/mqdefault.jpg', duration: 263 },
  { id: 'RgKAFK5djSk', title: 'Wiz Khalifa - See You Again', artist: 'Wiz Khalifa', thumbnail: 'https://i.ytimg.com/vi/RgKAFK5djSk/mqdefault.jpg', duration: 237 },
  { id: 'lXMskKTw3Bc', title: 'Katy Perry - Roar', artist: 'Katy Perry', thumbnail: 'https://i.ytimg.com/vi/lXMskKTw3Bc/mqdefault.jpg', duration: 269 },
  { id: 'CevxZvSJLk8', title: 'Miley Cyrus - Wrecking Ball', artist: 'Miley Cyrus', thumbnail: 'https://i.ytimg.com/vi/CevxZvSJLk8/mqdefault.jpg', duration: 351 },
  { id: 'hT_nvWreIhg', title: 'Katy Perry - Firework', artist: 'Katy Perry', thumbnail: 'https://i.ytimg.com/vi/hT_nvWreIhg/mqdefault.jpg', duration: 237 },
];

const DEMO_SEARCH = {
  'music': DEMO_TRENDING,
  'rock': [
    { id: '4cQr66HQco0', title: 'Queen - Bohemian Rhapsody', artist: 'Queen', thumbnail: 'https://i.ytimg.com/vi/4cQr66HQco0/mqdefault.jpg', duration: 354 },
    { id: 'fJ9rUzIMcZQ', title: 'Queen - Another One Bites The Dust', artist: 'Queen', thumbnail: 'https://i.ytimg.com/vi/fJ9rUzIMcZQ/mqdefault.jpg', duration: 215 },
    { id: 'hT_nvWreIhg', title: 'Nirvana - Smells Like Teen Spirit', artist: 'Nirvana', thumbnail: 'https://i.ytimg.com/vi/hT_nvWreIhg/mqdefault.jpg', duration: 284 },
  ],
  'pop': [
    { id: 'JGwWNGJdvx8', title: 'Adele - Hello', artist: 'Adele', thumbnail: 'https://i.ytimg.com/vi/JGwWNGJdvx8/mqdefault.jpg', duration: 367 },
    { id: 'YQHsXMglC9A', title: 'Taylor Swift - Blank Space', artist: 'Taylor Swift', thumbnail: 'https://i.ytimg.com/vi/YQHsXMglC9A/mqdefault.jpg', duration: 274 },
  ]
};

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
    const query = q.toLowerCase();
    
    // Try Piped first
    try {
      const response = await fetch(`${PIPED_API}/search?q=${encodeURIComponent(q)}&filter=videos`, {
        signal: AbortSignal.timeout(3000)
      });
      if (response.ok) {
        const data = await response.json();
        const results = (data.items || []).slice(0, 10).map((item: any) => ({
          id: item.url?.split('=')[1] || '',
          title: item.title || 'Unknown',
          artist: item.uploaderName || 'Unknown',
          thumbnail: item.thumbnail?.[0]?.url || '',
          duration: item.duration || 0
        })).filter((item: any) => item.id);
        
        if (results.length > 0) {
          res.status(200).json({ results, source: 'piped' });
          return;
        }
      }
    } catch (e) {
      console.log('Piped search failed, using demo data');
    }
    
    // Fallback to demo data
    const demoResults = DEMO_SEARCH[query as keyof typeof DEMO_SEARCH] || 
      DEMO_SEARCH['music'].map(t => ({ ...t, title: `${q} - ${t.title}` }));
    
    res.status(200).json({ results: demoResults.slice(0, 10), source: 'demo' });
    return;
  }
  
  // Stream endpoint
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    
    try {
      const response = await fetch(`${PIPED_API}/streams/${videoId}`, {
        signal: AbortSignal.timeout(3000)
      });
      if (response.ok) {
        const data = await response.json();
        const audioStreams = data.audioStreams || [];
        const bestAudio = audioStreams.find((s: any) => s.quality === '128kbps') || audioStreams[0];
        
        if (bestAudio?.url) {
          res.status(200).json({
            video_id: videoId,
            audio_url: bestAudio.url,
            title: data.title,
            thumbnail: data.thumbnailUrl,
            source: 'piped'
          });
          return;
        }
      }
    } catch (e) {
      console.log('Piped stream failed');
    }
    
    // Fallback - return demo stream URL
    res.status(200).json({
      video_id: videoId,
      audio_url: null,
      title: 'Demo Track',
      thumbnail: `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`,
      source: 'demo',
      note: 'Piped unavailable - audio streaming disabled'
    });
    return;
  }
  
  // Trending
  if (url.includes('/api/trending')) {
    try {
      const response = await fetch(`${PIPED_API}/trending`, {
        signal: AbortSignal.timeout(3000)
      });
      if (response.ok) {
        const data = await response.json();
        const results = (data || []).slice(0, 20).map((item: any) => ({
          id: item.url?.split('=')[1] || '',
          title: item.title || 'Unknown',
          artist: item.uploaderName || 'Unknown',
          thumbnail: item.thumbnail?.[0]?.url || '',
          duration: item.duration || 0
        })).filter((item: any) => item.id);
        
        if (results.length > 0) {
          res.status(200).json({ results, source: 'piped' });
          return;
        }
      }
    } catch (e) {
      console.log('Piped trending failed');
    }
    
    res.status(200).json({ results: DEMO_TRENDING, source: 'demo' });
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
    version: '2.2.0',
    sources: ['piped (primary)', 'demo (fallback)']
  });
}
