# Guía de Migración de Datos a PostgreSQL Local

## Credenciales de Usuario de Migración

### Usuario: `migracion_user`
- **Host:** `127.0.0.1`
- **Puerto:** `5432`
- **Usuario:** `migracion_user`
- **Contraseña:** `migracion_password123`
- **Base de Datos:** `chalan_sch_txn`

### Usuario Alternativo: `chalan_user` (mejorado)
- **Host:** `127.0.0.1`
- **Puerto:** `5432`
- **Usuario:** `chalan_user`
- **Contraseña:** `chalan_password`
- **Base de Datos:** `chalan_sch_txn`

---

## Método 1: Importar desde CSV usando COPY

### Usando psql desde terminal:

```bash
# Conectarse a PostgreSQL
docker exec -it chalan_postgres psql -U migracion_user -d chalan_sch_txn

# Importar CSV (ejemplo)
COPY nombre_tabla FROM '/tmp/datos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

### Usando DBeaver/Navicat:

1. **Importar CSV desde DBeaver:**
   - Click derecho en la tabla → `Import Data`
   - Seleccionar archivo CSV
   - Configurar delimitador y encoding
   - Ejecutar importación

2. **Importar CSV desde Navicat:**
   - Click derecho en la tabla → `Import Wizard`
   - Seleccionar archivo CSV
   - Configurar mapping de columnas
   - Ejecutar importación

---

## Método 2: Insertar datos manualmente

### Ejemplo de INSERT múltiple:

```sql
BEGIN;

INSERT INTO nombre_tabla (columna1, columna2, columna3) VALUES
    ('valor1', 'valor2', 'valor3'),
    ('valor4', 'valor5', 'valor6'),
    ('valor7', 'valor8', 'valor9');

COMMIT;
```

---

## Método 3: Importar desde archivo SQL

### Crear archivo de datos (datos.sql):

```sql
-- datos.sql
BEGIN;

INSERT INTO nombre_tabla (columna1, columna2) VALUES
    ('dato1', 'dato2'),
    ('dato3', 'dato4');

COMMIT;
```

### Ejecutar desde terminal:

```bash
docker exec -i chalan_postgres psql -U migracion_user -d chalan_sch_txn < datos.sql
```

### Ejecutar desde Docker (copiando archivo primero):

```bash
# Copiar archivo al contenedor
docker cp datos.sql chalan_postgres:/tmp/datos.sql

# Ejecutar SQL
docker exec chalan_postgres psql -U migracion_user -d chalan_sch_txn -f /tmp/datos.sql
```

---

## Método 4: Importar CSV usando Python (Django)

```python
import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apptransactions.models import TuModelo

with open('datos.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        TuModelo.objects.create(**row)
```

---

## Método 5: Importar desde MySQL (si tienes datos en MySQL)

### Usando pgLoader:

```bash
# Instalar pgloader (si no está instalado)
# En Windows: descargar desde https://github.com/dimitri/pgloader/releases

pgloader mysql://user:password@localhost/mysql_db \
         postgresql://migracion_user:migracion_password123@127.0.0.1:5432/chalan_sch_txn
```

---

## Verificación de Datos Importados

```sql
-- Contar registros en una tabla
SELECT COUNT(*) FROM nombre_tabla;

-- Ver algunos registros
SELECT * FROM nombre_tabla LIMIT 10;

-- Verificar estructura de la tabla
\d nombre_tabla
```

---

## Troubleshooting

### Error: "permission denied for schema public"
**Solución:** Ejecutar el script `crear_usuario_migracion.sql` o `mejorar_privilegios_chalan_user.sql`

### Error: "COPY requires superuser privilege"
**Solución:** Usar el usuario `migracion_user` que tiene privilegios de superusuario

### Error: "relation does not exist"
**Solución:** Verificar que la tabla existe: `\dt` o `SELECT * FROM information_schema.tables WHERE table_schema = 'public';`

---

## Notas Importantes

1. **Backup antes de migrar:** Siempre hacer backup de la base de datos antes de importar datos
2. **Transacciones:** Usar `BEGIN` y `COMMIT` para operaciones grandes
3. **Encoding:** Verificar que el CSV esté en UTF-8 si contiene caracteres especiales
4. **Validación:** Verificar la integridad de los datos después de la migración

