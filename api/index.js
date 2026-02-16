export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  // Return mock data for testing
  res.status(200).json({
    results: [
      { id: 'test1', title: 'Test Song 1', artist: 'Artist 1', thumbnail: '', duration: 180 },
      { id: 'test2', title: 'Test Song 2', artist: 'Artist 2', thumbnail: '', duration: 240 },
      { id: 'test3', title: 'Test Song 3', artist: 'Artist 3', thumbnail: '', duration: 200 }
    ]
  });
}
