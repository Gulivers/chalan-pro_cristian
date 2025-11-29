# Script para resetear contraseña de PostgreSQL y verificar conexión
# Ejecuta: .\fix-postgres-password.ps1

Write-Host "`n=== Solución de Problemas de Conexión PostgreSQL ===" -ForegroundColor Cyan
Write-Host ""

# Verificar si el contenedor está corriendo
$container = docker ps --filter "name=chalan_postgres" --format "{{.Names}}"
if (-not $container) {
    Write-Host "⚠️  El contenedor PostgreSQL no está corriendo" -ForegroundColor Yellow
    Write-Host "   Ejecuta: docker-compose -f docker-compose.local.yml up -d postgres" -ForegroundColor Yellow
    exit
}

Write-Host "✓ Contenedor PostgreSQL encontrado: $container" -ForegroundColor Green
Write-Host ""

# Obtener credenciales actuales
$envVars = docker exec $container env | Select-String "POSTGRES"
$user = ($envVars | Select-String "POSTGRES_USER").ToString().Split("=")[1]
$password = ($envVars | Select-String "POSTGRES_PASSWORD").ToString().Split("=")[1]
$db = ($envVars | Select-String "POSTGRES_DB").ToString().Split("=")[1]

Write-Host "Credenciales actuales:" -ForegroundColor Yellow
Write-Host "  Usuario: $user" -ForegroundColor White
Write-Host "  Contraseña: $password" -ForegroundColor White
Write-Host "  Base de Datos: $db" -ForegroundColor White
Write-Host ""

# Resetear contraseña
Write-Host "Reseteando contraseña del usuario $user..." -ForegroundColor Yellow
$resetResult = docker exec $container psql -U postgres -c "ALTER USER $user WITH PASSWORD '$password';" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Contrasena reseteada exitosamente" -ForegroundColor Green
} else {
    Write-Host "ERROR: Error al resetear contrasena: $resetResult" -ForegroundColor Red
}

Write-Host ""

# Probar conexión desde Docker
Write-Host "Probando conexión desde Docker..." -ForegroundColor Yellow
$testConnection = docker exec $container psql -U $user -d $db -c "SELECT 'Connection successful!' as status;" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Conexión exitosa desde Docker" -ForegroundColor Green
} else {
    Write-Host "⚠️  Error en la conexión: $testConnection" -ForegroundColor Red
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  DATOS PARA NAVICAT" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Tipo:      PostgreSQL" -ForegroundColor White
Write-Host "  Host:      127.0.0.1 (usa IPv4, NO localhost)" -ForegroundColor Green
Write-Host "  Puerto:    5432" -ForegroundColor White
Write-Host "  Usuario:   $user" -ForegroundColor White
Write-Host "  Contraseña: $password" -ForegroundColor White
Write-Host "  Base de Datos: $db" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: En Navicat, usa '127.0.0.1' en lugar de 'localhost'" -ForegroundColor Yellow
Write-Host "   Esto evita problemas con IPv6 (::1)" -ForegroundColor Yellow
Write-Host ""

# Verificar puerto
Write-Host "Verificando puerto 5432..." -ForegroundColor Yellow
$portCheck = netstat -an | Select-String ":5432" | Select-String "LISTENING"
if ($portCheck) {
    Write-Host "✓ Puerto 5432 está escuchando" -ForegroundColor Green
    Write-Host "  $portCheck" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Puerto 5432 no está escuchando" -ForegroundColor Yellow
}

Write-Host ""

