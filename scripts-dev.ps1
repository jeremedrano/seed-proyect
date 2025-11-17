# Scripts de Desarrollo - Proyecto CRUD Usuarios
# Ejecutar desde la raíz del proyecto

Write-Host "=== Scripts de Desarrollo ===" -ForegroundColor Cyan
Write-Host ""

# Función para ejecutar comandos con color
function Run-Command {
    param(
        [string]$Description,
        [string]$Command
    )
    Write-Host ">> $Description" -ForegroundColor Yellow
    Write-Host "   Comando: $Command" -ForegroundColor Gray
    Invoke-Expression $Command
    Write-Host ""
}

# Menú principal
Write-Host "Selecciona una opción:" -ForegroundColor Green
Write-Host "1.  Ejecutar TODOS los tests"
Write-Host "2.  Ejecutar solo tests unitarios (rápidos)"
Write-Host "3.  Ejecutar solo tests de integración"
Write-Host "4.  Ejecutar solo tests e2e"
Write-Host "5.  Ejecutar tests con cobertura HTML"
Write-Host "6.  Ejecutar tests con cobertura y fallar si < 80%"
Write-Host "7.  Watch mode (TDD) - solo unitarios"
Write-Host "8.  Ejecutar pylint"
Write-Host "9.  Ejecutar flake8"
Write-Host "10. Ejecutar black (check)"
Write-Host "11. Ejecutar black (format)"
Write-Host "12. Ejecutar isort (check)"
Write-Host "13. Ejecutar isort (format)"
Write-Host "14. Ejecutar pip-audit (seguridad)"
Write-Host "15. Ejecutar bandit (seguridad)"
Write-Host "16. PRE-COMMIT COMPLETO (todo)"
Write-Host "17. Instalar dependencias de desarrollo"
Write-Host "18. Iniciar servidor FastAPI"
Write-Host "0.  Salir"
Write-Host ""

$opcion = Read-Host "Ingresa el número de opción"

switch ($opcion) {
    "1" {
        Run-Command "Ejecutar TODOS los tests" "pytest tests/ -v"
    }
    "2" {
        Run-Command "Ejecutar solo tests unitarios" "pytest tests/ -v -m unit"
    }
    "3" {
        Run-Command "Ejecutar solo tests de integración" "pytest tests/ -v -m integration"
    }
    "4" {
        Run-Command "Ejecutar solo tests e2e" "pytest tests/ -v -m e2e"
    }
    "5" {
        Run-Command "Ejecutar tests con cobertura HTML" "pytest tests/ --cov=app --cov-report=html"
        Write-Host "Reporte generado en: htmlcov/index.html" -ForegroundColor Green
    }
    "6" {
        Run-Command "Ejecutar tests con cobertura (fail < 80%)" "pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80"
    }
    "7" {
        Run-Command "Watch mode (TDD) - solo unitarios" "ptw tests/unit/"
    }
    "8" {
        Run-Command "Ejecutar pylint" "pylint app/ --fail-under=8.0"
    }
    "9" {
        Run-Command "Ejecutar flake8" "flake8 app/ --max-line-length=100"
    }
    "10" {
        Run-Command "Ejecutar black (check)" "black app/ --check"
    }
    "11" {
        Run-Command "Ejecutar black (format)" "black app/"
    }
    "12" {
        Run-Command "Ejecutar isort (check)" "isort app/ --check-only"
    }
    "13" {
        Run-Command "Ejecutar isort (format)" "isort app/"
    }
    "14" {
        Run-Command "Ejecutar pip-audit (seguridad)" "pip-audit"
    }
    "15" {
        Run-Command "Ejecutar bandit (seguridad)" "bandit -r app/"
    }
    "16" {
        Write-Host "=== PRE-COMMIT COMPLETO ===" -ForegroundColor Cyan
        Write-Host "Ejecutando todas las verificaciones..." -ForegroundColor Yellow
        Write-Host ""
        
        Run-Command "1/8 Tests" "pytest tests/ -v"
        Run-Command "2/8 Cobertura >= 80%" "pytest tests/ --cov=app --cov-fail-under=80"
        Run-Command "3/8 Pylint >= 8.0" "pylint app/ --fail-under=8.0"
        Run-Command "4/8 Flake8" "flake8 app/ --max-line-length=100"
        Run-Command "5/8 Black check" "black app/ --check"
        Run-Command "6/8 Isort check" "isort app/ --check-only"
        Run-Command "7/8 Pip-audit" "pip-audit"
        Run-Command "8/8 Bandit" "bandit -r app/"
        
        Write-Host "=== PRE-COMMIT COMPLETADO ===" -ForegroundColor Green
    }
    "17" {
        Run-Command "Instalar dependencias de desarrollo" "pip install -r requirements-dev.txt"
    }
    "18" {
        Write-Host "Iniciando servidor FastAPI..." -ForegroundColor Yellow
        Write-Host "Servidor disponible en: http://localhost:8000" -ForegroundColor Green
        Write-Host "Documentación Swagger: http://localhost:8000/docs" -ForegroundColor Green
        Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Gray
        Write-Host ""
        uvicorn app.presentation.api.v1.main:app --reload
    }
    "0" {
        Write-Host "Saliendo..." -ForegroundColor Gray
    }
    default {
        Write-Host "Opción no válida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Script finalizado" -ForegroundColor Cyan

