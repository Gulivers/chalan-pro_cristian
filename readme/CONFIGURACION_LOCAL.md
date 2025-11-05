# Configuración Local para Desarrollo

## Archivo `.env.local` para Vue.js

Para desarrollo local, crea el archivo `vuefrontend/.env.local` con:

```bash
VUE_APP_API_BASE_URL=http://192.168.0.248:8000
```

O si prefieres usar localhost:

```bash
VUE_APP_API_BASE_URL=http://localhost:8000
```

Este archivo NO se sube a GitHub (está en `.gitignore`).

## Configuración en `main.js`

El archivo `vuefrontend/src/main.js` usa esta lógica:

```javascript
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'https://chalan-backend.onrender.com';
```

Esto significa:
- **Local:** Si existe `vuefrontend/.env.local`, usa esa URL
- **Producción:** Si no existe, usa `https://chalan-backend.onrender.com` (Render)

## Scripts Locales

Los siguientes scripts están en `.gitignore` y NO se suben a GitHub:
- `fix-postgres-password.ps1`
- `get-postgres-connection-info.ps1`
- `test-postgres-connection.ps1`
- `docker-postgres-setup.ps1`
- `docker-postgres-manage.ps1`

Estos son solo para desarrollo local.

