<template>
  <aside class="sidebar">
    <div class="logo-container">
      <div class="logo">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20.5 15.5L14.5 12V20L20.5 16.5V24C20.5 24.5523 20.0523 25 19.5 25H5.5C4.94772 25 4.5 24.5523 4.5 24V8C4.5 7.44772 4.94772 7 5.5 7H19.5C20.0523 7 20.5 7.44772 20.5 8V15.5Z" fill="#FF0000"/>
          <path d="M23.5 11C24.8807 11 26 9.88071 26 8.5C26 7.11929 24.8807 6 23.5 6C22.1193 6 21 7.11929 21 8.5C21 9.88071 22.1193 11 23.5 11Z" fill="#FF0000"/>
          <path d="M23.5 26C24.8807 26 26 24.8807 26 23.5C26 22.1193 24.8807 21 23.5 21C22.1193 21 21 22.1193 21 23.5C21 24.8807 22.1193 26 23.5 26Z" fill="#FF0000"/>
        </svg>
        <span class="logo-text">MusicProxy</span>
      </div>
    </div>

    <nav class="nav-menu">
      <router-link to="/" class="nav-item" active-class="active">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Головна</span>
      </router-link>

      <router-link to="/search" class="nav-item" active-class="active">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Пошук</span>
      </router-link>

      <router-link to="/library" class="nav-item" active-class="active">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 12V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H6C5.46957 22 4.96086 21.7893 4.58579 21.4142C4.21071 21.0391 4 20.5304 4 20V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M4 12H2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M22 12H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 4V2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 22V20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Бібліотека</span>
      </router-link>

      <div class="divider"></div>

      <div class="playlists-section">
        <div class="section-header">
          <span>Плейлисти</span>
          <button class="add-playlist-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <router-link to="/playlist/favorites" class="playlist-item">
          <div class="playlist-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z" fill="#FF0000"/>
            </svg>
          </div>
          <span>Улюблені треки</span>
        </router-link>

        <router-link to="/playlist/recent" class="playlist-item">
          <div class="playlist-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <span>Нещодавно</span>
        </router-link>

        <router-link to="/playlist/downloads" class="playlist-item">
          <div class="playlist-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 3V16M12 16L16 12M12 16L8 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20 21H4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <span>Завантажені</span>
        </router-link>
      </div>
    </nav>

    <div class="user-profile">
      <div class="profile-info">
        <div class="avatar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/>
            <path d="M5 20C5 16.134 8.13401 13 12 13C15.866 13 19 16.134 19 20" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <div class="user-details">
          <div class="username">Користувач</div>
          <div class="status">Особистий акаунт</div>
        </div>
      </div>
      <button class="settings-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
          <path d="M12 1V3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M12 21V23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M4.22 4.22L5.64 5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M18.36 18.36L19.78 19.78" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M1 12H3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M21 12H23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M4.22 19.78L5.64 18.36" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M18.36 5.64L19.78 4.22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
// This component doesn't require any logic for now
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: var(--bg-secondary);
  height: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
  padding: 16px 0;
  transition: width 0.3s ease;
}

.logo-container {
  padding: 0 16px 16px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo svg {
  color: #FF0000;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.nav-menu {
  flex: 1;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent);
  color: white;
}

.nav-item svg {
  flex-shrink: 0;
}

.divider {
  height: 1px;
  background: var(--border-color);
  margin: 16px 0;
}

.playlists-section {
  margin-top: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  margin-bottom: 8px;
}

.section-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.add-playlist-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.add-playlist-btn:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.playlist-item:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.playlist-icon {
  flex-shrink: 0;
}

.user-profile {
  padding: 16px;
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.status {
  font-size: 12px;
  color: var(--text-tertiary);
}

.settings-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.settings-btn:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}
</style>