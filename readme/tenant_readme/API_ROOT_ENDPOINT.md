# 🔌 API Root Endpoint - Schema Public

## 📋 Resumen

Se ha agregado un endpoint raíz `/api/` para el schema `public` que muestra los endpoints disponibles y documentación básica.

## 🌐 Endpoint

**URL**: `http://192.168.0.248:8000/api/`  
**Método**: `GET`  
**Autenticación**: No requerida (público)

## 📤 Respuesta

```json
{
  "message": "Chalan-Pro API - Public Schema",
  "version": "1.0.0",
  "endpoints": {
    "onboarding": {
      "create_tenant": {
        "url": "/api/onboarding/create-tenant/",
        "method": "POST",
        "description": "Crear un nuevo tenant y ambiente de trabajo",
        "required_fields": ["company_name", "email", "client_type"],
        "optional_fields": ["logo"],
        "example": {
          "company_name": "Phoenix Electric",
          "email": "admin@phoenix.com",
          "client_type": "electric",
          "logo": "(archivo de imagen opcional)"
        }
      }
    },
    "admin": {
      "url": "/admin/",
      "description": "Panel de administración global para gestionar tenants"
    }
  },
  "documentation": {
    "onboarding": "Accede a /onboarding en el frontend para crear tu cuenta",
    "api_docs": "Los endpoints de tenant están disponibles después de crear tu cuenta"
  }
}
```

## 🎯 Uso

### Ver Endpoints Disponibles

```bash
curl http://192.168.0.248:8000/api/
```

O simplemente abre en el navegador:
```
http://192.168.0.248:8000/api/
```

### Crear un Tenant

```bash
curl -X POST http://192.168.0.248:8000/api/onboarding/create-tenant/ \
  -F "company_name=Phoenix Electric" \
  -F "email=admin@phoenix.com" \
  -F "client_type=electric" \
  -F "logo=@/path/to/logo.png"
```

## 📝 Notas

- Este endpoint está disponible solo en el schema `public`
- Los endpoints de tenant (inventory, transactions, etc.) están disponibles después de crear un tenant y acceder a su subdominio
- El endpoint raíz proporciona información sobre cómo usar la API de onboarding

## 🔗 Endpoints Relacionados

- `/api/onboarding/create-tenant/` - Crear nuevo tenant
- `/admin/` - Panel de administración global

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

