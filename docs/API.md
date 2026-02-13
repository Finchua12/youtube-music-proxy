# YouTube Music Proxy API Документація

## Огляд

YouTube Music Proxy API надає RESTful інтерфейс для взаємодії з додатком, включаючи пошук, завантаження, стрімінг аудіо, управління плейлистами та рекомендаціями.

Базова URL: `http://127.0.0.1:8000/api/`

## Аутентифікація

Деякі ендпоінти вимагають аутентифікації через YouTube OAuth2. Для цього необхідно отримати авторизаційний токен.

### Отримання URL для авторизації

```http
GET /api/auth/url
```

**Відповідь:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/auth?client_id=..."
}
```

### Callback після авторизації

```http
GET /api/auth/callback?code=AUTH_CODE&state=STATE_TOKEN
```

### Перевірка статусу авторизації

```http
GET /api/auth/status
```

**Відповідь:**
```json
{
  "authenticated": true
}
```

## Пошук

### Пошук відео

```http
GET /api/search?query=QUERY&max_results=10
```

**Параметри:**
- `query` (обов'язковий): Пошуковий запит
- `max_results` (необов'язковий): Максимальна кількість результатів (за замовчуванням: 10)

**Відповідь:**
```json
{
  "results": [
    {
      "id": "VIDEO_ID",
      "title": "Назва відео",
      "duration": 240,
      "uploader": "Назва каналу",
      "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
      "view_count": 1000000,
      "upload_date": "20231201",
      "description": "Опис відео"
    }
  ]
}
```

## Завантаження та стрімінг

### Запит на завантаження аудіо

```http
POST /api/download
Content-Type: application/json

{
  "video_id": "VIDEO_ID",
  "quality": "192k"
}
```

**Параметри:**
- `video_id` (обов'язковий): ID YouTube відео
- `quality` (необов'язковий): Якість аудіо (за замовчуванням: "192k")

**Відповідь:**
```json
{
  "status": "started",
  "video_id": "VIDEO_ID",
  "quality": "192k"
}
```

Або якщо файл вже закешований:
```json
{
  "status": "cached",
  "video_id": "VIDEO_ID",
  "quality": "192k",
  "path": "VIDEO_ID_192k.mp3"
}
```

### Стрімінг аудіо

```http
GET /api/stream/VIDEO_ID?quality=192k
```

**Параметри:**
- `quality` (необов'язковий): Якість аудіо (за замовчуванням: "192k")

**Відповідь:**
- Потік аудіофайлу у форматі MP3

## Плейлисти

### Отримання всіх плейлистів

```http
GET /api/playlists
```

**Відповідь:**
```json
[
  {
    "id": 1,
    "name": "Мій плейлист",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "item_count": 15
  }
]
```

### Створення нового плейлиста

```http
POST /api/playlists
Content-Type: application/json

{
  "name": "Назва плейлиста"
}
```

**Відповідь:**
```json
{
  "id": 2,
  "name": "Назва плейлиста",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "item_count": 0
}
```

### Видалення плейлиста

```http
DELETE /api/playlists/PLAYLIST_ID
```

**Відповідь:**
```json
true
```

### Отримання треків плейлиста

```http
GET /api/playlists/PLAYLIST_ID
```

**Відповідь:**
```json
[
  {
    "id": 1,
    "playlist_id": 1,
    "video_id": "VIDEO_ID",
    "title": "Назва треку",
    "duration": 240,
    "added_at": "2024-01-15T10:30:00"
  }
]
```

### Додавання треку до плейлиста

```http
POST /api/playlists/PLAYLIST_ID/items
Content-Type: application/json

{
  "video_id": "VIDEO_ID",
  "title": "Назва треку",
  "duration": 240
}
```

**Відповідь:**
```json
true
```

### Видалення треку з плейлиста

```http
DELETE /api/playlists/PLAYLIST_ID/items/VIDEO_ID
```

**Відповідь:**
```json
true
```

## Нещодавно прослухані

### Отримання нещодавно прослуханих треків

```http
GET /api/recently-played?limit=20
```

**Параметри:**
- `limit` (необов'язковий): Максимальна кількість треків (за замовчуванням: 20)

**Відповідь:**
```json
[
  {
    "id": 1,
    "video_id": "VIDEO_ID",
    "title": "Назва треку",
    "played_at": "2024-01-15T10:30:00"
  }
]
```

### Додавання до нещодавно прослуханих

```http
POST /api/recently-played
Content-Type: application/json

{
  "video_id": "VIDEO_ID",
  "title": "Назва треку",
  "duration": 240
}
```

**Відповідь:**
```json
true
```

## Улюблені треки

### Додавання до улюблених

```http
POST /api/likes
Content-Type: application/json

