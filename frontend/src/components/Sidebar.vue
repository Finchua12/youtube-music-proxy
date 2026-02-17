<template>
  <aside class="sidebar">
    <div class="logo">
      <span class="logo-text">MusicProxy</span>
    </div>

    <nav class="nav-menu">
      <router-link to="/" class="nav-item" active-class="active">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0393 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Головна</span>
      </router-link>

      <router-link to="/search" class="nav-item" active-class="active">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>Пошук</span>
      </router-link>

      <router-link to="/library" class="nav-item" active-class="active">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M20 12V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H6C5.46957 22 4.96086 21.7893 4.58579 21.4142C4.21071 21.0391 4 20.5304 4 20V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Бібліотека</span>
      </router-link>

      <div class="divider"></div>

      <div class="playlists-section">
        <div class="section-header">
          <span>Плейлисти</span>
        </div>

        <router-link to="/playlist/favorites" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="#ef4444">
            <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35Z"/>
          </svg>
          <span>Улюблені</span>
        </router-link>

        <router-link to="/playlist/recent" class="nav-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6V12L16 14"/>
          </svg>
          <span>Нещодавно</span>
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg) 0;
  border-right: 1px solid var(--border-color);
}

.logo {
  padding: 0 var(--spacing-lg) var(--spacing-lg);
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  flex: 1;
  padding: 0 var(--spacing-sm);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  border-radius: var(--radius-md);
  margin-bottom: 2px;
}

.nav-item:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--hover-bg);
  color: var(--text-primary);
}

.nav-item svg {
  flex-shrink: 0;
}

.divider {
  height: 1px;
  background: var(--border-color);
  margin: var(--spacing-md) 0;
}

.section-header {
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-xs);
}

.section-header span {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>