import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import Home from './pages/Home.vue'
import Search from './pages/Search.vue'
import Library from './pages/Library.vue'
import Playlist from './pages/Playlist.vue'

// Import styles
import './styles/main.css'

// Create router
const routes = [
  { path: '/', component: Home },
  { path: '/search', component: Search },
  { path: '/library', component: Library },
  { path: '/playlist/:id', component: Playlist, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create app
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Initialize audio player
const playerStore = pinia.state.value.playerStore
if (playerStore) {
  playerStore.initialize()
}

app.mount('#app')