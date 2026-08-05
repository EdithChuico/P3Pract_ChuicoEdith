=============================================================================
README - Evidencias de Mejoras y Reproducibilidad (Fase 2)
=============================================================================
Estudiante: Edith Liliana Chuico Navarrete
Tema: Evaluación de georeferenciación en un sistema de asistencia biométrica 
      bajo redes Wi-Fi, datos móviles y VPN.
=============================================================================

1. ENLACE AL REPOSITORIO PÚBLICO ACTUALIZADO
-----------------------------------------------------------------------------
El código fuente completo de la arquitectura distribuida, incluyendo las 
actualizaciones del frontend para el control de la caché, se encuentra 
disponible en el siguiente repositorio:
Enlace: https://github.com/EdithChuico/Proyecto_DeteccionFace.git

2. CORRECCIONES PRINCIPALES REALIZADAS (Basadas en la Retroalimentación P1)
-----------------------------------------------------------------------------
Para garantizar la validez del experimento, se implementaron las 
siguientes mejoras metodológicas:
* Redefinición del Constructo: Se evaluó estrictamente el comportamiento de 
  la W3C Geolocation API, evitando conclusiones erróneas sobre el hardware A-GPS.
* Control de Caché: Se instrumentó el parámetro `maximumAge=0` vs. posiciones 
  cacheadas para medir su impacto en las Falsas Aceptaciones.
* Entorno Multi-plataforma: Se superó la limitación del dispositivo único 
  incorporando pruebas en un dispositivo nativo Android (POCO X6 Pro) junto 
  con el entorno de escritorio (Windows).
* Ground Truth y Aleatorización: Se establecieron distancias progresivas de 
  verdad terreno (2m, 9m, 11m, y 20m) respecto al geofence de 10m, ejecutando 
  320 pruebas bajo un protocolo de orden aleatorio.
* Desglose de Latencias y Estadística: Los tiempos se desglosaron en adquisición 
  geográfica, RTT de red y procesamiento del backend. Las variaciones se 
  respaldaron estadísticamente mediante un ANOVA factorial (p < 0.05).

3. ESTRUCTURA Y CONTENIDO DE ESTE ARCHIVO ZIP (Evidencias)
-----------------------------------------------------------------------------
Este archivo comprimido contiene los datos y recursos que respaldan los 
resultados documentados en el artículo. La estructura es la siguiente:

/datos
    - resultados-geocerca-fase2.csv : Dataset principal con los registros 
      brutos de las 320 pruebas de campo. Incluye variables de entorno (Wi-Fi, 
      Datos, VPN), política de caché, distancias ground-truth, métricas de 
      latencia desglosada y el resultado de validación del backend.
    - resultados-geocerca-fase1.csv : Dataset generado en la primera entrega, para
      evidenciar el cambio realizado en base a las sugerencias del docente.

/scripts
    - generar_curva.py : Script en Python (utilizando matplotlib y numpy) 
      que lee dinámicamente el archivo CSV, calcula matemáticamente las tasas 
      de FAR y FRR por cada distancia, y dibuja la curva de error progresivo 
      sin utilizar tasas escritas manualmente.
    - anova.py : Script estadístico para replicar el ANOVA 
      factorial sobre las latencias de RTT y adquisición geográfica.

/graficos
    - error_curve.png : Gráfico resultante del análisis de distancia vs error.
    - EjecuciónANOVA_FARyFRR.jpg : Gráficos de barras utilizados en el artículo.


4. INSTRUCCIONES DE REPRODUCIBILIDAD
-----------------------------------------------------------------------------
* Análisis de Datos: El archivo .csv en la carpeta `/datos` contiene los 
  registros exactos.
* Generación de Gráficos: Para comprobar la curva de error, ejecute el script 
  `generar_curva.py` ubicado en la carpeta `/scripts`. El script leerá el CSV, 
  calculará los falsos positivos/negativos por distancia y generará la imagen 
  exacta incluida en el manuscrito.