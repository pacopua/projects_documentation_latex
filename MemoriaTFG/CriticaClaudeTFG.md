Voy a leer el documento completo antes de emitir el veredicto.

Ya lo he leído. Aquí va la evaluación sin filtros.

---

## EVALUACIÓN CRÍTICA — TFG: Sistema Inteligente de Asistencia al Desarrollo Estructurado

**Nota previa: este documento NO está listo para defensa.** Lo que sigue es una lista de problemas ordenados por gravedad.

---

### GRAVEDAD MÁXIMA: Errores que invalidan la presentación

**1. El Capítulo 10 existe.**
Hay un capítulo titulado "Cosas en proceso y dudas" en la memoria final. Incluye frases como "Aún queda escribir este apartado" y "me he de leer de nuevo toda la sección". Esto es absolutamente impresentable. Un tribunal que abra el PDF y encuentre esto puede rechazar la defensa en el acto. Si se entrega esto al tribunal, la nota techo es un aprobado por educación.

**2. La Sección 9.1 "Conclusiones generales" está vacía.**
El apartado más importante de toda la memoria —el lugar donde el autor demuestra que entiende qué ha hecho y qué significa— tiene solo un título. Sin conclusiones generales, no hay tesis. Solo hay documentación de proyecto.

**3. La métrica "Test Coverage" se declara en la Sección 2.3 y desaparece.**
En los requisitos se lista explícitamente "Cobertura de Pruebas (Test Coverage) [37]" como métrica de evaluación. En el Capítulo 7 no aparece ni una sola vez. Esto es un incumplimiento directo de los objetivos declarados, no un matiz menor. [DONE: eliminada mención de "Test Coverage" en sección 2.3]

---

### GRAVEDAD ALTA: Problemas metodológicos que debilitan las conclusiones centrales

**4. N=3 por condición es estadísticamente indefendible.**
Se aplica el test t de Welch con n=3. Con ese tamaño muestral no se puede verificar la normalidad, los outliers tienen un peso devastador, y los intervalos de confianza son tan anchos que los resultados son poco más que anecdóticos. El propio autor lo reconoce ("los resultados deben interpretarse con cautela"), pero luego los presenta como conclusiones del abstract. Si los resultados son solo sugerentes, el abstract no puede decir "suggests improvements in code quality." El autor mismo admite en el Capítulo 9 que necesitaría n≥5 para rigor estadístico —eso implica que los experimentos actuales no tienen rigor estadístico.

**5. La condición "baseline" y "colbPowers" no son comparables.**
La condición colbPowers incluye el servidor MCP `code-review-graph`. La condición baseline no. Por tanto, la mejora medida puede deberse al grafo de dependencias, no al flujo SDD. El propio trabajo futuro (Sección 9.2.1) propone comparar "colbPowers con y sin code-review-graph para aislar el efecto del servidor MCP de forma independiente". Esto implica que el experimento actual **no puede** atribuir causalmente los resultados a colbPowers. Es una variable confusora no controlada. [Solucionado, MCP es parte del sistema de colbPowers, por lo que es correcta la comparación]

**6. El propio sistema no cumple su garantía central.**
La Sección 9.2.1 admite: "en los experimentos se observaron casos en los que el orquestador omitió la llamada al subagente revisor tras implementar código." La propuesta principal del TFG es que el flujo SDD garantiza especificación antes del código y revisión después. Si el orquestador omite la revisión, la garantía es una ficción. El trabajo futuro propone hooks para hacerlo determinista —lo que equivale a admitir que la implementación entregada no funciona como se describe. [El proyecto de final de grado no debe conseguir todo lo que se propone, es un trabajo con tiempo limitado y se da por hecho que van a haber limitaciones y cosas que no salgan perfectas, por lo que con que se comente lo sucedido, ya está bien]

**7. La anonimización del proyecto real está rota.**
La Sección 7.2 afirma que se han "omitido ciertos detalles para anonimizarlo". Las Figuras 10, 11, 12, 22, 23 y 24 etiquetan el proyecto como **"ConfortMental"** en todos los ejes. La anonimización dura exactamente un párrafo. [Solucionado, he cambiado la aparición de ese nombre en las tablas por "Repo existente"]

**8. La hipótesis del Caso 1 nunca se verifica.**
La hipótesis declarada es que colbPowers "debería sufrir menos de este problema [olvidar cambios]". Los datos recogidos son tokens consumidos y tool calls. En ningún momento se mide cuántos de los cambios solicitados se implementaron correctamente. Se mide el overhead del proceso, no la calidad del resultado. La hipótesis central del caso queda sin demostrar. [Ninguno de los experimentos han olvidado los cambios pedidos y los han aplicado bien]

---

### GRAVEDAD MEDIA: Inconsistencias internas y errores de contenido

