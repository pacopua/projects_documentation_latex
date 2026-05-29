# Toma de requerimientos
## Transcripción
He hecho pruebas básica, y solucionado ciertos problemas que estabamos teniendo con el módulo de transcripción. Resulta que se enviaba un parametro (sv=2026...) que no funciona por culpa de azure, ha habido que hacer un fallback a (sv=2020...), y ya parece que funciona.

Falta revisar en mayor profundidad el flujo y hacer diagramas de la base de datos para la memoria.
## Estudio de frameworks y planificación
- Se ha de explicar como funciona Tavily por encima (BM25)+Filtrar Por Calidad+Scraping de las web+Embedding+CosineSimilarity, si se puede meter un diagrama, **mejor**.

Revisar el flujo. Y de nuevo añadir un diagrama de como funciona el codigo y de como accede a los datos de blob storage.

# Agente de programación

Añadir el ciclo de funcionamiento de opencode y claude code, distinguir mejor entre las dos.

0. Revisar colbPowers y asegurarme de que no le falte nada.
1. Meterle un hook a opencode para que pueda usar code-review-graph adecuadamente
2. Hacer las pruebas de las combinaciones con gpt-4o, hacer 3x de cada una de las formas. Seguramente haya que comprar una subscripción de OpenAI
3. Intentar ver si consigo hacer que funcione un modelo local que llame herramientas, para mostrar ejemplos con dos modelos diferentes, y mostrar que en efecto, se puede usar modelos locales!
4. Si se consigue que funcione el modelo local, volver a hacer las pruebas pero con el modelo local.

# Seguimiento de reuniones

Módulo de seguimiento programado, falta incorporar la capacidad de que el agente pueda hacer tablas, pero como no tengon configurado el .env, no puedo hacer este trabajo aún. [DONE]

Después de esto hay que hacer pruebas. [ALMOST DONE]

# Memoria
- Lo de GEP se puede reescribir sin problema, presentarlo como considere, recomendado basarme en otros TFGs. Lo MAS importante del trabajo de verdad que es la memoria. Tienen que entenderse el contexto del problema, lo que se intenta cubrir, lo que no se intenta cubrir, etc. Esto es MAS importante que la implementación como tal incluso, ya que es la primera impresión que se lleva el corrector.

- Apartado de conclusiones.

- Apartado de posibles mejoras.

- Hacer una GRAN revisión para quitar/reescribir apartados. Leerselo todo entero es recomendable.