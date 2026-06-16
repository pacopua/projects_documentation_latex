# Diseño: Fusión de "Cambios de Alcance del Proyecto" en Secciones 1-5

**Fecha:** 2026-06-16  
**Documento afectado:** `memoria.tex`  
**Objetivo:** Eliminar la sección "Cambios de Alcance del Proyecto" distribuyendo su contenido en las secciones 1-5 mediante cambios quirúrgicos, produciendo una narrativa cohesiva donde la Sección 2 describe el alcance FINAL del proyecto y la Sección 1 explica cómo se llegó a él.

---

## Principios del enfoque

- **Cambios quirúrgicos** — preservar el texto original GEP donde sigue siendo válido; reemplazar únicamente lo que es inexacto o engañoso
- **Transparencia breve** — mencionar el pivote de alcance en los puntos clave, sin dwellar en el enfoque abandonado
- **Narrativa jerárquica** — SDD/colbPowers como núcleo, toma de requerimientos como entrada, seguimiento del cliente como salida
- **Los agentes sí existen** — colbPowers usa un orquestador que invoca subagentes especializados mediante skills; la diferencia con el plan original es el mecanismo (plugin sobre herramienta existente) y la capa de constitution.md + features.md

---

## Cambio estructural global

Mover `\section{Planificación}` para que sea `\subsection{Planificación}` dentro de `\section{Gestión del Proyecto}`. La jerarquía completa resultante:

```
\section{Gestión del Proyecto}
  \subsection{Planificación}          ← movida desde \section
    \subsubsection{GP}
    \subsubsection{TP}
    \subsubsection{DA}
      \paragraph{DA1}
      \paragraph{DA2}
      \paragraph{DA3}
      \paragraph{DA4}
    \subsubsection{PV}
    \subsubsection{Recursos}
    \subsubsection{Tabla resumen}
    \subsubsection{Diagrama de Gantt}
  \subsection{Gestión de riesgos}
  \subsection{Gestión económica}
  \subsection{Informe de sostenibilidad}
  \subsection{Leyes y regulaciones}
```

---

## Sección 1 — Introducción y contexto

### 1.1 Estado del arte
**Acción:** Ampliar con nuevas entradas. Añadir al final de la subsección:

**Nueva categoría — Asistentes CLI extensibles:**
- ClaudeCode (Anthropic) y OpenCode (open source): asistentes de programación de tipo CLI que operan desde la terminal con acceso nativo al sistema de archivos. Exponen mecanismos de extensibilidad nativos: plugins, hooks de ciclo de vida y el protocolo MCP (Model Context Protocol).

**Nueva entrada — superpowers plugin:**
- Plugin open source para ClaudeCode que implementa el patrón orquestador + subagentes mediante skills. Proporciona una arquitectura base para flujos de trabajo Spec-First, pero sin mecanismo de constitución ni features compartidas entre sesiones o desarrolladores.

**Ampliar entradas existentes:**
- *Herramientas de transcripción:* añadir Azure Speech Service (cloud, con diarización de hablantes, adoptado por estar incluido en la suscripción de Colb.AI)
- *Herramientas de documentación de reuniones:* ampliar con Otter.ai, Fireflies.ai, Microsoft Copilot for Teams — generan resúmenes genéricos no parametrizables con el formato específico de cada empresa, lo que justifica una solución propia

### 1.2 Análisis comparativo
**Acción:** Ampliar la tabla existente con dos filas nuevas y añadir párrafo de conclusión.

**Filas nuevas en la tabla:**

| Herramienta | Enfoque Principal | Inconveniente Principal | Integración en Código Existente |
|---|---|---|---|
| ClaudeCode / OpenCode | CLI extensible | Requiere plugin/configuración para Spec-First | Alta |
| superpowers | Orquestador + subagentes via skills | Sin constitución ni features globales entre sesiones | Alta |

**Párrafo de conclusión a añadir tras la tabla:**
superpowers fue evaluado como candidato directo al problema planteado. Resuelve la orquestación de agentes, pero no garantiza coherencia arquitectónica entre sesiones ni entre desarrolladores distintos, ya que carece de un mecanismo de contexto persistente y compartido. Se decidió adoptarlo como base y extenderlo: el resultado es **colbPowers**, que añade la capa de `constitution.md` (reglas y estándares del proyecto) y `features.md` (registro de funcionalidades) como fuente de verdad compartida para todos los agentes.

### 1.3 Propuesta de implementación
**Acción:** Reescribir completamente.

**Nuevo texto:**
Aprovechando la arquitectura de superpowers, el proyecto propone el desarrollo de **colbPowers**: un plugin para ClaudeCode y OpenCode que extiende el patrón orquestador/subagentes añadiendo una capa de contexto persistente basada en `constitution.md` y `features.md`. Este plugin estructura el ciclo de vida del software en torno a tres pilares complementarios:

