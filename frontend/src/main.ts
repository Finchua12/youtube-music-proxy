import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import Home from './pages/Home.vue'
import Search from './pages/Search.vue'
import Library from './pages/Library.vue'
import Playlist from './pages/Playlist.vue'
import Login from './pages/Login.vue'
import Callback from './pages/Callback.vue'

// Import styles
import './styles/main.css'

// Create router with hash history for better SPA compatibility
const routes = [
  { path: '/', component: Home },
  { path: '/search', component: Search },
  { path: '/library', component: Library },
  { path: '/playlist/:id', component: Playlist, props: true },
  { path: '/login', component: Login },
  { path: '/callback', component: Callback }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Create app
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Mount app
app.mount('#app')