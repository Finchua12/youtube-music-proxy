# YouTube Music Project Completion Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete the YouTube Music desktop application with full backend-frontend integration

**Architecture:** Python FastAPI backend serving REST API, Vue/Tauri frontend consuming API, SQLite for storage, yt-dlp for YouTube integration

**Tech Stack:** Python 3.11+, FastAPI, Vue 3, TypeScript, Tauri, Rust, SQLite, yt-dlp, ffmpeg

---

## Current Status

The project has complete skeleton implementations for both backend and frontend with all core components in place. The next phase requires:
1. Setting up development environment
2. Connecting frontend to backend
3. Implementing real YouTube API integration
4. Adding actual audio playback functionality
5. Testing and building the application

## Prerequisites Setup

### Task 1: Install System Dependencies

**Step 1: Install Rust toolchain**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**Step 2: Install Node.js 20+**
```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

**Step 3: Install Python 3.11+ and ffmpeg**
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv ffmpeg

# On Arch/CachyOS
sudo pacman -Syu python python-venv ffmpeg
```

**Step 4: Install yt-dlp**
```bash
pip install yt-dlp
```

### Task 2: Set Up Backend Environment

**Files:**
- Create: `backend/venv/`
- Modify: `backend/requirements.txt`

**Step 1: Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

**Step 2: Install Python dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Test backend startup**
```bash
python src/main.py
```
Expected: Server starts on http://127.0.0.1:8000

**Step 4: Commit**
```bash
git add backend/requirements.txt
git commit -m "chore: set up backend development environment"
```

### Task 3: Set Up Frontend Environment

**Files:**
- Create: `frontend/node_modules/`
- Modify: `frontend/package.json`

**Step 1: Install frontend dependencies**
```bash
cd frontend
npm install
```

**Step 2: Test frontend dev server**
```bash
npm run dev
```
Expected: Vite dev server starts

**Step 3: Commit**
```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "chore: set up frontend development environment"
```

## Backend Implementation

### Task 4: Implement Real YouTube Authentication

**Files:**
- Modify: `backend/src/auth.py`
- Modify: `backend/src/youtube_api.py`

**Step 1: Update auth.py with real Google OAuth2 integration**
- Replace placeholder authentication with real Google OAuth2 flow
- Implement proper token exchange and refresh logic
- Add proper error handling for authentication failures

**Step 2: Implement youtube_api.py with real YouTube Data API**
- Integrate with YouTube Data API v3
- Implement search, playlist, and recommendation endpoints
- Add proper rate limiting and error handling

**Step 3: Test authentication flow**
```bash
# Start backend
cd backend
source venv/bin/activate
python src/main.py

# Test auth endpoint
curl http://127.0.0.1:8000/api/auth/url
```
Expected: Returns valid Google OAuth2 URL

**Step 4: Commit**
```bash
git add backend/src/auth.py backend/src/youtube_api.py
git commit -m "feat: implement real YouTube authentication and API integration"
```

## Frontend-Backend Integration

### Task 5: Connect Frontend to Backend API

**Files:**
- Create: `frontend/src/api/`
- Create: `frontend/src/api/client.ts`
- Modify: `frontend/src/pages/Home.vue`
- Modify: `frontend/src/pages/Search.vue`
- Modify: `frontend/src/pages/Library.vue`
- Modify: `frontend/src/pages/Playlist.vue`

**Step 1: Create API client**
```typescript
// frontend/src/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
});

export default apiClient;
```

**Step 2: Update Home.vue to fetch real data**
- Replace mock data with API calls to `/api/recommendations`
- Implement proper loading states and error handling
- Add real search functionality

**Step 3: Update Search.vue to use backend search**
- Connect search input to `/api/search` endpoint
- Implement real-time search with debouncing
- Display actual search results from YouTube

**Step 4: Update Library.vue to fetch user data**
- Connect to `/api/playlists` endpoint
- Implement playlist creation and management
- Add liked songs and downloaded tracks functionality

**Step 5: Update Playlist.vue to load real playlist data**
- Connect to `/api/playlists/{id}` endpoint
- Implement track addition/removal
- Add real playlist metadata

**Step 6: Test frontend-backend integration**
```bash
# Start backend
cd backend
source venv/bin/activate
python src/main.py

# Start frontend
cd frontend
npm run dev
```
Expected: Frontend loads real data from backend

**Step 7: Commit**
```bash
git add frontend/src/api/ frontend/src/pages/Home.vue frontend/src/pages/Search.vue frontend/src/pages/Library.vue frontend/src/pages/Playlist.vue
git commit -m "feat: connect frontend to backend API"
```

## Audio Playback Implementation

### Task 6: Implement Real Audio Playback

