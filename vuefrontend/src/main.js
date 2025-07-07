import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // OAHP
import {Modal} from 'bootstrap';
import 'vue-select/dist/vue-select.css';
import {setupAxiosInterceptors} from './utils/axiosConfig';
import axios from 'axios';
import authService from './auth/authService';
import {appMixin} from '@mixins/appMixin';
import 'leaflet/dist/leaflet.css';
import '@/assets/scss/custom-bootstrap.scss'; // custom scss npm install sass sass-loader --save-dev

// Permite que las cookies se envíen con cada solicitud
axios.defaults.withCredentials = true;

setupAxiosInterceptors();

// La URL base de la API
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/';

// Crea la aplicación de Vue
const app = createApp(App);

// Usa el mixin globalmente en toda la app
app.mixin(appMixin);

// Monta la aplicación con router y store
app.use(store).use(router).mount('#app');
