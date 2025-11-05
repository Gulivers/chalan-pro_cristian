# 🔌 Conexión a PostgreSQL Local con Navicat

Esta guía te ayudará a conectarte a PostgreSQL local usando Navicat para migrar datos de MySQL a PostgreSQL.

## 🚨 Solución Rápida: Error "password authentication failed"

Si recibes el error: `FATAL: password authentication failed for user "chalan_user"`

**Solución inmediata:**
1. En Navicat, cambia el **Host** de `localhost` a `127.0.0.1`
2. Usa estas credenciales exactas:
   - **Host:** `127.0.0.1` (NO `localhost`)
   - **Puerto:** `5432`
   - **Usuario:** `chalan_user`
   - **Contraseña:** `chalan_password`
   - **Base de Datos:** `chalan_sch_txn`

**¿Por qué funciona?**
- `localhost` puede resolverse a IPv6 (`::1`) que causa problemas de autenticación
- `127.0.0.1` fuerza IPv4, que funciona correctamente con Docker

---

## 📋 Requisitos Previos

1. **PostgreSQL debe estar corriendo** en Docker
   ```powershell
   docker ps | Select-String "chalan-postgres"
   ```
   Si no está corriendo:
   ```powershell
   docker-compose -f docker-compose.local.yml up -d postgres
   ```

2. **Navicat instalado** (cualquier versión que soporte PostgreSQL)

## 🔧 Datos de Conexión para Navicat

Basado en tu configuración en `docker-compose.local.yml`, estos son los datos que necesitas:

### Configuración de Conexión

| Campo | Valor |
|-------|-------|
| **Nombre de Conexión** | `chalan-postgres-local` (o el que prefieras) |
| **Tipo de Base de Datos** | `PostgreSQL` |
| **Host** | `127.0.0.1` ⚠️ **Usa IPv4, NO localhost** |
| **Puerto** | `5432` |
| **Usuario** | `chalan_user` (o el valor de `POSTGRES_USER` en tu `.env`) |
| **Contraseña** | `chalan_password` (o el valor de `POSTGRES_PASSWORD` en tu `.env`) |
| **Base de Datos** | `chalan_sch_txn` (o el valor de `POSTGRES_DB` en tu `.env`) |

### ⚠️ Importante: Verificar tus Valores

Los valores exactos dependen de tu archivo `.env`. Para verificar:

1. **Verificar variables en Docker Compose:**
   ```powershell
   docker-compose -f docker-compose.local.yml config
   ```

2. **O verificar directamente en el contenedor:**
   ```powershell
   docker exec chalan-postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_database(), current_user;"
   ```

## 📝 Pasos para Conectar en Navicat

### Paso 1: Crear Nueva Conexión

1. Abre **Navicat**
2. Haz clic en **Connection** → **PostgreSQL** (o el botón "New Connection")
3. Se abrirá el diálogo de conexión

### Paso 2: Configurar la Conexión

En el diálogo de conexión, completa:

**Pestaña "General":**
- **Connection Name:** `chalan-postgres-local`
- **Host:** `127.0.0.1` ⚠️ **IMPORTANTE: Usa IPv4, NO localhost**
- **Port:** `5432`
- **Initial Database:** `chalan_sch_txn`
- **Username:** `chalan_user`
- **Password:** `chalan_password` (o tu contraseña del `.env`)

> ⚠️ **SOLUCIÓN PARA ERROR DE AUTENTICACIÓN:**
> Si recibes el error "password authentication failed", usa `127.0.0.1` en lugar de `localhost` en el campo Host.
> Esto evita problemas con IPv6 (`::1`) que pueden causar errores de autenticación.

**Pestaña "Advanced" (Opcional):**
- **Connection Timeout:** `10` (segundos)
- **Keep-alive Interval:** `30` (segundos)

### Paso 3: Probar la Conexión

1. Haz clic en **Test Connection**
2. Si es exitoso, verás "Connection successful"
3. Si falla, verifica:
   - Que PostgreSQL esté corriendo: `docker ps`
   - Que el puerto 5432 esté disponible: `netstat -an | Select-String "5432"`
   - Que las credenciales coincidan con tu `.env`

### Paso 4: Guardar y Conectar

1. Haz clic en **OK** para guardar la conexión
2. Haz doble clic en la conexión para conectarte
3. Deberías ver tu base de datos `chalan_sch_txn` en el árbol

