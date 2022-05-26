import { createApp } from 'vue'
import App from './App.vue'
import io from 'socket.io-client';

const app = createApp(App)
app.config.globalProperties.$socketio = io('http://localhost:8100');
app.mount('#app')
