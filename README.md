# bit-ia-nuevo v3.0 - Professional Futures Bot

Este bot ha sido reconstruido desde cero siguiendo los 7 requisitos profesionales para operar en Bybit Futuros.

## Parámetros de Configuración Final

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Modo** | AUTÓNOMO v3.1 | Aprendizaje y ajuste dinámico |
| **Apalancamiento** | 5x | Fijo para todas las posiciones |
| **Monto por Operación** | $50.00 USDT | Margen inicial fijo |
| **Stop Loss** | 1% (Exacto) | Fijo e inamovible |
| **Take Profit** | 2% (Exacto) | Fijo e inamovible |
| **Indicadores** | EMA 8 / 20 / 50 | Filtro tendencial y gatillo |
| **Rastreo Cierres** | En tiempo real | Reporte de PnL USDT inmediato |
| **Aprendizaje IA** | Dinámico | Ajusta filtros según racha de pérdidas |

## Estructura del Proyecto

- `core/`: Clientes de API, Telegram, Estadísticas y Riesgo.
- `strategy/`: Motores de análisis, indicadores y filtros.
- `data/`: Historial de operaciones (JSON).
- `reports/`: Gráficos de desempeño (PNG).

## Despliegue en Render

## Guía de Despliegue 🚀

Sigue estos pasos para poner tu bot en vivo:

### Paso 1: Subir a GitHub
1. Crea un repositorio en GitHub llamado `bit-ia-nuevo`.
2. En tu terminal local (en la carpeta del bot), ejecuta:
   ```bash
   git remote add origin <URL_DE_TU_REPO_GIT>
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Configurar en Render
1. Ve a [Render Dashboard](https://dashboard.render.com/).
2. Crea un nuevo **Worker** (o Web Service) y conecta tu repo.
3. Configuración:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### Paso 3: Variables de Entorno (IMPORTANTE)
En la pestaña **Environment** de Render, añade los valores de tu archivo `.env`:
- `BYBIT_API_KEY`
- `BYBIT_API_SECRET`
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

---
*Bot bit-ia-nuevo v3.2 Professional - Operando con Disciplina e Inteligencia.*

🚀 **El bot está diseñado para operar 24/7 de forma autónoma.**
