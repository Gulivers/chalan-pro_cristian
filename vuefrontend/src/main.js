import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { createPinia } from 'pinia';  // OAHP
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // OAHP

import BootstrapVueNext from 'bootstrap-vue-next';
import { BTable, BPagination } from 'bootstrap-vue-next'
import {Modal} from 'bootstrap';
import 'vue-select/dist/vue-select.css';
import {setupAxiosInterceptors} from './utils/axiosConfig';
import axios from 'axios';
import authService from './auth/authService';
import {appMixin} from '@mixins/appMixin';
import {dataTableMixin} from '@mixins/dataTableMixin';
import 'leaflet/dist/leaflet.css';
import '@/assets/scss/custom-bootstrap.scss'; // custom scss npm install sass sass-loader --save-dev

// Permite que las cookies se envíen con cada solicitud
axios.defaults.withCredentials = true;

setupAxiosInterceptors();

// La URL base de la API
// axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/';
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://192.168.0.248:8000';

// Crea la aplicación de Vue
const app = createApp(App);

app.use(router);
app.use(BootstrapVueNext);
app.component('BTable', BTable)
app.component('BPagination', BPagination)

// Inicializa Pinia
const pinia = createPinia();
app.use(pinia); 

// Usa los mixins globalmente en toda la app
app.mixin(appMixin);
app.mixin(dataTableMixin);



// Monta la aplicación con router y store
app.use(store).use(router).mount('#app');
