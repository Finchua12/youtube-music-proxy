export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  const url = req.url || '';
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
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
      
      res.status(200).json({ results });
      return;
    }
    
    // Root
    res.status(200).json({ status: 'ok' });
    
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
}
