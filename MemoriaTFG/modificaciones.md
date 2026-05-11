# Modificaciones realizadas respecto a la versión inicial

## Bloque 1 — Contexto y Alcance

**1. Nueva subsección "Definición del Problema" (tras la Introducción)**
- Explica el problema central: ausencia de un flujo estructurado para el uso de IA en desarrollo
- Tres consecuencias del paradigma *Code-Driven*: generación de *slop code*, falta de trazabilidad, y barrera de incorporación para nuevos desarrolladores
- Frase conclusiva en negrita que resume el problema que resuelve el TFG

**2. Sub-objetivos reformulados como resultados (sección 3.2)**
- Los 4 sub-objetivos pasaron de describir *acciones a realizar* a expresar *resultados a conseguir*, con verbos de impacto (*Conseguir, Lograr, Obtener, Garantizar*) y el beneficio concreto de cada uno

**3. Sección "Obstáculos y Riesgos" ampliada (sección 3.3)**
- Los 3 riesgos originales (1 frase cada uno) se expandieron con causa, impacto y mitigación
- El riesgo del IDE fue reescrito para reflejar el trade-off real: control IDE nativo vs. LangChain + APIs directas
- Añadido un **4º riesgo nuevo**: dependencia de la calidad de las especificaciones
- Añadido párrafo introductorio con referencia cruzada a la Sección 6

---

## Bloque 2 — Planificación Temporal

**4. Tabla de desglose de horas por rol (tras la tabla resumen de tareas)**
- Nueva tabla que distribuye las ~537h entre los 4 roles: Jefe de Proyecto (~77h), Investigador/Documentador (~190h), Programador Junior (~210h), Tester (~60h)

**5. Campo "Tareas afectadas" en cada riesgo (Sección 6)**
- Riesgo 1 → DA1–DA4, GP5, PV
- Riesgo 2 → DA3, DA4, DA1
- Riesgo 3 → DA1, DA2, PV2

**6. Riesgos 4, 5 y 6 añadidos a la Sección 6**
- **Riesgo 4**: Limitaciones de control IDE (Plan B: prompts breves + orquestación manual humana)
- **Riesgo 5**: Ventana de contexto (Plan B: resúmenes de conversación + aislamiento de agentes por feature)
- **Riesgo 6**: Fricción por auditorías (Plan B: niveles de severidad en el Reviewer)
- Cada uno con: probabilidad, tareas afectadas, plan B, afectación temporal y recursos

**7. Referencias cruzadas entre secciones**
- Sección 3.3 añade referencia a la Sección 6 para el detalle completo de riesgos
- Sección 6 añade referencia al apartado 7.4 para los costes de imprevistos

---

## Bloque 3 — Gestión Económica

**8. Control de Gestión ampliado (sección 7.3)**
- Cada uno de los 4 indicadores ahora incluye un bloque **"Criterio de actuación"** con umbrales concretos y acciones escalonadas:
  - Desviación de horas: 3 niveles (0–10% / 10–20% / >20%)
  - Desviación de coste personal: 3 niveles (<300€ / 300–800€ / >800€)
  - Desviación de costes genéricos: 2 niveles (<30€/mes / ≥30€/mes sostenido)
  - Fondo de imprevistos: 3 niveles (>50% / 0–50% / negativo)

**9. Riesgos R4, R5, R6 cuantificados en Imprevistos (sección 7.4)**
- R4 (Limitaciones IDE): 178,85€ | Probabilidad: 50%
- R5 (Ventana de contexto): 134,28€ | Probabilidad: 60%
- R6 (Fricción en el bucle): 74,60€ | Probabilidad: 50%
- Total imprevistos actualizado: 367,32€ → **755,05€**
- Presupuesto total actualizado: 13.879,93€ → **14.267,66€** (tabla de coste total y dimensión económica de sostenibilidad)

---

## Bloque 4 — Mejoras transversales

**10. `\newpage` antes de "Descripción de las tareas"**
- La sección ahora empieza en página nueva como el resto de secciones principales

**11. `\newpage` antes de "Gestión de riesgos"**
- Evita que la sección empiece pegada al diagrama de Gantt

**12. Etiqueta del Gantt corregida**
- `\label{fig:heatmap}` → `\label{fig:gantt}`