1. **Toma de requerimientos** — transformar transcripciones de reuniones en planes de implementación estructurados mediante búsqueda semántica web
2. **Spec-Driven Development** — garantizar que cada implementación esté precedida de una especificación validada, coordinada por un agente orquestador que invoca subagentes especializados (implementador, revisor de código, revisor de compatibilidad con specs/constitución/features)
3. **Seguimiento del cliente** — automatizar la generación de documentación post-reunión con el formato específico de Colb.ai

*"Originalmente se contempló construir este sistema desde cero. Durante la fase de investigación previa (TP1) se descubrió que superpowers ya ofrecía la arquitectura base necesaria, lo que permitió redirigir el esfuerzo hacia la contribución diferencial: la capa de constitución y features, y los tres pilares del ciclo de vida."*

---

## Sección 2 — Alcance del Proyecto

### 2.1 Párrafo de apertura
**Acción:** Reescribir.

**Nuevo texto:**
De acuerdo con las necesidades de Colb.Ai y la filosofía de documentar primero reglas y planes de implementación, este proyecto se centrará en el desarrollo de **colbPowers**: un plugin para los asistentes CLI ClaudeCode y OpenCode que extiende el patrón orquestador/subagentes de superpowers añadiendo una capa de contexto persistente basada en `constitution.md` y `features.md`. Este plugin cubre el ciclo de vida completo de un proyecto software, desde la toma de requerimientos hasta el seguimiento del cliente.

### 2.2 Objetivo General — párrafo principal
**Acción:** Cambio quirúrgico.

Reemplazar: *"diseñar y desarrollar un sistema de asistencia a la programación compuesto por un equipo especializado de agentes de IA"*  
Por: *"desarrollar colbPowers como extensión de superpowers que añade constitution.md y features.md como contexto global compartido, estructurando el flujo de desarrollo mediante un agente orquestador que coordina subagentes especializados"*

### 2.3 Sub-objetivos
**Acción:** Cambios quirúrgicos en las descripciones, manteniendo los títulos.

- **Separación de responsabilidades:** añadir que se materializa mediante skills que invocan subagentes especializados: implementador, revisor de código y revisor de compatibilidad con specs/constitución/features
- **Coherencia arquitectónica:** añadir que se implementa concretamente mediante `constitution.md` y `features.md` como fuente de verdad compartida entre sesiones y desarrolladores
- **Agentes capaces de actuar:** mantener intacto
- **Trazabilidad:** añadir que se garantiza porque todo cambio debe ser coherente con `constitution.md` y `features.md` antes de ser implementado

### 2.4 Requerimientos Funcionales
**Acción:** Mantener los 4 existentes, añadir 2 nuevos.

**Nuevos requerimientos:**
- El sistema debe incluir un módulo de procesamiento de transcripciones capaz de generar planes de implementación estructurados a partir de reuniones con el cliente
- El sistema debe incluir un módulo de generación de documentación de seguimiento post-reunión con el formato específico de Colb.ai

### 2.5 Requerimientos No Funcionales
**Acción:** Un cambio quirúrgico.

Reemplazar: *"Integración Local: acoplarse al entorno de desarrollo integrado (IDE)"*  
Por: *"Integración con asistentes CLI: el plugin debe ser compatible con ClaudeCode y OpenCode, utilizando sus mecanismos nativos de extensibilidad (MCP, hooks, skills)"*

### 2.6 Métricas de Evaluación del Código
**Acción:** Dos cambios quirúrgicos.

1. Reemplazar *"calculadas de forma automatizada por el agente Reviewer"* por *"calculadas mediante **radon**, herramienta Python de análisis estático"*
2. Añadir aclaración: las métricas no forman parte del flujo de los agentes, sino que constituyen una herramienta de evaluación independiente que el desarrollador utiliza para analizar manualmente la calidad del código generado

### 2.7 Nuevo subapartado: Revisión del alcance inicial
**Acción:** Añadir nuevo `\subsection{Revisión del alcance inicial}` al final de la Sección 2, antes de pasar a Metodología.

Contenido: comparación explícita entre el alcance comprometido en el GEP y el alcance final ejecutado:

- **Alcance GEP:** construir un sistema de agentes desde cero (Architect, Developer, Reviewer) integrado en el IDE
- **Alcance final:** desarrollar colbPowers como extensión de superpowers para ClaudeCode/OpenCode, cubriendo tres pilares (Toma de requerimientos, SDD, Seguimiento del cliente)
- **Justificación del cambio:** durante TP1 se descubrió que superpowers ya ofrecía la arquitectura orquestador/subagentes; construir desde cero habría sido redundante. El esfuerzo se redirigió hacia la contribución diferencial (constitution.md, features.md) y se amplió el alcance para cubrir el ciclo de vida completo del proyecto software
- **Sub-objetivos:** los cuatro sub-objetivos originales (separación de responsabilidades, coherencia arquitectónica, agentes autónomos, trazabilidad) se mantienen intactos en su esencia; solo cambia el mecanismo de implementación