**Files:**
- Create: `frontend/src/audio/`
- Create: `frontend/src/audio/player.ts`
- Modify: `frontend/src/components/PlayerBar.vue`

**Step 1: Create audio player service**
```typescript
// frontend/src/audio/player.ts
import { Howl, Howler } from 'howler';

class AudioManager {
  private currentSound: Howl | null = null;

  play(url: string) {
    if (this.currentSound) {
      this.currentSound.stop();
    }

    this.currentSound = new Howl({
      src: [url],
      html5: true,
      onplay: () => console.log('Playback started'),
      onend: () => console.log('Playback finished'),
      onpause: () => console.log('Playback paused'),
      onstop: () => console.log('Playback stopped'),
    });

    this.currentSound.play();
  }

  pause() {
    if (this.currentSound) {
      this.currentSound.pause();
    }
  }

  stop() {
    if (this.currentSound) {
      this.currentSound.stop();
    }
  }
}

export default new AudioManager();
```

**Step 2: Update PlayerBar.vue to use real audio**
- Replace mock playback controls with real audio player
- Implement progress tracking and seeking
- Add volume control and mute functionality
- Handle audio events (play, pause, stop, end)

**Step 3: Connect audio player to backend streaming**
- Update backend to serve actual audio files
- Implement proper streaming with range requests
- Add audio caching and cleanup functionality

**Step 4: Test audio playback**
```bash
# Start backend
cd backend
source venv/bin/activate
python src/main.py

# Start frontend
cd frontend
npm run dev

# Navigate to app and play a track
```
Expected: Audio plays from YouTube source

**Step 5: Commit**
```bash
git add frontend/src/audio/ frontend/src/components/PlayerBar.vue
git commit -m "feat: implement real audio playback functionality"
```

## Testing and Quality Assurance

### Task 7: Add Comprehensive Testing

**Files:**
- Create: `backend/tests/`
- Create: `frontend/tests/`
- Create: `tests/e2e/`

**Step 1: Add backend unit tests**
- Test API endpoints with pytest
- Add database integration tests
- Test downloader and cache functionality

**Step 2: Add frontend unit tests**
- Test Vue components with Vitest
- Add API client tests
- Test audio player functionality

**Step 3: Add end-to-end tests**
- Test full user flows with Playwright
- Test search, playback, and library management
- Add cross-platform testing

**Step 4: Run test suite**
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/

# Frontend tests
cd frontend
npm run test

# E2E tests
npx playwright test
```
Expected: All tests pass

**Step 5: Commit**
```bash
git add backend/tests/ frontend/tests/ tests/
git commit -m "test: add comprehensive test suite"
```

## Build and Deployment

### Task 8: Create Production Build

**Files:**
- Modify: `src-tauri/tauri.conf.json`
- Create: `dist/`

**Step 1: Configure Tauri for production**
- Update tauri.conf.json with production settings
- Add proper icons and metadata
- Configure bundling for different platforms

**Step 2: Build backend executable**
```bash
cd backend
source venv/bin/activate
pip install pyinstaller
pyinstaller src/main.py
```

**Step 3: Build frontend application**
```bash
cd frontend
npm run build
```

**Step 4: Build Tauri application**
```bash
cd frontend
npm run tauri:build
```
Expected: Creates installable application bundles

**Step 5: Test production build**
- Install and run the built application
- Verify all functionality works
- Test on target platform (CachyOS)

**Step 6: Commit**
```bash
git add src-tauri/tauri.conf.json
git commit -m "build: create production build configuration"
```

## Documentation and Finalization

### Task 9: Complete Documentation

**Files:**
- Create: `docs/user-guide.md`
- Create: `docs/developer-guide.md`
- Modify: `README.md`

**Step 1: Write user guide**
- Installation instructions
- Getting started tutorial
- Feature documentation
- Troubleshooting guide

**Step 2: Write developer guide**
- Development setup
- Architecture overview
- API documentation
- Contributing guidelines

**Step 3: Update README.md**
- Add installation instructions
- Link to documentation
- Include screenshots
- Add license information

**Step 4: Commit**
```bash
git add docs/ README.md
git commit -m "docs: complete project documentation"
```

## Final Verification

### Task 10: Final Integration Testing

**Step 1: Run full integration test**
- Start backend server
- Launch frontend application
- Test all major features
- Verify error handling

**Step 2: Performance testing**
- Test application startup time
- Verify memory usage
- Check network performance

**Step 3: Security review**
- Verify proper authentication
- Check data handling
- Review permissions

**Step 4: Final commit**
```bash
git add .
git commit -m "feat: complete YouTube Music application implementation"
```

---

Plan complete and saved to `docs/plans/2024-02-12-youtube-music-completion-plan.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?