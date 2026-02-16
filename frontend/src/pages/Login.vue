<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo">
        <svg viewBox="0 0 24 24" width="64" height="64" fill="currentColor">
          <path d="M12 0C5.376 0 0 5.376 0 12s5.376 12 12 12 12-5.376 12-12S18.624 0 12 0zm0 19.104c-3.924 0-7.104-3.18-7.104-7.104S8.076 4.896 12 4.896s7.104 3.18 7.104 7.104-3.18 7.104-7.104 7.104zm0-13.332c-3.432 0-6.228 2.796-6.228 6.228S8.568 18.228 12 18.228s6.228-2.796 6.228-6.228S15.432 5.772 12 5.772zM9.684 15.54V8.46L15.816 12l-6.132 3.54z"/>
        </svg>
        <h1>YouTube Music Proxy</h1>
      </div>
      
      <p class="subtitle">Увійдіть через Google для доступу до ваших плейлистів</p>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Завантаження...</p>
      </div>
      
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="retry" class="btn-secondary">Спробувати знову</button>
      </div>
      
      <div v-else class="login-options">
        <button @click="loginWithGoogle" class="btn-google">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Увійти через Google
        </button>
        
        <div class="divider">
          <span>або</span>
        </div>
        
        <button @click="continueWithoutLogin" class="btn-secondary">
          Продовжити без авторизації
        </button>
      </div>
      
      <div class="features">
        <h3>Що ви отримаєте після авторизації:</h3>
        <ul>
          <li>✅ Доступ до ваших YouTube плейлистів</li>
          <li>✅ Синхронізація вподобаних треків</li>
          <li>✅ Персоналізовані рекомендації</li>
          <li>✅ Історія прослуховувань</li>
        </ul>
      </div>
      
      <p class="privacy-note">
        🔒 Ваші дані в безпеці. Ми не зберігаємо ваш пароль.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlayerStore } from '@/stores/player'
import { authApi } from '@/services/api'

const router = useRouter()
const playerStore = usePlayerStore()

const loading = ref(false)
const error = ref('')

onMounted(async () => {
  // Перевіряємо чи користувач вже авторизований
  const token = localStorage.getItem('access_token')
  if (token) {
    router.push('/')
  }
})

const loginWithGoogle = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await authApi.getAuthUrl() as { auth_url: string }
    if (response.auth_url) {
      // Перенаправляємо на Google OAuth
      window.location.href = response.auth_url
    } else {
      error.value = 'Не вдалося отримати посилання для авторизації'
    }
  } catch (err) {
    error.value = 'Помилка підключення до сервера'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}

const continueWithoutLogin = () => {
  // Позначаємо що користувач увійшов як гість
  localStorage.setItem('auth_mode', 'guest')
  router.push('/')
}

const retry = () => {
  error.value = ''
  loading.value = false
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
}

.login-container {
  background: var(--bg-primary, #0f0f0f);
  border-radius: 16px;
  padding: 48px;
  max-width: 420px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.logo {
  margin-bottom: 24px;
}

.logo svg {
  color: #ff0000;
  margin-bottom: 16px;
}

.logo h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary, #fff);
  margin: 0;
}

.subtitle {
  color: var(--text-secondary, #aaa);
  margin-bottom: 32px;
  font-size: 14px;
}

.loading {
  padding: 32px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #ff0000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.error p {
  color: #ff4444;
  margin-bottom: 12px;
}

.btn-google {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 14px 24px;
  background: #fff;
  color: #333;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-google:hover {
  background: #f5f5f5;
  transform: translateY(-1px);
}

.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: var(--text-secondary, #666);
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color, #333);
}

.divider span {
  padding: 0 16px;
  font-size: 14px;
}

.btn-secondary {
  width: 100%;
  padding: 14px 24px;
  background: transparent;
  color: var(--text-primary, #fff);
  border: 1px solid var(--border-color, #333);
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.features {
  text-align: left;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid var(--border-color, #333);
}

.features h3 {
  font-size: 14px;
  color: var(--text-secondary, #aaa);
  margin-bottom: 16px;
}

.features ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.features li {
  color: var(--text-primary, #fff);
  font-size: 14px;
  margin-bottom: 8px;
  padding-left: 8px;
}

.privacy-note {
  margin-top: 24px;
  font-size: 12px;
  color: var(--text-secondary, #666);
}
</style>
