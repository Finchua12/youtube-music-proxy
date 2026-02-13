# YouTube Music Proxy

CachyOS desktop application for streaming YouTube music without ads.

## Features

- 🎵 Stream YouTube music without ads
- 📱 Native desktop app for CachyOS (Linux)
- 💾 Local playlists with SQLite
- 🗂️ Queue management
- 🔍 Search YouTube directly
- 🎛️ Media controls integration
- 📴 Offline caching
- 🎨 Modern UI

## Tech Stack

- **Frontend**: Tauri (Rust + TypeScript/Vue)
- **Backend**: Python (FastAPI)
- **Database**: SQLite
- **Media**: yt-dlp + ffmpeg
- **UI Framework**: Vue 3 + TypeScript

## Project Structure

```
youtube-music/
├── backend/           # Python backend
│   ├── src/
│   │   ├── main.py          # FastAPI app
│   │   ├── downloader.py    # yt-dlp integration
│   │   ├── cache.py         # Audio caching
│   │   └── db.py            # SQLite database
│   └── tests/
├── frontend/        # Tauri frontend
│   └── src/
│       ├── components/        # Vue components
│       ├── pages/             # App pages
│       ├── main.ts            # Entry point
│       └── App.vue            # Root component
├── docs/            # Documentation
├── scripts/         # Build & dev scripts
├── tests/           # E2E tests
└── src-tauri/       # Tauri configuration
    ├── Cargo.toml
    └── src/main.rs
```

## Development Setup

### Prerequisites
- CachyOS (Arch-based)
- Rust toolchain
- Python 3.11+
- Node.js 20+
- ffmpeg
- yt-dlp

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run tauri:dev
```

### Build for Production

```bash
# Backend executable
pyinstaller backend/src/main.py

# Frontend app
cd frontend
npm run tauri:build
```

## Configuration

Create `config.json`:

```json
{
  "cache_dir": "~/.cache/youtube-music",
  "max_cache_size_gb": 5,
  "audio_quality": "192k",
  "auto_cleanup": true
}
```

## License

MIT License - Personal use only
