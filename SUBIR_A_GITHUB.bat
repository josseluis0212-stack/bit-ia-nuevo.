@echo off
echo PREPARANDO SUBIDA A GITHUB - Antigravity Alfa v5.0
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. Inicializando repositorio local...
git init
echo 2. Añadiendo archivos...
git add .
echo 3. Creando commit Alfa v5.0...
git commit -m "Antigravity Alfa v5.0 - Estrategia Avanzada"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo SIGUIENTE PASO:
echo 1. Asegúrate de tener tu repositorio en GitHub.
echo 2. Ejecuta estos comandos para sincronizar con la nube (Render):
echo    git branch -M main
echo    git push -u origin main
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Una vez subido, Render se activará automáticamente.
pause