### 2.8 Obstáculos y Riesgos
**Acción:** Sin cambios. Los outcomes se tratan en Sección 5.

---

## Sección 3 — Metodología y Rigor

### 3.1 Metodología de Trabajo
**Acción:** Añadir al final de la subsección.

**Texto a añadir:**
*"Un ejemplo concreto de esta metodología en acción fue el cambio de alcance producido al finalizar la fase TP1. Los hallazgos sobre la extensibilidad de los asistentes CLI y la existencia de superpowers fueron presentados al director del proyecto al cierre del sprint, permitiendo reorientar el Sprint Backlog en consecuencia sin comprometer la planificación global."*

### 3.2 Herramientas de Seguimiento y Control
**Acción:** Sin cambios.

---

## Sección 4 — Planificación (ahora subsección de Gestión del Proyecto)

### 4.0 Nuevo subapartado: Revisión de la planificación inicial
**Acción:** Añadir nuevo `\subsubsection{Revisión de la planificación inicial}` al final de la subsección Planificación, después del Diagrama de Gantt.

Contenido: comparación explícita entre la planificación comprometida en el GEP y la planificación final ejecutada:

- **DA1 GEP:** implementación de agentes Architect, Developer, Reviewer desde cero
- **DA1 final:** configuración del plugin colbPowers, estructura de constitution.md/features.md, agente orquestador base
- **DA2 GEP:** integración de métricas de evaluación en el agente Reviewer
- **DA2 final:** subagentes especializados + desarrollo de scripts de radon como herramienta de evaluación manual independiente
- **DA3 GEP:** AgentSkills e integración MCP
- **DA3 final:** ampliación de MCPs y refinamiento del flujo colbPowers — sin cambio significativo
- **DA4 GEP:** técnicas de Information Retrieval y MCPs avanzados
- **DA4 final:** módulos de toma de requerimientos (Azure Speech + LangChain/Tavily) y seguimiento del cliente
- **Justificación global:** la reducción de esfuerzo en el núcleo SDD (aprovechando superpowers) liberó horas que se reinvirtieron en los dos pilares adicionales, manteniendo el total de horas estimado (~540h) sin desviación significativa
- **Cuantificación:** incluir tabla comparativa de horas estimadas GEP vs. horas reales por fase

### 4.1 Párrafo de apertura
**Acción:** Cambio quirúrgico.

Reemplazar: *"ecosistema de agentes basados en Spec-Driven Development (SDD)"*  
Por: *"desarrollo de colbPowers y los módulos complementarios de toma de requerimientos y seguimiento del cliente"*

### 4.2 TP1 — Trabajo Previo
**Acción:** Reescribir descripción de TP1.

**Nuevo texto:**
*"Investigar el ecosistema de asistentes CLI extensibles (ClaudeCode, OpenCode) y plugins existentes, especialmente superpowers. Este estudio reveló que la arquitectura base ya existía y que su adopción era viable dentro del alcance del TFG. Este descubrimiento, unido a la constatación de que el esfuerzo de implementación del núcleo SDD era menor del previsto, permitió expandir el alcance del proyecto para incluir dos pilares adicionales: el módulo de toma de requerimientos y el módulo de seguimiento del cliente."*

### 4.3 DA — Desarrollo Ágil

**DA1 — Sprint 1: MVP**
- Descripción general: *"Implementar la versión base funcional de colbPowers: configuración del plugin en ClaudeCode y OpenCode, definición de la estructura de constitution.md y features.md, e implementación del agente orquestador con las skills base."*
- DA1.1: Configuración del plugin e integración con ClaudeCode/OpenCode
- DA1.2: Definición de la estructura de constitution.md y features.md
- DA1.3: Implementación del agente orquestador y skills base

**DA2 — Sprint 2: Subagentes especializados y métricas de evaluación**
- Descripción general: *"Implementar los subagentes especializados e integrar radon como herramienta de análisis estático independiente del flujo de agentes, utilizada por el desarrollador para evaluar manualmente la calidad del código generado."*
- DA2.1: Implementación del subagente implementador
- DA2.2: Implementación de los subagentes revisores (código y compatibilidad)
- DA2.3: Desarrollo de scripts de radon como herramienta de evaluación manual

**DA3 — Sprint 3: Habilidades e Integración MCP**
- Descripción general: actualizar terminología para reflejar contexto de plugin (en lugar de "agentes desde cero")
- Subtareas: mantener estructura, actualizar referencias

