# Встановлення YouTube Music Proxy

## Системні вимоги

### Операційна система
- **CachyOS** (рекомендовано)
- Arch Linux, Manjaro або інші Arch-based дистрибутиви
- Ubuntu 20.04+, Fedora 32+, або інші сучасні Linux дистрибутиви

### Залежності
- **Python** 3.11 або новіша
- **Node.js** 18 або новіша
- **Rust** (через rustup)
- **ffmpeg** та **ffprobe**
- **yt-dlp**
- **SQLite** 3.35 або новіша

## Встановлення залежностей

### Arch-based системи (CachyOS, Arch Linux, Manjaro)

```bash
# Оновити систему
sudo pacman -Syu

# Встановити основні залежності
sudo pacman -S python python-pip nodejs npm rust ffmpeg yt-dlp

# Встановити додаткові інструменти (за бажанням)
sudo pacman -S git sqlite3
```

### Ubuntu/Debian

```bash
# Оновити систему
sudo apt update && sudo apt upgrade

# Встановити основні залежності
sudo apt install python3 python3-pip nodejs npm ffmpeg

# Встановити Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Встановити yt-dlp
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Встановити додаткові інструменти (за бажанням)
sudo apt install git sqlite3
```

### Fedora

```bash
# Оновити систему
sudo dnf update

# Встановити основні залежності
sudo dnf install python3 python3-pip nodejs npm rust ffmpeg

# Встановити yt-dlp
sudo dnf install yt-dlp

# Встановити додаткові інструменти (за бажанням)
sudo dnf install git sqlite
```

## Клонування репозиторію

```bash
# Клонувати проект
git clone https://github.com/your-username/youtube-music-proxy.git
cd youtube-music-proxy
```

## Налаштування Backend

### Створення віртуального середовища

```bash
# Перейти до директорії backend
cd backend

# Створити віртуальне середовище
python -m venv venv

# Активувати віртуальне середовище
source venv/bin/activate  # Linux/macOS
# або
venv\Scripts\activate     # Windows
```

### Встановлення Python залежностей

```bash
# Встановити залежності
pip install -r requirements.txt

# Або встановити окремо (якщо requirements.txt відсутній)
pip install fastapi uvicorn yt-dlp sqlalchemy alembic pydantic pydantic-settings python-multipart requests aiofiles asyncio-mqtt mutagen pillow google-api-python-client
```

### Налаштування конфігурації

Створіть файл `config.json` в директорії `backend`:

```json
{
  "cache_dir": "~/.cache/youtube-music",
  "max_cache_size_gb": 5,
  "audio_quality": "192k",
  "auto_cleanup": true,
  "download_format": "mp3",
  "max_download_threads": 3,
  "proxy_enabled": false,
  "proxy_url": "",
  "theme": "dark",
  "language": "uk"
}
```

### Запуск Backend

```bash
# Запустити сервер розробки
python src/main.py

# Або використовуючи uvicorn напряму
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

Сервер буде доступний за адресою: `http://127.0.0.1:8000`

## Налаштування Frontend

### Встановлення Node.js залежностей

```bash
# Перейти до директорії frontend
cd ../frontend

# Встановити залежності
npm install
```

### Налаштування Tauri

Tauri вже включений в `package.json`, але вам потрібно встановити системні залежності:

#### Arch-based системи

```bash
sudo pacman -S webkit2gtk openssl-apple-framework-sys
```

#### Ubuntu/Debian

```bash
sudo apt install libwebkit2gtk-4.0-dev build-essential curl wget libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev
```

#### Fedora

```bash
sudo dnf install webkit2gtk4.0-devel openssl-devel clang libappindicator-gtk3-devel
```

## Розробка

### Запуск Frontend в режимі розробки

```bash
# Запустити Tauri в режимі розробки
npm run tauri:dev
```

### Збірка проекту

```bash
# Збірка для виробництва
npm run tauri:build
```

Виконуваний файл буде створений в директорії `src-tauri/target/release/`.

## Налаштування середовища

### Змінні середовища

Створіть файл `.env` в директорії `backend`:

```env
# Налаштування сервера
HOST=127.0.0.1
PORT=8000

# Налаштування бази даних
DATABASE_URL=sqlite:///home/user/.local/share/youtube-music/database.db

# Налаштування кешу
CACHE_DIR=~/.cache/youtube-music
MAX_CACHE_SIZE_GB=5

# API ключі (за бажанням)
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## Усунення несправностей

### Поширені проблеми

#### 1. Помилка "ModuleNotFoundError: No module named 'yt_dlp'"

```bash
# Встановіть yt-dlp
pip install yt-dlp
```

#### 2. Помилка "Command 'ffmpeg' not found"

```bash
# Встановіть ffmpeg (Arch-based)
sudo pacman -S ffmpeg

# Встановіть ffmpeg (Ubuntu/Debian)
sudo apt install ffmpeg

# Встановіть ffmpeg (Fedora)
sudo dnf install ffmpeg
```

#### 3. Помилка "error: linker 'cc' not found"

```bash
# Встановіть інструменти збірки (Arch-based)
sudo pacman -S base-devel

# Встановіть інструменти збірки (Ubuntu/Debian)
sudo apt install build-essential

# Встановіть інструменти збірки (Fedora)
sudo dnf install gcc
```

#### 4. Помилка "error while loading shared libraries: libwebkit2gtk-4.0.so.37"

```bash
# Встановіть webkit2gtk (Arch-based)
sudo pacman -S webkit2gtk

# Встановіть webkit2gtk (Ubuntu/Debian)
sudo apt install libwebkit2gtk-4.0-dev

# Встановіть webkit2gtk (Fedora)
sudo dnf install webkit2gtk4.0-devel
```

### Перевірка встановлення

```bash
# Перевірити версії інструментів
python --version
node --version
npm --version
rustc --version
ffmpeg -version
yt-dlp --version
```

## Оновлення проекту

```bash
# Оновити репозиторій
git pull

# Оновити Python залежності
pip install -r backend/requirements.txt --upgrade

# Оновити Node.js залежності
cd frontend && npm update
```

## Наступні кроки

Після успішного встановлення:

1. Запустіть backend сервер: `cd backend && python src/main.py`
2. Запустіть frontend додаток: `cd frontend && npm run tauri:dev`
3. Відкрийте додаток і насолоджуйтесь музикою без реклами!