## 🔍 Verificar Variables de tu `.env`

Si no recuerdas los valores exactos de tu `.env`, puedes verificar:

```powershell
# Ver las variables de entorno del contenedor PostgreSQL
docker exec chalan-postgres env | Select-String "POSTGRES"

# O conectarte directamente para verificar
docker exec -it chalan-postgres psql -U postgres -c "\du"
```

## 📊 Migración de MySQL a PostgreSQL

Una vez conectado con Navicat, puedes migrar datos:

### Opción 1: Usar la Herramienta de Migración de Navicat

1. En Navicat, ve a **Tools** → **Data Transfer** (o **Transfer Database**)
2. **Source:** Selecciona tu conexión MySQL
3. **Destination:** Selecciona tu conexión PostgreSQL (`chalan-postgres-local`)
4. Selecciona las tablas que quieres migrar
5. Configura opciones de migración:
   - **Drop Tables:** No (para no borrar datos existentes)
   - **Create Tables:** Sí (si las tablas no existen)
   - **Insert Data:** Sí
6. Haz clic en **Start** para iniciar la migración

### Opción 2: Exportar/Importar Manualmente

1. **Exportar desde MySQL:**
   - Conecta a MySQL en Navicat
   - Selecciona la base de datos MySQL
   - Right-click → **Dump SQL File** → **Structure and Data**
   - Guarda el archivo SQL

2. **Ajustar el SQL para PostgreSQL:**
   - PostgreSQL tiene algunas diferencias con MySQL
   - Puedes usar herramientas como `pgloader` o ajustar manualmente:
     - `AUTO_INCREMENT` → `SERIAL` o `GENERATED ALWAYS AS IDENTITY`
     - `` `backticks` `` → `"double quotes"` o eliminar
     - `ENGINE=InnoDB` → Eliminar (no aplica en PostgreSQL)

3. **Importar a PostgreSQL:**
   - Conecta a PostgreSQL en Navicat
   - Selecciona la base de datos `chalan_sch_txn`
   - Right-click → **Execute SQL File**
   - Selecciona el archivo SQL ajustado

### Opción 3: Usar pgloader (Recomendado para Migraciones Complejas)

```powershell
# Instalar pgloader (si no lo tienes)
# Windows: Descargar desde https://github.com/dimitri/pgloader/releases

# Migrar desde MySQL a PostgreSQL
pgloader mysql://usuario:password@localhost:3306/mysql_db \
         postgresql://chalan_user:chalan_password@localhost:5432/chalan_sch_txn
```

## 🛠️ Solución de Problemas

### Error: "Connection refused"
- **Causa:** PostgreSQL no está corriendo
- **Solución:**
  ```powershell
  docker-compose -f docker-compose.local.yml up -d postgres
  ```

### Error: "Password authentication failed"
- **Causa:** Usuario o contraseña incorrectos
- **Solución:** Verifica tu `.env` o usa:
  ```powershell
  docker exec chalan-postgres psql -U postgres -c "\du"
  ```

### Error: "Database does not exist"
- **Causa:** La base de datos no existe en PostgreSQL
- **Solución:** Créala:
  ```powershell
  docker exec -it chalan-postgres psql -U chalan_user -d postgres -c "CREATE DATABASE chalan_sch_txn;"
  ```

### Error: "Port 5432 is already in use"
- **Causa:** Otro servicio está usando el puerto 5432
- **Solución:**
  ```powershell
  # Ver qué está usando el puerto
  netstat -ano | Select-String "5432"
  
  # O cambiar el puerto en docker-compose.local.yml
  # Cambia "5432:5432" a "5433:5432"
  ```

## ✅ Verificación Post-Migración

Después de migrar, verifica:

```sql
-- Conectado a PostgreSQL en Navicat, ejecuta:

-- Ver todas las tablas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Ver conteo de registros por tabla
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables
ORDER BY tablename;

-- Verificar estructura de una tabla específica
\d nombre_de_tabla
```

## 📚 Referencias

- [Navicat Documentation](https://www.navicat.com/manual/online_manual/en/navicat/win_manual/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [pgloader Documentation](https://pgloader.readthedocs.io/)

---

**Nota:** Si cambias las credenciales en tu `.env`, necesitarás actualizar la conexión en Navicat también.

