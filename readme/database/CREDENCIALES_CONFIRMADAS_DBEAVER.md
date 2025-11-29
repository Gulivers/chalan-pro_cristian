# ✅ Credenciales Confirmadas para DBeaver (Verificado desde pgAdmin)

## 📊 Resultados de la Verificación

### ✅ Usuarios Disponibles:
- **chalan_user** - Superusuario, Create DB ✅
- **migracion_user** - Superusuario, Create role, Create DB, Replication, Bypass RLS ✅
- **postgres** - Superusuario (por defecto)

### ✅ Bases de Datos Disponibles:
- **chalan_sch_txn** - Propietario: chalan_user ✅
- **chalan_inv_txn** - Propietario: postgres

### ✅ Configuración de Red:
- **Puerto:** `5432` ✅
- **Escucha en:** `*` (todas las interfaces) ✅
- **Método de autenticación:** `scram-sha-256` ✅
- **Puerto expuesto por Docker:** `0.0.0.0:5432->5432/tcp` ✅

---

## 🔐 Credenciales EXACTAS para DBeaver

### Configuración Principal (Recomendada):

```
┌─────────────────────────────────────────┐
│ Host:        127.0.0.1                  │
│ Puerto:      5432                        │
│ Base de Datos: chalan_sch_txn           │
│ Usuario:     chalan_user                 │
│ Contraseña:  chalan_password             │
└─────────────────────────────────────────┘
```

### Configuración Alternativa (Usuario de Migración):

```
┌─────────────────────────────────────────┐
│ Host:        127.0.0.1                  │
│ Puerto:      5432                        │
│ Base de Datos: chalan_sch_txn           │
│ Usuario:     migracion_user             │
│ Contraseña:  migracion_password123      │
└─────────────────────────────────────────┘
```

---

## 🔧 Configuración del Driver en DBeaver

### Paso 1: Verificar Versión del Driver
- Debe ser **42.2.0 o superior** para soportar `scram-sha-256`
- Si no, actualiza desde: https://jdbc.postgresql.org/download/

### Paso 2: Configurar Propiedades del Driver
En **Edit Driver → Default properties**, agrega:
```
ssl=false
sslmode=disable
```

### Paso 3: Configurar Conexión
- **Connect by:** Host (no URL)
- **Host:** `127.0.0.1` ← **CRÍTICO: NO uses localhost**
- **Port:** `5432`
- **Database:** `chalan_sch_txn`
- **Authentication:** Database Native
- **Username:** `chalan_user`
- **Password:** `chalan_password` ← **Escribe manualmente**

---

## 📋 URL JDBC Completa (Para Prueba)

Si quieres probar con URL completa en lugar de campos individuales:

```
jdbc:postgresql://127.0.0.1:5432/chalan_sch_txn?user=chalan_user&password=chalan_password&ssl=false
```

**Nota:** Esto es solo para prueba. Si funciona con URL completa, el problema es la configuración de autenticación en los campos individuales.

---

## ✅ Verificación Final

Ejecuta este comando para confirmar que las credenciales funcionan:

```powershell
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user, current_database();"
```

**Resultado esperado:**
```
 current_user | current_database 
--------------+------------------
 chalan_user  | chalan_sch_txn
```

Si esto funciona pero DBeaver no, el problema es específico del driver JDBC en DBeaver.

---

## 🚨 Checklist Final para DBeaver

- [ ] Driver PostgreSQL versión 42.2.0 o superior
- [ ] Properties del driver: `ssl=false` y `sslmode=disable`
- [ ] Host: `127.0.0.1` (NO localhost)
- [ ] Puerto: `5432`
- [ ] Base de datos: `chalan_sch_txn`
- [ ] Usuario: `chalan_user`
- [ ] Contraseña: `chalan_password` (escrita manualmente, sin espacios)
- [ ] Authentication: `Database Native`
- [ ] Conexión funciona desde terminal (verificado ✅)

---

## 💡 Alternativa Confirmada: pgAdmin

Si DBeaver sigue dando problemas, usa **pgAdmin** que ya está funcionando:
- URL: `http://localhost:5050`
- Email: `admin@chalan.com`
- Password: `chalan_password` (o la de tu `.env`)
- Servidor: `chalan_postgres` (nombre del contenedor)
- Base de datos: `chalan_sch_txn`

---

## 📝 Comandos PSQL para Ejecutar desde pgAdmin

Puedes ejecutar estos comandos en el Query Tool de pgAdmin para verificar:

```sql
-- Ver información de conexión actual
SELECT 
    current_user as usuario_actual,
    current_database() as base_datos_actual,
    inet_server_port() as puerto_servidor,
    version() as version_postgresql;

-- Ver usuarios disponibles
SELECT 
    rolname as usuario,
    rolsuper as superusuario,
    rolcanlogin as puede_conectar
FROM pg_roles 
WHERE rolname IN ('chalan_user', 'migracion_user');

-- Ver bases de datos disponibles
SELECT 
    datname as base_datos,
    pg_catalog.pg_get_userbyid(datdba) as propietario
FROM pg_database 
WHERE datname IN ('chalan_sch_txn', 'chalan_inv_txn');
```

