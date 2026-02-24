# Arquitectura de la IA - bit-ia-nuevo v3.2 🧠

La "IA Interna" de este bot no es una simple caja negra; es un motor de **Inferencia Probabilística Basado en Heurísticas** diseñado para maximizar la probabilidad de éxito en el mercado de futuros de Bybit.

## ¿Cómo fue creada?

La IA se basa en 4 pilares de análisis técnico e institucional, ponderados para generar un **Score de Confianza (0-100%)**.

### 1. Sistema de Confluencia Tendencial (30%)
Analiza los timeframes de 4H, 1H y 5m simultáneamente. Si el precio está por encima de la EMA 50 en todas las temporalidades y ocurre un cruce de EMA 8/20, se asigna el puntaje máximo en esta categoría. Esto asegura que nunca operemos en contra de la "mano fuerte".

### 2. Filtro de Volumen Predictivo (30%)
Utiliza una desviación estándar sobre el volumen promedio de las últimas 20 velas. La IA busca "picos de absorción" o "picos de ruptura". Si el volumen de la señal es significativamente mayor al promedio pero sin ser una "vela de agotamiento", la IA valida la fuerza del movimiento.

### 3. Cálculo de Distancia y Probabilidad (20%)
La IA mide la distancia entre el precio actual y el Take Profit (2%) versus la distancia al EMA 50. Si el precio está demasiado extendido (lejos de la media), la IA descarta la señal por riesgo de "reversión a la media", incluso si el indicador dice comprar.

### 4. Estabilidad de Volatilidad (20%)
Usando el ATR (Average True Range), la IA calcula si el rango de movimiento actual permite alcanzar el 2% de ganancia en un tiempo razonable. Si la volatilidad es demasiado baja, el mercado está "muerto" y la señal se descarta para evitar quedar atrapado en lateralizaciones.

## El "Portero" (Decision Gate)
Antes de enviar una señal a Bybit o Telegram:
1. La IA suma los puntos de los 4 pilares.
2. Si el **Score Final > 80%**, la operación se aprueba.
3. Si el **Score Final < 80%**, el bot registra la señal en logs pero **la descarta**, protegiendo tu capital de señales mediocres.

## Mejora Continua (Self-Learning)
Cada vez que una operación se cierra (ganada o perdida), la IA guarda las condiciones de ese mercado. Si detecta que ciertas condiciones (ej. RSI muy alto) causan pérdidas constantes, ajustará automáticamente los pesos de los pilares para ser más selectiva.
