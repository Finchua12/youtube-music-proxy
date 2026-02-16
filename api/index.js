module.exports = async (req, res) => {
  const url = req.url;
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    res.end();
    return;
  }
  
  try {
    // Search endpoint
    if (url.includes('/api/search')) {
      const urlObj = new URL(url, 'https://example.com');
      const q = urlObj.searchParams.get('q') || '';
      const maxResults = parseInt(urlObj.searchParams.get('max_results') || '10');
      
      // Use Invidious API (no API key needed)
      const response = await fetch(
        `https://vid.puffyan.us/api/v1/search?q=${encodeURIComponent(q)}&type=video&limit=${maxResults}`
      );
      const data = await response.json();
      
      const results = data
        .filter(item => item.type === 'video')
        .slice(0, maxResults)
        .map(item => ({
          id: item.videoId,
          title: item.title,
          artist: item.author,
          thumbnail: item.videoThumbnails?.[0]?.url || '',
          duration: parseInt(item.lengthSeconds) || 0
        }));
      
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ results }));
      return;
    }
    
    // Playlists
    if (url.includes('/api/playlists') && req.method === 'GET') {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify([]));
      return;
    }
    
    // Auth
    if (url.includes('/api/auth/url')) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ auth_url: 'https://accounts.google.com/o/oauth2/auth' }));
      return;
    }
    
    if (url.includes('/api/auth/status')) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ authenticated: false }));
      return;
    }
    
    // Stream URL
    if (url.includes('/api/stream/')) {
      const videoId = url.split('/api/stream/')[1]?.split('?')[0];
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({
        video_id: videoId,
        audio_url: `https://vid.puffyan.us/latest_version?id=${videoId}&itag=140`
      }));
      return;
    }
    
    // Root API
    if (url === '/api' || url === '/api/') {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ 
        status: 'ok', 
        message: 'YouTube Music Proxy API',
        endpoints: ['/api/search', '/api/playlists', '/api/auth/url', '/api/auth/status', '/api/stream/:id']
      }));
      return;
    }
    
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not found' }));
    
  } catch (error) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: error.message }));
  }
};
