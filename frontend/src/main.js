import './assets/main.css'
import { createApp } from 'vue'
import VueSmoothScroll from 'vue3-smooth-scroll'
import App from './App.vue'
import router from './router'
import store from './store'
import TransitionWrapper from './components/TransitionWrapper.vue'
//in your `main.js` file
import '../node_modules/flowbite-vue/dist/index.css'
import removeConsole from './plugins/removeConsole'

const app = createApp(App)

app.component('TransitionWrapper', TransitionWrapper)
app.use(router)
app.use(store)
app.use(VueSmoothScroll)
app.use(removeConsole)

app.mount('#app')
