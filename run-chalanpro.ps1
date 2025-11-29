Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -WindowStyle Hidden

# ---------------------------------------------------------------
# 2) Wait for Docker Engine to become ready
# ---------------------------------------------------------------
Write-Host " Waiting for Docker Engine to boot..."

# Wait until "docker info" stops throwing errors
$maxAttempts = 40
$attempt = 0

while ($attempt -lt $maxAttempts) {
    try {
        docker info > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker Engine is ready!"
            break
        }
    } catch {}

    Start-Sleep -Seconds 2
    $attempt++
}

if ($attempt -eq $maxAttempts) {
    Write-Host "Docker Engine did not start. Exiting..."
    exit
}

# ---------------------------------------------------------------
# 3) Set project directory
# ---------------------------------------------------------------
$projectPath = "D:\MisDesarrollos\Driver_ChalanProyect\chalan_tenant_sch"

Write-Host ""
Write-Host " Switching to project directory..."
Set-Location $projectPath

# ---------------------------------------------------------------
# 4) Start backend stack using docker-compose
# ---------------------------------------------------------------
Write-Host ""
Write-Host "Starting backend services with docker-compose..."

docker-compose -f docker-compose.local.yml restart backend
docker-compose -f docker-compose.local.yml restart postgres
docker-compose -f docker-compose.local.yml restart pgadmin
docker-compose -f docker-compose.local.yml restart redis

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error starting backend services."
    exit
}

Write-Host "Backend services running in background!"

# ---------------------------------------------------------------
# 5) Start frontend Vue
# ---------------------------------------------------------------
Write-Host ""
Write-Host "Starting Vue frontend..."

Set-Location "$projectPath\vuefrontend"

npm run serve

Write-Host ""
Write-Host "=============================================="
Write-Host " Chalan-Pro is LIVE on your local environment"
Write-Host " Backend: Docker (running underground)        "
Write-Host " Frontend: npm run serve                      "
Write-Host "=============================================="
