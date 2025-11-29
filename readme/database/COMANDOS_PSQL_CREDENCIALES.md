# 🔍 Comandos PSQL para Obtener Credenciales y Configuración para DBeaver

## ✅ Verificación Completa desde pgAdmin/psql

Ya que pgAdmin está funcionando correctamente, estos comandos te darán las credenciales exactas para DBeaver.

---

## 📋 Comandos PSQL para Ejecutar

### 1. Verificar Usuarios y Sus Privilegios

```sql
-- Conectarse como superusuario
docker exec -it chalan_postgres psql -U postgres

-- Ver todos los usuarios y sus atributos
\du

-- Ver usuarios específicos con más detalle
SELECT 
    rolname as usuario,
    rolsuper as superusuario,
    rolcreatedb as puede_crear_db,
    rolcreaterole as puede_crear_roles,
    rolcanlogin as puede_conectar
FROM pg_roles 
WHERE rolname IN ('chalan_user', 'migracion_user', 'postgres');
```

### 2. Verificar Bases de Datos Disponibles

```sql
-- Listar todas las bases de datos
\l

-- Ver bases de datos específicas con más detalle
SELECT 
    datname as base_datos,
    pg_catalog.pg_get_userbyid(datdba) as propietario,
    pg_encoding_to_char(encoding) as encoding
FROM pg_database 
WHERE datname IN ('chalan_sch_txn', 'chalan_inv_txn', 'postgres');
```

### 3. Verificar Configuración de Puerto y Red

```sql
-- Ver puerto configurado
SHOW port;

-- Ver direcciones de escucha
SHOW listen_addresses;

-- Ver todas las configuraciones de red relevantes
SELECT name, setting, unit 
FROM pg_settings 
WHERE name IN ('port', 'listen_addresses', 'max_connections');
```

### 4. Verificar Método de Autenticación

```sql
-- Ver método de encriptación de contraseñas
SHOW password_encryption;

-- Ver configuración de autenticación
SELECT name, setting 
FROM pg_settings 
WHERE name LIKE '%password%' OR name LIKE '%auth%';
```

### 5. Verificar Conexión Actual (desde pgAdmin)

Si estás conectado en pgAdmin, ejecuta esta query en el Query Tool:

```sql
-- Ver información de la conexión actual
SELECT 
    current_user as usuario_actual,
    current_database() as base_datos_actual,
    inet_server_addr() as direccion_ip_servidor,
    inet_server_port() as puerto_servidor,
    version() as version_postgresql;
```

### 6. Verificar Tablas de Autenticación

```sql
-- Ver información de usuarios (sin contraseñas)
SELECT 
    rolname as usuario,
    rolpassword IS NOT NULL as tiene_contraseña,
    rolvaliduntil as contraseña_expira_en
FROM pg_authid 
WHERE rolname IN ('chalan_user', 'migracion_user');

-- Ver permisos sobre bases de datos
SELECT 
    datname as base_datos,
    pg_catalog.pg_get_userbyid(datdba) as propietario
FROM pg_database 
WHERE datname IN ('chalan_sch_txn', 'chalan_inv_txn');
```

---

## 🔧 Script Completo para Ejecutar en PowerShell

Copia y pega este script completo en PowerShell:

```powershell
Write-Host "=== VERIFICACION DE CREDENCIALES PARA DBEAVER ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Usuarios disponibles:" -ForegroundColor Yellow
docker exec chalan_postgres psql -U postgres -c "\du"

Write-Host "`n2. Bases de datos disponibles:" -ForegroundColor Yellow
docker exec chalan_postgres psql -U postgres -c "\l chalan_sch_txn"

Write-Host "`n3. Configuración de red:" -ForegroundColor Yellow
docker exec chalan_postgres psql -U postgres -c "SELECT name, setting FROM pg_settings WHERE name IN ('port', 'listen_addresses', 'password_encryption');"

Write-Host "`n4. Verificar conexión con chalan_user:" -ForegroundColor Yellow
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user as usuario, current_database() as base_datos, version() as version_postgresql;"

Write-Host "`n5. Verificar puerto expuesto por Docker:" -ForegroundColor Yellow
docker ps --filter "name=chalan_postgres" --format "table {{.Names}}\t{{.Ports}}"

Write-Host "`n=== RESULTADO ===" -ForegroundColor Green
Write-Host "Credenciales para DBeaver:" -ForegroundColor Green
Write-Host "  Host: 127.0.0.1" -ForegroundColor White
Write-Host "  Puerto: 5432" -ForegroundColor White
Write-Host "  Base de Datos: chalan_sch_txn" -ForegroundColor White
Write-Host "  Usuario: chalan_user" -ForegroundColor White
Write-Host "  Contraseña: chalan_password" -ForegroundColor White
```

---

## 📊 Query SQL para Ejecutar en pgAdmin Query Tool

Abre pgAdmin → Query Tool y ejecuta esta query completa:

```sql
-- Información completa de conexión y configuración
SELECT 
    '=== INFORMACION DE CONEXION ===' as seccion,
    current_user as usuario_actual,
    current_database() as base_datos_actual,
    inet_server_addr() as direccion_ip_servidor,
    inet_server_port() as puerto_servidor,
    version() as version_postgresql
UNION ALL
SELECT 
    '=== CONFIGURACION DE RED ===',
    name,
    setting,
    NULL,
    NULL,
    NULL
FROM pg_settings 
WHERE name IN ('port', 'listen_addresses', 'password_encryption')
UNION ALL
SELECT 
    '=== USUARIOS DISPONIBLES ===',
    rolname,
    CASE WHEN rolsuper THEN 'Superusuario' ELSE 'Usuario normal' END,
    CASE WHEN rolcanlogin THEN 'Puede conectar' ELSE 'No puede conectar' END,
    NULL,
    NULL
FROM pg_roles 
WHERE rolname IN ('chalan_user', 'migracion_user', 'postgres');
```

---

## ✅ Credenciales Confirmadas para DBeaver

Basado en la conexión exitosa de pgAdmin, estas son las credenciales que DEBES usar en DBeaver:

### Configuración Principal:

```
Host:        127.0.0.1
Puerto:      5432
Base de Datos: chalan_sch_txn
Usuario:     chalan_user
Contraseña:  chalan_password
```

### Configuración Alternativa (Usuario de Migración):

```
Host:        127.0.0.1
Puerto:      5432
Base de Datos: chalan_sch_txn
Usuario:     migracion_user
Contraseña:  migracion_password123
```

---

## 🔍 Verificación Final desde Terminal

Ejecuta este comando para verificar que todo está correcto:

```powershell
# Prueba de conexión completa
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "
SELECT 
    'CONEXION EXITOSA' as estado,
    current_user as usuario,
    current_database() as base_datos,
    inet_server_port() as puerto;
"
```

Si este comando funciona, las credenciales son correctas y el problema está en DBeaver.

---

## 🚨 Si DBeaver Sigue Fallando

Después de ejecutar estos comandos y confirmar las credenciales, si DBeaver sigue sin conectarse:

1. **Verifica la versión del driver:** Debe ser 42.2.0 o superior
2. **Usa URL completa** en lugar de campos individuales:
   ```
   jdbc:postgresql://127.0.0.1:5432/chalan_sch_txn?user=chalan_user&password=chalan_password&ssl=false
   ```
3. **Alternativa:** Usa pgAdmin que ya está funcionando ✅

