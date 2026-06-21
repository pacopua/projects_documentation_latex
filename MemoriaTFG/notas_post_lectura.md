Lectura entera TFG con apuntes:
# Review post lectura mia
---

- 1.1.2: párrafo final contradice lo que se termina aplicando, se podría borrar tal cual[DONE]
- 1.2.3: Agent Skill definición se podría mejorar. Ahora se dice que es cómo una herramienta o script que el agente puede usar, pero en realidad es un prompt que puede incluir scripts en subcarpetas que SÍ puede ejecutar, pero primero debe leer el prompt al activar la Skill.[DONE]
- 1.2.4: Se introduce el apartado de transcripción por la cara cuando no se ha mencionado previamente in ningún momento.[DONE]

- 1.4:
	+ En general quizás se podrían expandir estos apartados[DONE]
	+ Se deberian añadir citaciones tanto en 1.4.5 como en 1.4.7.[DONE]

---

2: Cambiada introducción[DONE]
2.1: Se siguen planteando La toma de requerimientos y el módulo de seguimiento del cliente como apartados diferentes. Además[DONE]

---

3: Este apartado prácticamente NO ha cambiado[DONE]
3.3: Preguntarle a David por este apartado.[DONE]

---

4.1.3: Revisar estos sprints, cambiarle la definición a alguno de ellos pero sin tener que actualizar el diagrama de GANTT. Quzias se podría añadir mas peso a el tiempo que tomó hacer los experimentos y evaluarlos estadisticamente? 20 horas aproximadamente. [DONE]

4.4.4: Apartado identificado como crítico, le tengo que preguntar a David si esto se lo van a mirar.[DONE]

---

6.2.2 El flujo de funcionamiento de los agentes no se ve del todo claro, puesto que tenemos los pasos como \paragraph, y luego tenemos el apartado de "Similitud con ClaudeCode." también como paragraph, cuesta distinguir que es una sección y no un paso mas de el flujo de opencode.[DONE]

6.3.1 code-review-graph, explicación demasiado breve, falta poner ejemplos de reducción de tokens. En el GitHub hay un par.[DONE]
	- También hay que explicar que se tuvieron que implementar plugins personalizados con Opencode para implementar esta herramienta [DONE]

---

Se explica bien la metodología estadistica que se ha seguido?? [DONE]

---

9. 
	+ Añadir en las conclusiones si se han cubierto los requisitos funcionales y no funcionales definidos anteriormente. [Done]
	+ Repasar conclusiones de resultados estadísticos. [PENDING]

---

Anexo, eliminar mención de "Explicación completa", cuando realmente no es una explicación completa [DONE]

# Review de David

- Hedges' g en vez de cohens. Decirme en que me he basa [DONE]
- Cambiar cosasa que están a futuro sobretodo para los apartados 1-4 de la memoria. [DONE]
- Cambiar lo de el "Uso de IA", que quede claro que la IA es una herramienta. [DONE]
- Glosario de siglas. [DONE]
- Keywords después del abstract. [DONE]
- Intentar vigilar con las afirmaciones, poner referencias. [DONE] solo code-review-graph pendiente
- El p-value mide si hay o no efecto, mientras que cohen y hedges miden la magnitud del efecto. Cambiar las tablas para que se vea reflejado. [DONE]
- Cambiar nombre de la lsita de tablas -> "Lista de tablas" [DONE]
- Cambiar los diagramas con los módulos! Ahora mismo hay un diagrama con lógica que no corresponde a su módulo. [DONE]
- Cambiar 6.3.3, explicar que colbPowers se ha desarrollado para este proyecto, entre otras cosas [DONE]
- Mover el apartado de integración del conocimiento a otro lado. [Done]

- Cambiar readme.md de colbPowers para que ponga colbPowers y no superpowers. [DONE]
- Apartado 1.6 (Propuesta). Explicar qué se hace exactamente, que no hago codigo desde 0, sino que junto un montón de cosas ya implementadas en un solo sistema. [DONE]
13/13

# Cambios para que David pueda hacer una envaluación rápida.

  ---
  Estructura y formato

  1. Keywords añadidas en los tres abstracts (EN/ES/CA): SDD, LLM, agentes de código, HITL, etc.
  2. Nueva lista de siglas/acrónimos (API, CC, CLI, DCM, HITL, IDE, LLM, MCP, SDD, WSL…) añadida tras el índice de tablas.
  3. "Integración de conocimientos" reubicada dentro del bloque de Alcance, eliminando su posición como sección independiente al final.
  4. Sección privada de notas del autor eliminada ("Cosas en proceso y dudas").
  5. "Similitud con ClaudeCode" promovida de \paragraph a \subsubsection.
  6. Etiquetas \label duplicadas corregidas (tres figuras compartían fig:skill_definition).
  7. Verbos pasados de futuro a presente en toda la memoria.

  ---
  Contenido técnico

  8. Definición de Agent Skills reescrita: de "herramientas/scripts invocables" a "documentos de instrucciones procedimentales en Markdown que el agente consulta bajo demanda".
  9. Motivo de descarte de Spec Kit / AgentOS más concreto: incompatibilidad con el flujo de Colb.AI, no solo "fricción excesiva".
  10. Nuevo párrafo explicitando que el TFG gira en torno a la integración de herramientas existentes, no a construir desde cero.
  11. Benchmarks de code-review-graph actualizados: de una prueba puntual (-37,5%) a los benchmarks oficiales (38× a 528×, mediana ~82×), con nueva figura del grafo sobre un repo de
  Colb.AI.
  12. Nuevo párrafo sobre adaptadores JavaScript para OpenCode en la sección de code-review-graph.
  13. colbPowers descrito con más precisión: incluye creación de skills nuevas (defining-constitution, defining-features) además de la fuente de verdad compartida.

  ---
  Metodología estadística (cambio mayor)

  14. d de Cohen → g de Hedges en todo el bloque experimental, con justificación (corrige sesgo en muestras pequeñas).
  15. Aclaración metodológica añadida: el p-value determina existencia de efecto; la g solo cuantifica magnitud cuando p < 0,05.
  16. p-values y valores de g incluidos directamente en los párrafos de análisis (antes solo porcentajes).
  17. Factor de sobrecoste corregido: de 2,9×–4,5× a 2,2×–4,5× (en conclusiones y sección de sostenibilidad).

  ---
  Bibliografía (14 entradas nuevas)

  Hedges (1981), Cohen (1988), Welch (1947), JetBrains DevEco 2025, Vaithilingam et al. (CHI 2022), Standish CHAOS Report (1994), Cunningham (1992, deuda técnica), LangChain, Tree-sitter,
  Anthropic MCP (2024), estudio de burnout en SW (2023), Azure Speech Service, Otter.ai y Fireflies.ai.

  ---
  En total: cambios de estructura (7), de contenido técnico (6), de metodología estadística (4), y 14 referencias nuevas.

# Segunda lectura
- Citar a Claue Cowork en 1.4.5 Herramientas de documentación de reuniones
- Explicar qué es Claude Cowork en algún lado?