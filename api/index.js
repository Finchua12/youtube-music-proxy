import fetch from 'node-fetch';

module.exports = async (req, res) => {
  const url = req.url;
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    res.end();
    return;
  }
  
  try {
    // Route: /api/search
    if (url.includes('/api/search')) {
      const urlObj = new URL(url, 'https://example.com');
      const q = urlObj.searchParams.get('q') || '';
      const maxResults = urlObj.searchParams.get('max_results') || '10';
      
      const response = await fetch(
        `https://vid.puffyan.us/api/v1/search?q=${encodeURIComponent(q)}&type=video&sort_by=relevance`
      );
      const data = await response.json();
      
      const results = data.slice(0, parseInt(maxResults)).map(item => ({
        id: item.videoId,
        title: item.title,
        artist: item.author,
        thumbnail: item.videoThumbnails?.[0]?.url || '',
        duration: item.lengthSeconds || 0
      }));
      
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ results }));
      return;
    }
    
    // Route: /api/playlists
    if (url.includes('/api/playlists')) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify([]));
      return;
    }
    
    // Route: /api/auth/url
    if (url.includes('/api/auth/url')) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ auth_url: 'https://accounts.google.com/o/oauth2/auth' }));
      return;
    }
    
    // Route: /api/auth/status
    if (url.includes('/api/auth/status')) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ authenticated: false }));
      return;
    }
    
    // Root
    if (url === '/' || url === '') {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ 
        status: 'ok', 
        message: 'YouTube Music Proxy API',
        version: '1.0.0'
      }));
      return;
    }
    
    // 404 for unknown routes
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not found' }));
    
  } catch (error) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: error.message }));
  }
};
