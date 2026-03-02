# Arquitectura Antigravity Alfa v5.0 🧠

El bot ha evolucionado hacia un sistema de **Confluencia Técnica Avanzada** y **Gestión de Riesgo Dinámica**, diseñado para maximizar la precisión en Bybit Testnet.

## Pilares de Inteligencia (Motor Alfa)

La IA calcula un **Score de Probabilidad (0-100%)** basado en 4 pilares técnicos:

### 1. Tendencia Institucional (30%)
Utiliza la **EMA 200** en el timeframe de 4H para asegurar que el bot nunca opere contra la tendencia de largo plazo. Solo se permiten Longs si el precio está arriba de la media y el Histograma MACD es positivo.

### 2. Momento y Fuerza (30%)
Analiza la confluencia entre el **MACD** (Cruce de líneas) y el **RSI**. El RSI actúa como filtro de seguridad para evitar entrar en zonas de sobreventa o sobrecompra extrema donde el riesgo de reversión es alto.

### 3. Volatilidad Dinámica (20%)
Implementa **Bandas de Bollinger**. El bot identifica si el mercado está en una fase de expansión o compresión lateral. Si el ancho de bandas es muy bajo (mercado muerto), la señal se descarta automáticamente.

### 4. Flujo de Volumen (20%)
Valida la señal mediante el **Volumen Relativo**. Una entrada solo es válida si el volumen de la vela actual es significativamente superior al promedio de las últimas 20 velas, confirmando interés institucional.

## Gestión de Riesgo Dinámica (ATR)
A diferencia de versiones anteriores con SL/TP fijos, la v5.0 utiliza el **ATR (Average True Range)**. 
- **Stop Loss:** Se coloca a 1.5x ATR, adaptándose a la volatilidad real del par.
- **Take Profit:** Se coloca a 2.5x ATR, buscando un ratio de beneficio superior a 1.5.

## Autonomía 24/7
El bot escanea dinámicamente **TODOS** los pares de futuros perpetuos disponibles en Bybit, gestionando hasta 10 posiciones simultáneas con un margen estricto de $100 USDT a 5x de apalancamiento.
