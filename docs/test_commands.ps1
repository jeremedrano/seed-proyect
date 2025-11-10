# Script de Pruebas Manuales - User Management API
# Ejecutar línea por línea o todo el script

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "User Management API - Test Suite" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$BASE_URL = "http://localhost:8000"
$API_URL = "$BASE_URL/api/v1"

Write-Host "Base URL: $BASE_URL" -ForegroundColor Yellow
Write-Host ""

# ======================
# 1. TESTS BÁSICOS
# ======================

Write-Host "1. Testing Health Check..." -ForegroundColor Green
curl "$BASE_URL/health"
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "2. Testing Root Endpoint..." -ForegroundColor Green
curl "$BASE_URL/"
Write-Host ""
Start-Sleep -Seconds 1

# ======================
# 2. CREAR USUARIOS (ÉXITO)
# ======================

Write-Host "3. Creating User 1 (Juan Pérez)..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan.perez@example.com",
    "name": "Juan Pérez",
    "age": 30
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "4. Creating User 2 (María García)..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "maria.garcia@example.com",
    "name": "María García",
    "age": 25
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "5. Creating User 3 (Pedro López)..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "pedro.lopez@example.com",
    "name": "Pedro López",
    "age": 35
  }'
Write-Host ""
Start-Sleep -Seconds 1

# ======================
# 3. VALIDACIONES (ERROR)
# ======================

Write-Host "6. Testing Duplicate Email (should return 400)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan.perez@example.com",
    "name": "Otro Juan",
    "age": 40
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "7. Testing Invalid Email (should return 422)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "email-sin-arroba",
    "name": "Test User",
    "age": 25
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "8. Testing Negative Age (should return 422)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "age": -10
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "9. Testing Zero Age (should return 422)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "age": 0
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "10. Testing Empty Name (should return 422)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "",
    "age": 25
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "11. Testing Missing Fields (should return 422)..." -ForegroundColor Yellow
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com"
  }'
Write-Host ""
Start-Sleep -Seconds 1

# ======================
# 4. CASOS ADICIONALES
# ======================

Write-Host "12. Creating User with Minimum Age (18)..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "young@example.com",
    "name": "Usuario Joven",
    "age": 18
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "13. Creating User with High Age (100)..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "old@example.com",
    "name": "Usuario Mayor",
    "age": 100
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "14. Testing Long Name..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "longname@example.com",
    "name": "Juan Carlos Alberto Francisco de la Santísima Trinidad García López",
    "age": 45
  }'
Write-Host ""
Start-Sleep -Seconds 1

Write-Host "15. Testing Special Characters in Name..." -ForegroundColor Green
curl -X POST "$API_URL/users/" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "special@example.com",
    "name": "José María Ñoño OConnor",
    "age": 40
  }'
Write-Host ""
Start-Sleep -Seconds 1

# ======================
# RESUMEN
# ======================

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Tests Completed!" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Summary:" -ForegroundColor White
Write-Host "  - Health checks: 2" -ForegroundColor White
Write-Host "  - Success cases: 7" -ForegroundColor Green
Write-Host "  - Error cases: 6" -ForegroundColor Yellow
Write-Host "  - Total tests: 15" -ForegroundColor White
Write-Host ""
Write-Host "Check the responses above to verify:" -ForegroundColor White
Write-Host "  ✅ Success cases returned 201" -ForegroundColor Green
Write-Host "  ✅ Duplicate email returned 400" -ForegroundColor Green
Write-Host "  ✅ Invalid data returned 422" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Check users.db file exists" -ForegroundColor White
Write-Host "  2. Open http://localhost:8000/api/v1/docs" -ForegroundColor White
Write-Host "  3. Run automated tests: pytest tests/ -v" -ForegroundColor White
Write-Host ""

