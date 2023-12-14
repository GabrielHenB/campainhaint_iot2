import './bootstrap'; //Ja carrega o Axios
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

// Import our custom CSS
import '../css/app.scss';

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap';


import App from './Pages/App.vue';
import HomeView from './Pages/HomeView.vue';

// =================== FIM IMPORTS ==========================

// Cria APP Vue
const app = createApp(App);

// Caminho base do projeto. Isso nao eh a melhor forma.
const base_path = "/campainhaint/public/";

// Roteamento SPA por vue-router instanciado aqui. 
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: base_path,
      name: 'index',
      component: HomeView
    },
    {
      path: base_path + 'camera',
      name: 'camera',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('./Pages/CameraView.vue')
    },
    {
        path: base_path + 'historico',
        name:'historico',
        component: () => import('./Pages/HistoricoView.vue')
    },
    {
      path: base_path + 'eventos',
      name:'eventos',
      component: () => import('./Pages/HistoricoView.vue')
    },
    {
      path: base_path + "configuracoes",
      name: 'configuracoes',
      component: () => import('./Pages/ConfigView.vue')
    },
    {
      path: base_path + "about",
      name: 'about',
      component: () => import('./Pages/AboutView.vue')
    },
]
});

// USAR O ROUTER
app.use(router);

// INICIALIZA O VUE OFICIALMENTE
app.mount('#app');