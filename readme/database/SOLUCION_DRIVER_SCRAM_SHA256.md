# 🔧 Solución Específica: Driver PostgreSQL con SCRAM-SHA-256

## 🎯 Problema Identificado

PostgreSQL 16 usa `scram-sha-256` para autenticación. Algunas versiones antiguas del driver JDBC de PostgreSQL pueden tener problemas con este método.

---

## ✅ Solución 1: Actualizar Driver en DBeaver

### Paso 1: Descargar Driver Actualizado

1. En DBeaver: **Window → Preferences → Drivers → PostgreSQL**
2. Click en **"Download"** o descarga manualmente:
   - Ve a: https://jdbc.postgresql.org/download.html
   - Descarga la versión más reciente (ej: `postgresql-42.7.1.jar` o superior)

### Paso 2: Configurar Driver Correctamente

En **Edit Driver 'PostgreSQL'**, configura:

**Settings:**
- Driver Type: `PostgreSQL`
- Class Name: `org.postgresql.Driver`
- URL Template: `jdbc:postgresql://{host}[:{port}]/[{database}]`
- Default Port: `5432`

**Default properties** (pestaña "Default properties"):
```
ssl=false
sslmode=disable
```

**Advanced parameters** (opcional):
```
connectTimeout=10
socketTimeout=10
```

---

## ✅ Solución 2: Usar URL Completa con Parámetros

En lugar de usar los campos individuales, prueba usar la **URL completa**:

1. En DBeaver, en la sección **Connect by**, selecciona **URL** (no "Host")
2. Usa esta URL exacta (reemplaza con tus credenciales):
```
jdbc:postgresql://127.0.0.1:5432/chalan_sch_txn?user=chalan_user&password=chalan_password&ssl=false
```

**⚠️ Nota:** Esto es solo para prueba. Si funciona, confirma que el problema es la configuración de autenticación.

---

## ✅ Solución 3: Verificar Versión del Driver

El driver debe ser versión **42.2.0 o superior** para soportar correctamente `scram-sha-256`.

Para verificar:
1. En DBeaver: **Window → Preferences → Drivers → PostgreSQL**
2. Pestaña **Libraries**
3. Verifica que tengas `postgresql-42.2.0.jar` o superior

Si tienes una versión anterior:
1. Click en **Remove**
2. Click en **Add File** o **Download**
3. Selecciona la versión más reciente

---

## ✅ Solución 4: Cambiar Método de Autenticación Temporalmente (TEST)

**⚠️ SOLO PARA PRUEBAS - NO PARA PRODUCCIÓN**

Si necesitas probar rápidamente, podemos cambiar temporalmente a `md5`:

```powershell
# 1. Cambiar a md5 temporalmente
docker exec chalan_postgres psql -U postgres -c "ALTER USER chalan_user WITH PASSWORD 'chalan_password';"
docker exec chalan_postgres psql -U postgres -c "ALTER SYSTEM SET password_encryption = 'md5';"
docker restart chalan_postgres

# 2. Probar conexión en DBeaver
# Si funciona, el problema es scram-sha-256 con tu versión del driver

# 3. Volver a scram-sha-256 (MÁS SEGURO)
docker exec chalan_postgres psql -U postgres -c "ALTER SYSTEM SET password_encryption = 'scram-sha-256';"
docker exec chalan_postgres psql -U postgres -c "ALTER USER chalan_user WITH PASSWORD 'chalan_password';"
docker restart chalan_postgres
```

---

## ✅ Solución 5: Usar pgAdmin (Alternativa)

Si DBeaver sigue dando problemas, usa pgAdmin que ya está configurado:

1. Abre: `http://localhost:5050`
2. Login:
   - Email: `admin@chalan.com`
   - Password: `chalan_password` (o la que tengas en `.env` como `POSTGRES_PASSWORD`)
3. Agregar Servidor:
   - **General → Name:** `chalan_local`
   - **Connection → Host:** `chalan_postgres` (nombre del contenedor)
   - **Connection → Port:** `5432`
   - **Connection → Database:** `chalan_sch_txn`
   - **Connection → Username:** `chalan_user`
   - **Connection → Password:** `chalan_password`

---

## 🔍 Diagnóstico: Verificar que PostgreSQL funciona

```powershell
# Esto DEBE funcionar desde terminal
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user, version();"
```

Si esto funciona pero DBeaver no, el problema es específico del driver JDBC en DBeaver.

---

## 📋 Checklist Final

- [ ] Driver PostgreSQL versión 42.2.0 o superior
- [ ] Properties del driver: `ssl=false` y `sslmode=disable`
- [ ] Probar con URL completa en lugar de campos individuales
- [ ] Verificar que la conexión funciona desde terminal
- [ ] Si nada funciona, usar pgAdmin como alternativa

---

## 🚨 Si Nada Funciona

El problema más probable es la versión del driver. Asegúrate de tener la versión más reciente:

1. Elimina el driver actual en DBeaver
2. Descarga manualmente: https://jdbc.postgresql.org/download/
3. Instala la versión más reciente
4. Vuelve a intentar la conexión

