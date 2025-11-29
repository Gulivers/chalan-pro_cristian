# Credenciales de Usuarios PostgreSQL Local

## Usuario de Migración (NUEVO - Recomendado para importar datos)

### Credenciales:
- **Host:** `127.0.0.1`
- **Puerto:** `5432`
- **Usuario:** `migracion_user`
- **Contraseña:** `migracion_password123`
- **Base de Datos:** `chalan_sch_txn`

### Privilegios:
- ✅ **Superusuario** (todos los privilegios)
- ✅ **Crear bases de datos**
- ✅ **Crear roles**
- ✅ **Replicación**
- ✅ **Bypass RLS** (Row Level Security)
- ✅ **COPY** (importar CSV)
- ✅ **INSERT, UPDATE, DELETE** en todas las tablas

---

## Usuario Existente Mejorado (chalan_user)

### Credenciales:
- **Host:** `127.0.0.1`
- **Puerto:** `5432`
- **Usuario:** `chalan_user`
- **Contraseña:** `chalan_password`
- **Base de Datos:** `chalan_sch_txn`

### Privilegios:
- ✅ **Superusuario** (mejorado)
- ✅ **Crear bases de datos**
- ✅ **Todos los privilegios** sobre `chalan_sch_txn`

---

## Ejemplos de Uso Rápido

### 1. Conectar desde DBeaver/Navicat
Usa cualquiera de las dos credenciales anteriores.

### 2. Importar CSV desde terminal:
```bash
docker exec -it chalan_postgres psql -U migracion_user -d chalan_sch_txn

# Luego en psql:
COPY nombre_tabla FROM '/tmp/datos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

### 3. Insertar datos manualmente:
```sql
INSERT INTO nombre_tabla (col1, col2) VALUES ('valor1', 'valor2');
```

### 4. Importar archivo SQL:
```bash
docker cp datos.sql chalan_postgres:/tmp/datos.sql
docker exec chalan_postgres psql -U migracion_user -d chalan_sch_txn -f /tmp/datos.sql
```

---

## Notas Importantes

- ⚠️ El usuario `migracion_user` tiene privilegios de superusuario - úsalo solo para migración de datos
- ⚠️ Para desarrollo normal, usa `chalan_user` 
- ⚠️ Para producción en Render, usa las credenciales de Render

---

## Verificar Conexión

```bash
# Probar conexión con migracion_user
docker exec chalan_postgres psql -U migracion_user -d chalan_sch_txn -c "SELECT current_user, current_database();"

# Probar conexión con chalan_user
docker exec chalan_postgres psql -U chalan_user -d chalan_sch_txn -c "SELECT current_user, current_database();"
```

