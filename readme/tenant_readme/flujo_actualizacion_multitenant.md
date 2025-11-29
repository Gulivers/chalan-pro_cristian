# 🔄 Flujo de Actualización Multi-Tenant en Chalan-Pro

Este esquema describe cómo se lleva a cabo el flujo de actualización general (backend y frontend) para múltiples clientes (tenants) en el sistema Chalan-Pro, cuando cada cliente corre en contenedores separados.

---

## 🧱 Infraestructura Base

- **Un contenedor por cliente para:**
  - Django Backend → `web-<cliente>`
  - Nginx Frontend → `nginx-<cliente>`
- **Contenedores compartidos:**
  - `nginx-proxy` → maneja tráfico HTTP/HTTPS
  - `letsencrypt-nginx-proxy-companion` → gestiona certificados SSL
  - `postgresql` → contiene todos los schemas (uno por cliente)
  - `redis` → sesiones y caché por tenant
  - `pgadmin` → gestión base de datos

---

## 📦 Diagrama Contenedores (ASCII)

```plaintext
                  ┌────────────────────────────┐
                  │         Usuario            │
                  │ client2.example.com        │
                  └────────────┬───────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ nginx-proxy  │◄────── Certs (Let's Encrypt)
                        └─────┬────────┘
         ┌────────────────────┴─────────────────────┐
         │                                          │
 ┌──────────────┐                          ┌──────────────┐
 │ nginx-client2│                          │ nginx-phoenix│
 └─────┬────────┘                          └─────┬────────┘
       │ Vue static                            │ Vue static
       ▼                                       ▼
 ┌──────────────┐                       ┌──────────────┐
 │ web-client2  │◄──── API ────────►    │ web-phoenix  │
 └─────┬────────┘                       └─────┬────────┘
       │ Django schema                        │ Django schema
       ▼                                      ▼
 ┌──────────────────┐                ┌────────────────────┐
 │ tenant_client2   │                │ tenant_phoenix     │
 │ (PostgreSQL)     │                │ (PostgreSQL)       │
 └──────────────────┘                └────────────────────┘
```

---

## 🛠️ Flujo de Actualización General

```plaintext
[DevOps] 
    │
    ├──> Actualiza código fuente backend y frontend
    │
    ├──> Compila backend:
    │     docker build -t chalanpro:2.1.0 .
    │
    ├──> Compila frontend Vue:
    │     npm run build
    │
    └──> Ejecuta:
           docker-compose up -d --force-recreate \
             web-phoenix web-client2 web-client3 \
             nginx-phoenix nginx-client2 nginx-client3
```

---

## ⚙️ Despliegue por Cliente

```plaintext
[Cliente: phoenixelectricandair.net]
    │
    ├──> nginx-proxy enruta a nginx-phoenix
    │
    ├──> nginx-phoenix sirve dist Vue actualizado
    │
    ├──> Vue llama API → nginx-proxy → web-phoenix
    │
    └──> Django backend (v2.1.0) usa schema tenant_phoenix

[Cliente: client2.example.com]
    │
    ├──> nginx-proxy enruta a nginx-client2
    │
    ├──> nginx-client2 sirve dist Vue actualizado
    │
    ├──> Vue llama API → nginx-proxy → web-client2
    │
    └──> Django backend (v2.1.0) usa schema tenant_client2
```

---

## 📋 Checklist Automatizable de Actualización

- [ ] Commit del código actualizado (`git commit -m 'Update v2.1.0'`)
- [ ] `docker build -t chalanpro:2.1.0 .`
- [ ] `npm run build` para frontend
- [ ] `docker-compose up -d --force-recreate` de todos los contenedores
- [ ] Validar `/api/` y vistas frontend en cada tenant
- [ ] Correr migraciones por schema si aplica
  ```bash
  docker exec web-client2 python manage.py migrate --schema=tenant_client2
  ```
- [ ] Verificar logs y healthcheck

---

## 🧪 Flujo Progresivo (opcional)

1. Se actualiza solo un tenant (ej: `web-phoenix`, `nginx-phoenix`)
2. Se verifica comportamiento con producción real
3. Si todo está ok, se actualiza el resto

---

## ✅ Resultado Final

- Todos los clientes reciben mejoras y correcciones
- No hay downtime si se usa `--force-recreate`
- Se mantiene la personalización por dominio y schema
- Se optimiza el proceso de mantenimiento con scripts automatizados

