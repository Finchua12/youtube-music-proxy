<template>
  <div class="callback-page">
    <div class="callback-container">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <h2>Авторизація...</h2>
        <p>Зачекайте, ми обробляєємо ваш вхід</p>
      </div>
      
      <div v-else-if="error" class="error">
        <svg viewBox="0 0 24 24" width="64" height="64" fill="#ff4444">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
        <h2>Помилка авторизації</h2>
        <p>{{ error }}</p>
        <button @click="goToLogin" class="btn-primary">
          Повернутися до входу
        </button>
      </div>
      
      <div v-else class="success">
        <svg viewBox="0 0 24 24" width="64" height="64" fill="#4CAF50">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <h2>Успішно!</h2>
        <p>Ви авторизовані. Перенаправляємо...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '@/services/api'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  // Отримуємо параметри з URL
  const code = route.query.code as string
  const state = route.query.state as string
  const errorParam = route.query.error as string
  
  if (errorParam) {
    error.value = 'Авторизація відхилена'
    loading.value = false
    return
  }
  
  if (!code || !state) {
    error.value = 'Відсутні необхідні параметри авторизації'
    loading.value = false
    return
  }
  
  try {
    // Відправляємо code на бекенд для обміну на токени
    const response = await authApi.handleCallback(code, state) as { 
      access_token: string 
      refresh_token?: string
      expires_at?: number
    }
    
    if (response.access_token) {
      // Зберігаємо токени
      localStorage.setItem('access_token', response.access_token)
      if (response.refresh_token) {
        localStorage.setItem('refresh_token', response.refresh_token)
      }
      if (response.expires_at) {
        localStorage.setItem('expires_at', response.expires_at.toString())
      }
      localStorage.setItem('auth_mode', 'google')
      
      // Перенаправляємо на головну
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      error.value = 'Не вдалося отримати токен доступу'
    }
  } catch (err: any) {
    error.value = err.message || 'Помилка під час авторизації'
  } finally {
    loading.value = false
  }
})

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.callback-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
}

.callback-container {
  background: var(--bg-primary, #0f0f0f);
  border-radius: 16px;
  padding: 48px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.loading, .error, .success {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 64px;
  height: 64px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: #ff0000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

h2 {
  color: var(--text-primary, #fff);
  margin-bottom: 12px;
  font-size: 24px;
}

p {
  color: var(--text-secondary, #aaa);
  margin-bottom: 24px;
}

.error svg {
  margin-bottom: 16px;
}

.success svg {
  margin-bottom: 16px;
}

.btn-primary {
  padding: 12px 32px;
  background: #ff0000;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #cc0000;
}
</style>