**DA4 — Sprint 4: Módulos complementarios y refinamiento final**
- Descripción general: *"Implementar el módulo de toma de requerimientos (transcripción con Azure Speech Service + procesamiento con LangChain/Tavily) y el módulo de seguimiento del cliente, y refinar el sistema completo."*
- DA4.1: Módulo de transcripción (Azure Speech Service)
- DA4.2: Módulo de procesamiento de requerimientos (LangChain/Tavily)
- DA4.3: Módulo de seguimiento del cliente y refinamiento global

### 4.4 PV — Pruebas y Validación
**Acción:** Cambio quirúrgico en PV1.

Reemplazar: *"scripts locales en Python y bash"* → *"scripts de radon y configuraciones del plugin colbPowers"*

### 4.5 Recursos de Software
**Acción:** Añadir herramientas nuevas a la lista existente.

- Azure Speech Service (transcripción de reuniones presenciales con diarización)
- LangChain + Tavily (procesamiento de requerimientos y búsqueda semántica web)
- radon (análisis estático de código)
- Añadir OpenCode junto a ClaudeCode en la categoría de asistentes IA

### 4.6 Tabla resumen de tareas
**Acción:** Actualizar descripciones de DA1-DA4 para reflejar los nuevos títulos de sprint. Horas y dependencias se mantienen.

### 4.7 Diagrama de Gantt
**Acción:** Sin cambios.

---

## Sección 5 — Gestión del Proyecto

### 5.1 Gestión de riesgos
**Acción:** Añadir nota de outcome SOLO a los riesgos que se materializaron.

- **Riesgo 1** (cambios en requerimientos): añadir al final — *"Este riesgo se materializó durante la fase TP1. El mecanismo de revisión de sprint absorbió el cambio de alcance de forma controlada, reorientando el Sprint Backlog sin comprometer la planificación global."*
- **Riesgo 4** (limitaciones IDE): añadir al final — *"Este riesgo se manifestó parcialmente. Los mecanismos nativos de extensibilidad (MCP, hooks, skills) resultaron suficientes para el flujo implementado."*
- **Riesgos 2, 3, 5, 6:** sin cambios.

### 5.2 Gestión económica
**Acción:** Actualizar descripciones de DA1-DA4 en "Coste por actividad" para reflejar los nuevos títulos de sprint. Cifras económicas sin cambios.

**Nuevo subapartado:** Añadir `\subsubsection{Revisión de los costes iniciales}` al final de la subsección Gestión económica, después del Coste total.

Contenido: comparación explícita entre el presupuesto comprometido en el GEP y la valoración económica final:

- **Presupuesto GEP:** 14.099,81€
- **Presupuesto final:** 14.099,81€ — sin variación
- **Justificación:** el cambio de alcance tuvo impacto económico neutro; las horas previstas para construir agentes desde cero se redistribuyeron entre la investigación del ecosistema (TP1 ampliado) y la implementación de los módulos de toma de requerimientos y seguimiento del cliente (DA4 reorientado)
- **Desviaciones por partida:** indicar si hubo desviaciones en costes de software (APIs, suscripciones) o hardware respecto a lo estimado, y su causa
- **Valoración económica del trabajo realizado:** cuantificar el coste real incurrido hasta la fecha de entrega comparado con la estimación, usando las mismas fórmulas de la sección de costes

### 5.3 Informe de sostenibilidad
**Acción:** Añadidos menores.

- **Dimensión económica:** añadir — *"La adopción de superpowers como base redujo significativamente las horas de desarrollo previstas, contribuyendo a mantener el presupuesto dentro de lo estimado."*
- **Dimensión social:** añadir — *"El uso de colbPowers como capa de abstracción reduce la curva de aprendizaje para nuevos desarrolladores, al proporcionar un marco de trabajo consistente independientemente del asistente utilizado."*
- **Dimensión ambiental:** sin cambios.

### 5.4 Leyes y regulaciones
**Acción:** Cambio quirúrgico en "Propiedad intelectual".

Añadir: colbPowers es una obra derivada de superpowers bajo su licencia open source, con contribuciones originales documentadas en el repositorio git del proyecto.

---

## Sección 6 — Cambios de Alcance del Proyecto

**Acción: Eliminar completamente.** Todo su contenido queda distribuido en las secciones anteriores según este diseño.

---

## Resumen de cambios por tipo

| Tipo | Cantidad estimada |
|---|---|
| Reescrituras completas | 4 (apertura S2, propuesta S1, TP1, DA1/DA4) |
| Cambios quirúrgicos (párrafo/frase) | ~15 |
| Añadidos (texto nuevo) | ~10 |
| Sin cambios | ~60% del documento |
| Eliminaciones | Sección 6 completa |
