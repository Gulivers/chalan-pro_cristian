# 🔧 Solución: Frontend no accesible para Onboarding

## Problema

Al intentar acceder a `http://localhost:8000/onboarding`, se obtenía un error 404 porque:

1. El frontend Vue está en un servidor separado (puerto 3000)
2. El backend Django solo sirve las rutas API y admin (puerto 8000)
3. El servicio frontend no estaba corriendo en Docker

## Solución Implementada

### 1. Agregar Servicio Frontend a docker-compose.yml

Se agregó el servicio `frontend` al `docker-compose.yml`:

```yaml
frontend:
  image: node:18-alpine
  container_name: chalan-frontend
  working_dir: /app
  command: sh -c "npm ci && npm run serve -- --host 0.0.0.0 --port 3000"
  volumes:
    - ./vuefrontend:/app
    - chalan-frontend-node_modules:/app/node_modules
  ports:
    - "3000:3000"
  environment:
    - HOST=0.0.0.0
    - NODE_ENV=development
  depends_on:
    - backend
```

### 2. Corregir Proxy en vue.config.js

Se actualizó el proxy para que apunte al backend correcto:

```javascript
devServer: {
  host: '0.0.0.0',
  port: 3000,
  allowedHosts: ['all'],
  proxy: {
    '/api': {
      target: 'http://chalan-backend:8000',
      changeOrigin: true,
      secure: false,
      ws: true,
    },
  },
},
```

## Cómo Acceder

### Opción 1: Frontend en Puerto 3000 (Recomendado)

**URL**: `http://localhost:3000/onboarding`

El frontend Vue está corriendo en el puerto 3000 y hace proxy de las peticiones `/api` al backend en el puerto 8000.

### Opción 2: Iniciar Frontend Manualmente

Si prefieres iniciar el frontend manualmente fuera de Docker:

```bash
cd vuefrontend
npm install
npm run serve
```

Luego acceder a: `http://localhost:3000/onboarding`

## Verificación

### Verificar que el Frontend está Corriendo

```bash
docker ps | grep chalan-frontend
```

Debería mostrar:
```
chalan-frontend   Up   ...   0.0.0.0:3000->3000/tcp
```

### Ver Logs del Frontend

```bash
docker logs chalan-frontend --tail 50
```

Deberías ver algo como:
```
App running at:
- Local:   http://localhost:3000/
- Network: http://0.0.0.0:3000/
```

## Iniciar el Frontend

Si el frontend no está corriendo:

```bash
docker-compose up -d frontend
```

O para ver los logs en tiempo real:

```bash
docker-compose up frontend
```

## Notas Importantes

1. **Puerto 3000**: El frontend Vue corre en el puerto 3000, no en el 8000
2. **Proxy**: Las peticiones `/api/*` se redirigen automáticamente al backend
3. **Hot Reload**: El frontend tiene hot reload activado en desarrollo
4. **Dependencias**: La primera vez puede tardar varios minutos en instalar `node_modules`

## Troubleshooting

### Error: "Cannot connect to backend"

**Causa**: El proxy no puede alcanzar el backend.

**Solución**: Verificar que el backend esté corriendo:
```bash
docker ps | grep chalan-backend
```

### Error: "Port 3000 already in use"

**Causa**: Otro proceso está usando el puerto 3000.

**Solución**: 
1. Detener el proceso que usa el puerto 3000
2. O cambiar el puerto en `vue.config.js` y `docker-compose.yml`

### Frontend no inicia

**Causa**: Problemas con node_modules o dependencias.

**Solución**:
```bash
docker-compose down frontend
docker volume rm chalan_tenant_sch_chalan-frontend-node_modules
docker-compose up -d frontend
```

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

