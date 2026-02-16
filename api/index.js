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
  
  // Test endpoint
  if (url === '/api/test') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ test: 'ok' }));
    return;
  }
  
  try {
    // Search endpoint
    if (url.includes('/api/search')) {
      const urlObj = new URL(url, 'https://example.com');
      const q = urlObj.searchParams.get('q') || '';
      const maxResults = parseInt(urlObj.searchParams.get('max_results') || '10');
      
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
    
    // Root API
    if (url === '/api' || url === '/api/') {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ status: 'ok' }));
      return;
    }
    
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not found' }));
    
  } catch (error) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: error.toString() }));
  }
};
