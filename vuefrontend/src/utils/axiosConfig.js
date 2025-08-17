// Interceptor de solicitudes de Axios para manejar la autenticación
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import router from '../router';

export function setupAxiosInterceptors() {
  // Interceptor de solicitud
  axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('authToken');

      if (token) {
        config.headers['Authorization'] = `Token ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  const api_endpoints = [
    { 'route': '/api/contract/', 'method': 'PUT' },
    { 'route': '/api/contract/', 'method': 'POST' },
    { 'route': '/api/contract/', 'method': 'DELETE' },
    // { 'route': '/api/contract/', 'method': 'GET' },
    { 'route': '/api/contractdetails/', 'method': 'PUT' },
    { 'route': '/api/workprice/', 'method': 'PUT' },
    { 'route': '/api/workprice/', 'method': 'POST' },
    { 'route': '/api/workprice/', 'method': 'DELETE' },
    // { 'route': '/api/workprice/', 'method': 'GET' }
  ];

  // Función para verificar si la ruta y el método están en la lista
  function shouldLogAction(url, method) {
    return api_endpoints.some(endpoint => url.includes(endpoint.route) && method.toUpperCase() === endpoint.method);
  }

  // Interceptor de respuesta
  axios.interceptors.response.use(
    response => {

      const config = response.config;
      // console.log("config->", config);
      // Verificamos si la URL y el método están en la lista api_endpoints
      if (shouldLogAction(config.url, config.method)) {
        logUserAction(config, response.data);
      }

      return response;
    },
    async error => {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        // Se eliminó la lógica de refresco de token
        localStorage.removeItem('authToken');
        localStorage.removeItem('userPermissions');
        router.push('/login');
        return Promise.reject(error);
      }
      return Promise.reject(error);
    }
  );
}

// Función para registrar la acción del usuario
function logUserAction(config, data) {
  const token = localStorage.getItem('authToken');
  if (token) {
    axios.post('/api/log-action/', {
      action: config.method.toUpperCase(),
      model_name: extractModelName(config.url), // Extraemos el nombre del modelo
      object_id: data.id || null, // ID del objeto, si está disponible
      details: `Action logged at ${config.url} with method ${config.method.toUpperCase()}`
    }, {
      headers: {
        Authorization: `Token ${token}`,
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        console.log("Action logged:", response.data);
      })
      .catch(error => {
        console.error("Error logging the action:", error);
      });
  } else {
    console.error("Token not found. The user is not authenticated.");
  }
}

// Función para extraer el nombre del modelo de la URL
function extractModelName(url) {
  if (url.includes('/api/contract/')) return 'Contract';
  if (url.includes('/api/contractdetails/')) return 'ContractDetails';
  if (url.includes('/api/workprice/')) return 'WorkPrice';
  if (url.includes('/api/events/')) return 'Event';
  return 'UnknownModel'; // Modelo desconocido si no se encuentra
}