{
  "video_id": "VIDEO_ID",
  "title": "Назва треку"
}
```

**Відповідь:**
```json
true
```

### Видалення з улюблених

```http
DELETE /api/likes/VIDEO_ID
```

**Відповідь:**
```json
true
```

### Отримання улюблених треків

```http
GET /api/likes?limit=100
```

**Параметри:**
- `limit` (необов'язковий): Максимальна кількість треків (за замовчуванням: 100)

**Відповідь:**
```json
[
  {
    "id": 1,
    "video_id": "VIDEO_ID",
    "title": "Назва треку",
    "added_at": "2024-01-15T10:30:00"
  }
]
```

### Перевірка, чи трек улюблений

```http
GET /api/likes/VIDEO_ID
```

**Відповідь:**
```json
true
```

## Рекомендації

### Отримання персоналізованих рекомендацій

```http
GET /api/recommendations?limit=20
```

**Параметри:**
- `limit` (необов'язковий): Максимальна кількість рекомендацій (за замовчуванням: 20)

**Відповідь:**
```json
[
  {
    "id": "VIDEO_ID",
    "title": "Назва відео",
    "duration": 240,
    "uploader": "Назва каналу",
    "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
    "view_count": 1000000,
    "upload_date": "20231201"
  }
]
```

### Отримання рекомендацій для відкриття

```http
GET /api/recommendations/discovery?limit=10
```

**Параметри:**
- `limit` (необов'язковий): Максимальна кількість рекомендацій (за замовчуванням: 10)

**Відповідь:**
```json
[
  {
    "id": "VIDEO_ID",
    "title": "Назва відео",
    "duration": 240,
    "uploader": "Назва каналу",
    "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
    "view_count": 1000000,
    "upload_date": "20231201"
  }
]
```

## Управління кешем

### Отримання статистики кешу

```http
GET /api/cache/stats
```

**Відповідь:**
```json
{
  "size_bytes": 1256789012,
  "size_gb": 1.25,
  "max_size_gb": 5.0,
  "file_count": 42,
  "directory": "/home/user/.cache/youtube-music"
}
```

### Очищення старих файлів кешу

```http
POST /api/cache/cleanup
```

**Відповідь:**
```json
5  // Кількість видалених файлів
```

### Повне очищення кешу

```http
POST /api/cache/clear
```

**Відповідь:**
```json
true
```

## Налаштування користувача

### Встановлення налаштування

```http
POST /api/preferences
Content-Type: application/json

{
  "key": "theme",
  "value": "dark"
}
```

**Відповідь:**
```json
true
```

### Отримання налаштування

```http
GET /api/preferences?key=theme
```

**Відповідь:**
```json
{
  "theme": "dark"
}
```

### Отримання всіх налаштувань

```http
GET /api/preferences
```

**Відповідь:**
```json
{
  "theme": "dark",
  "language": "uk",
  "audio_quality": "192k",
  "auto_cleanup": true
}
```

## Коди стану HTTP

- `200 OK`: Успішний запит
- `201 Created`: Ресурс успішно створений
- `400 Bad Request`: Неправильний запит
- `401 Unauthorized`: Необхідна аутентифікація
- `404 Not Found`: Ресурс не знайдений
- `500 Internal Server Error`: Внутрішня помилка сервера

## Обробка помилок

Всі помилки повертаються у форматі JSON:

```json
{
  "detail": "Опис помилки"
}
```

## Приклад використання

### JavaScript (з використанням fetch)

```javascript
// Пошук треків
async function searchTracks(query) {
  const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
  const data = await response.json();
  return data.results;
}

// Завантаження аудіо
async function downloadAudio(videoId) {
  const response = await fetch('/api/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      video_id: videoId,
      quality: '192k'
    })
  });
  return await response.json();
}

// Створення плейлиста
async function createPlaylist(name) {
  const response = await fetch('/api/playlists', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name })
  });
  return await response.json();
}
```

### Python (з використанням requests)

```python
import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# Пошук треків
def search_tracks(query, max_results=10):
    response = requests.get(f'{BASE_URL}/search', params={
        'query': query,
        'max_results': max_results
    })
    return response.json()['results']

# Завантаження аудіо
def download_audio(video_id, quality='192k'):
    response = requests.post(f'{BASE_URL}/download', json={
        'video_id': video_id,
        'quality': quality
    })
    return response.json()

# Створення плейлиста
def create_playlist(name):
    response = requests.post(f'{BASE_URL}/playlists', json={'name': name})
    return response.json()
```

## Обмеження

- Максимальна кількість одночасних завантажень: 3 (налаштовується)
- Максимальний розмір кешу: 5 ГБ (налаштовується)
- Максимальна тривалість відео для завантаження: 2 години