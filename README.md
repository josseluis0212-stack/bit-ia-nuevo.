# bit-ia-nuevo v3.0 - Professional Futures Bot

Este bot ha sido reconstruido desde cero siguiendo los 7 requisitos profesionales para operar en Bybit Futuros.

## Parámetros de Configuración Final

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Mercado** | Bybit USDT-Perpetual | Futuros lineales |
| **Apalancamiento** | 5x | Fijo para todas las posiciones |
| **Monto por Operación** | $50.00 USDT | Margen inicial fijo |
| **Límite de Operaciones** | 10 simultáneas | Máximo 10 monedas distintas |
| **Stop Loss** | 1% | Fijo e inamovible |
| **Take Profit** | 2% | Fijo e inamovible |
| **Timeframes** | 4h / 1h / 5m | Análisis MTF para tendencia y entrada |
| **Indicadores** | EMA 8 / EMA 21 | Cruce de medias y soportes |
| **Filtros** | Volumen, Volatilidad, Macro | Triple validación antes de entrar |
| **IA Interna** | Scoring Probabilidad | Mínimo 75% para ejecutar |

## Estructura del Proyecto

- `core/`: Clientes de API, Telegram, Estadísticas y Riesgo.
- `strategy/`: Motores de análisis, indicadores y filtros.
- `data/`: Historial de operaciones (JSON).
- `reports/`: Gráficos de desempeño (PNG).

## Despliegue en Render

1. Sube este código a tu repositorio de GitHub.
2. Crea un **Web Service** o **Worker** en Render.
3. Configura las variables de entorno (`.env`) en el dashboard de Render.
4. Comando de inicio: `python main.py`.

🚀 **El bot está diseñado para operar 24/7 de forma autónoma.**
