@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo   PREPARANDO SUBIDA A GITHUB - Antigravity Alfa v5.1
echo ========================================================
echo.

echo 1. Limpiando y preparando archivos...
git add .

echo 2. Creando punto de guardado (v5.1 Premium)...
git commit -m "🚀 Antigravity Alfa v5.1 - Sincronizacion Automatica Cloud"

echo 3. Enviando a la Nube (GitHub -> Render)...
git branch -M main
git push -u origin main --force

echo.
echo ========================================================
echo   ¡TODO LISTO! Tus cambios ya estan en la Nube. ☁️
echo   Render se activara automaticamente en unos minutos.
echo ========================================================
echo.
pause
