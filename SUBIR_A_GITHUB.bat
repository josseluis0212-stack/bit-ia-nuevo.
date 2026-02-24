@echo off
echo PREPARANDO SUBIDA A GITHUB - bit-ia-nuevo v3.0
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. Inicializando repositorio local...
git init
echo 2. Añadiendo archivos...
git add .
echo 3. Creando primer commit...
git commit -m "v3.0 - Profesional Futures Bot Build"
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo SIGUIENTE PASO:
echo 1. Crea un repositorio VACÍO en GitHub.
echo 2. Copia la URL del repositorio (https://github.com/tu-usuario/nombre-repo.git).
echo 3. Ejecuta estos comandos en esta terminal:
echo    git remote add origin TU_URL_DE_GITHUB
echo    git branch -M main
echo    git push -u origin main
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pause
