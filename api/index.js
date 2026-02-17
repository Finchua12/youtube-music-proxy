const DEMO_TRENDING = [
  { id: 'dQw4w9WgXcQ', title: 'Never Gonna Give You Up', artist: 'Rick Astley', thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg', duration: 213 },
  { id: 'JGwWNGJdvx8', title: 'Shape of You', artist: 'Ed Sheeran', thumbnail: 'https://i.ytimg.com/vi/JGwWNGJdvx8/mqdefault.jpg', duration: 233 },
  { id: 'kJQP7kiw5Fk', title: 'Despacito', artist: 'Luis Fonsi', thumbnail: 'https://i.ytimg.com/vi/kJQP7kiw5Fk/mqdefault.jpg', duration: 282 },
  { id: '2Vv-BfVoq4g', title: 'Perfect', artist: 'Ed Sheeran', thumbnail: 'https://i.ytimg.com/vi/2Vv-BfVoq4g/mqdefault.jpg', duration: 263 },
  { id: 'RgKAFK5djSk', title: 'See You Again', artist: 'Wiz Khalifa', thumbnail: 'https://i.ytimg.com/vi/RgKAFK5djSk/mqdefault.jpg', duration: 237 },
];

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const url = req.url || '';
  
  // Search
  if (url.includes('/api/search')) {
    const q = new URL(url, 'https://example.com').searchParams.get('q') || '';
    const results = DEMO_TRENDING.map(t => ({ ...t, title: `${t.title} - ${q}` }));
    res.status(200).json({ results });
    return;
  }
  
  // Trending
  if (url.includes('/api/trending')) {
    res.status(200).json({ results: DEMO_TRENDING });
    return;
  }
  
  // Stream
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1].split('?')[0];
    res.status(200).json({
      video_id: videoId,
      audio_url: null,
      title: 'Demo',
      note: 'Streaming requires Piped API'
    });
    return;
  }
  
  // Other endpoints
  if (url.includes('/api/playlists') || url.includes('/api/recently-played') || url.includes('/api/likes')) {
    res.status(200).json([]);
    return;
  }
  
  if (url.includes('/api/auth/status')) {
    res.status(200).json({ authenticated: false });
    return;
  }
  
  res.status(200).json({ status: 'ok', version: '2.2.0' });
}
