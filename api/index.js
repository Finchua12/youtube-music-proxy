const YOUTUBE_API_KEY = 'AIzaSyD9jUj4E5KyF6h7kd1GeFj8dR63HCmKmKg';
const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3';

function parseDuration(durationStr) {
  if (!durationStr) return 0;
  const match = durationStr.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
  if (!match) return 0;
  const hours = parseInt(match[1]) || 0;
  const minutes = parseInt(match[2]) || 0;
  const seconds = parseInt(match[3]) || 0;
  return hours * 3600 + minutes * 60 + seconds;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const url = req.url || '';
  
  // Search - only videos with duration
  if (url.includes('/api/search')) {
    const q = new URL(url, 'https://example.com').searchParams.get('q') || '';
    
    try {
      const searchResponse = await fetch(
        `${YOUTUBE_API_BASE}/search?part=snippet&type=video&q=${encodeURIComponent(q)}&maxResults=15&key=${YOUTUBE_API_KEY}`
      );
      const searchData = await searchResponse.json();
      
      const videoIds = (searchData.items || []).map(item => item.id.videoId).join(',');
      
      const detailsResponse = await fetch(
        `${YOUTUBE_API_BASE}/videos?part=snippet,contentDetails&id=${videoIds}&key=${YOUTUBE_API_KEY}`
      );
      const detailsData = await detailsResponse.json();
      
      const detailsMap = {};
      (detailsData.items || []).forEach(item => {
        detailsMap[item.id] = item;
      });
      
      // Filter: only videos with duration (no live streams)
      const results = (searchData.items || [])
        .filter(item => {
          const details = detailsMap[item.id.videoId];
          const duration = details ? parseDuration(details.contentDetails?.duration) : 0;
          return duration > 0; // Only videos with known duration
        })
        .map(item => {
          const details = detailsMap[item.id.videoId];
          return {
            id: item.id.videoId,
            title: item.snippet.title,
            artist: item.snippet.channelTitle,
            thumbnail: item.snippet.thumbnails?.medium?.url || item.snippet.thumbnails?.default?.url || '',
            duration: details ? parseDuration(details.contentDetails?.duration) : 0
          };
        });
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Search error:', error);
      res.status(500).json({ error: 'Search failed' });
    }
    return;
  }
  
  // Trending - only music videos
  if (url.includes('/api/trending')) {
    try {
      // Use music category (10)
      const response = await fetch(
        `${YOUTUBE_API_BASE}/videos?part=snippet,contentDetails&chart=mostPopular&regionCode=US&videoCategoryId=10&maxResults=20&key=${YOUTUBE_API_KEY}`
      );
      const data = await response.json();
      
      // Filter: only videos with duration
      const results = (data.items || [])
        .filter(item => {
          const duration = parseDuration(item.contentDetails?.duration);
          return duration > 0;
        })
        .map(item => ({
          id: item.id,
          title: item.snippet.title,
          artist: item.snippet.channelTitle,
          thumbnail: item.snippet.thumbnails?.medium?.url || '',
          duration: parseDuration(item.contentDetails?.duration)
        }));
      
      res.status(200).json({ results });
    } catch (error) {
      console.error('Trending error:', error);
      res.status(500).json({ error: 'Trending failed' });
    }
    return;
  }
  
  // Stream with duration
  if (url.includes('/api/stream/')) {
    const videoId = url.split('/api/stream/')[1]?.split('?')[0];
    
    try {
      const response = await fetch(
        `${YOUTUBE_API_BASE}/videos?part=snippet,contentDetails&id=${videoId}&key=${YOUTUBE_API_KEY}`
      );
      const data = await response.json();
      const item = data.items?.[0];
      
      if (!item) {
        res.status(404).json({ error: 'Video not found' });
        return;
      }
      
      const duration = parseDuration(item.contentDetails?.duration);
      
      res.status(200).json({
        video_id: videoId,
        title: item.snippet.title,
        thumbnail: item.snippet.thumbnails?.medium?.url || '',
        duration: duration
      });
    } catch (error) {
      console.error('Stream error:', error);
      res.status(500).json({ error: 'Failed to get video info' });
    }
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
  
  res.status(200).json({ status: 'ok', version: '3.2.0' });
}
