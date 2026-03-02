# Antigravity Alfa v5.0 - Professional Futures Bot

Este bot ha sido transformado en un motor de trading autónomo de alta fidelidad, utilizando confluencia técnica institucional y gestión de riesgo dinámica.

## Parámetros de Operación Alfa v5.0

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Modo** | ANTIGRAVITY v5.0 | Totalmente autónomo e independiente |
| **Apalancamiento** | 5x (Fijo) | Configuración de riesgo balanceada |
| **Monto por Operación** | $100.00 USDT | Margen por posición (Demo) |
| **Stop Loss** | Dinámico (ATR) | Basado en volatilidad real |
| **Take Profit** | Dinámico (ATR) | Ratio optimizado > 1.5 |
| **Indicadores** | MACD / RSI / BB / EMA 200 | Motor de confluencia triple |
| **Rastreo Cierres** | Tiempo Real | Notificaciones inmediatas en español |
| **Escaneo de Pares** | TOTAL | Escanea todos los perpetuos USDT |

## Estructura del Proyecto

- `core/`: Clientes de API, Telegram, Estadísticas y Riesgo.
- `strategy/`: Motores de análisis Antigravity Alfa.
- `data/`: Historial de operaciones (JSON).
- `reports/`: Gráficos de desempeño (PNG).

## Despliegue 🚀

1. Configura tu `.env` con las claves de Bybit Testnet.
2. Asegura que `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` están presentes.
3. Ejecución local: `python main.py`.
4. El bot operará 24/7 de forma autónoma, buscando solo señales de alta probabilidad (>85%).

---
*Antigravity Alfa v5.0 - Inteligencia aplicada al mercado de futuros.*