**9. Contradicción ambiental flagrante.**
La Sección 4.4.4 afirma que el sistema "permite ir al grano" reduciendo llamadas a LLMs y disminuyendo el consumo energético. Los datos experimentales del Capítulo 7 muestran que colbPowers consume entre **2,9x y 4,5x más tokens** que el baseline. La dimensión ambiental afirma exactamente lo contrario de lo que los propios resultados demuestran.

**10. El modelo "DeepSeek V4-Flash" no existe (o no está documentado).**
Las Tablas 12 y 14 usan "DeepSeek V4-Flash". No existe ningún modelo con ese nombre en la documentación pública de DeepSeek. DeepSeek tiene V2, V2.5, V3, R1 y variantes, pero ningún "V4-Flash". Si el autor inventó el nombre, es un error grave. Si es un nombre real de un modelo de 2026, necesita una referencia.

**11. La descripción de MP3 en la Sección 8.2 es técnicamente incorrecta.**
El autor afirma que el audio "se convierte a MP3 para que utilice Huffman Encoding para reducir aún más el tamaño." MP3 usa MDCT (Modified Discrete Cosine Transform) y modelado psicoac ústico como mecanismos primarios de compresión. Huffman se usa solo en la etapa de codificación entrópica final. Presentar MP3 como "Huffman Encoding" en una tesis de Ingeniería Informática, además en la sección de integración de conocimientos de la asignatura de compresión, es un error conceptual importante.

**12. El "estado del arte" no cumple los mínimos académicos.**
Las descripciones de Spec Kit (Sección 1.4.1) y AgentOS (Sección 1.4.2) son tautológicas: "Spec Kit es una herramienta diseñada para facilitar el desarrollo basado en especificaciones." No hay análisis técnico, no se mencionan LangGraph, CrewAI ni AutoGen —frameworks multi-agente establecidos y directamente comparables. La tabla comparativa (Cuadro 1) se basa en valoraciones propias sin justificación empírica.

**13. La referencia [15] contradice el argumento que soporta.**
El autor usa la "Ley del Mínimo Esfuerzo" para explicar por qué los desarrolladores evitan la documentación. La referencia [15] citada es "The Effort Paradox: Effort is both costly and valued" (Inzlicht et al., 2018), cuyo argumento central es que los humanos también **valoran** el esfuerzo. Citar este paper como soporte de "los humanos evitan el esfuerzo" es una lectura selectiva que invierte el argumento del propio trabajo citado.

**14. La "innovación" de colbPowers se reduce a dos ficheros Markdown.**
El núcleo técnico diferencial respecto a superpowers es añadir `constitution.md` y `features.md`. Son dos ficheros de texto plano. El resto de la arquitectura (orquestador, subagentes, skills, hooks) se hereda directamente de superpowers. Para un TFG de Ingeniería Informática, esto es una contribución técnica extremadamente delgada que necesita justificarse mucho más robustamente.

**15. Conflicto de interés no gestionado.**
El director del proyecto pertenece a Colb.AI. El TFG desarrolla colbPowers para Colb.AI. El experimento evalúa colbPowers sobre proyectos de Colb.AI. El propio autor ejecuta los experimentos y los valora. No hay evaluación ciega, no hay evaluador externo, no hay réplica independiente. Este conflicto de interés estructural no se menciona en ningún momento.

---

### GRAVEDAD BAJA: Problemas formales y de redacción

**16. Errores tipográficos en la Sección 3.3:** "uitilizado" (→ utilizado), "reestrucurar" (→ reestructurar), "secciones algunas secciones" (redundancia).

**17. La Figura 4** muestra una captura de pantalla de la interfaz de Claude Cowork (producto de Anthropic) y la etiqueta dice "Generación propia." No es generación propia.

**18. Los salarios del presupuesto se extraen de Indeed (referencia [14])**, una web de crowdsourcing laboral, como si fuera una fuente académica. No lo es.

**19. Radon solo analiza Python**, pero el Caso 1 es Flutter/Dart. La ausencia de métricas de calidad en el Caso 1 se presenta como una decisión metodológica, cuando en realidad es una limitación de haber elegido una herramienta incompatible con el lenguaje del proyecto real.

**20. El Capítulo 8 (Integración de conocimientos)** — el propio autor duda de si debería eliminarse (ítem 2 del Capítulo 10). Incluir en la memoria un capítulo que el autor considera que "no aporta absolutamente nada" refleja falta de criterio editorial.

---

### RESUMEN EJECUTIVO

Este TFG tiene trabajo real detrás. La arquitectura de colbPowers está pensada, el pipeline de transcripción está implementado, y el diseño experimental tiene intención. Pero tal como está, hay **dos secciones obligatorias incompletas o vacías**, los **experimentos no pueden soportar las conclusiones que se extraen**, y existe al menos **un error técnico grave** (descripción de MP3). Antes de la defensa, como mínimo se debe: escribir las conclusiones, eliminar el Capítulo 10, añadir la métrica de Test Coverage o justificar explícitamente su ausencia, y corregir la contradicción ambiental. Sin eso, el tribunal tiene material más que suficiente para hacer una defensa muy incómoda.