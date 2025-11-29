# 🐛 Depuración del Onboarding - Guardar Tenant sin Schema

## Problema Identificado

El error 500 al crear un tenant puede estar relacionado con la creación automática del schema por parte de `django-tenants`. 

## Solución Implementada

Se modificó el flujo para:

1. **Generar schema_name y tenant_id primero** (sin guardar)
2. **Guardar el tenant en la base de datos** con `auto_create_schema=False`
3. **Crear el schema manualmente** después de guardar el tenant
4. **Agregar logging detallado** para depurar problemas

## Cambios en `tenants/views.py`

### Antes:
```python
tenant = Tenant(...)
tenant.save()  # Esto intentaba crear el schema automáticamente
```

### Ahora:
```python
# 1. Generar schema_name y tenant_id
schema_name = temp_tenant._generate_schema_name()
tenant_id = temp_tenant._generate_tenant_id()

# 2. Crear tenant con auto_create_schema=False
tenant = Tenant(..., auto_create_schema=False)

# 3. Guardar en DB primero
tenant.save()

# 4. Crear schema manualmente
with connection.cursor() as cursor:
    cursor.execute(f'CREATE SCHEMA "{tenant.schema_name}"')
```

## Logging Agregado

El sistema ahora registra:
- ✅ Inicio de creación de tenant
- ✅ Schema name generado
- ✅ Tenant ID generado
- ✅ Validación del tenant
- ✅ Guardado en base de datos
- ✅ Creación del schema en PostgreSQL
- ✗ Errores detallados con traceback completo

## Verificar Logs

Para ver los logs en tiempo real:

```bash
docker logs -f chalan-backend | grep -i "tenant\|schema\|error"
```

O ver los últimos logs:

```bash
docker logs chalan-backend --tail 50
```

## Próximos Pasos de Depuración

1. **Probar crear un tenant** desde el frontend
2. **Revisar los logs** para ver exactamente dónde falla
3. **Verificar en la base de datos** si el tenant se guardó:
   ```sql
   SELECT * FROM tenants_tenant ORDER BY created_on DESC LIMIT 5;
   ```
4. **Verificar si el schema se creó**:
   ```sql
   SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%';
   ```

## Comandos Útiles

### Ver tenants en la base de datos:
```bash
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_per_tenant -c "SELECT id, name, schema_name, email, is_active FROM tenants_tenant ORDER BY created_on DESC LIMIT 5;"
```

### Ver schemas creados:
```bash
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_per_tenant -c "\dn"
```

### Ver logs del backend en tiempo real:
```bash
docker logs -f chalan-backend
```

---

**Fecha**: 2025-11-24  
**Versión**: 1.0.0

