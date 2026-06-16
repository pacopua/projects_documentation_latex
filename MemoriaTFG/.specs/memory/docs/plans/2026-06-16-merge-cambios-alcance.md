# Fusión de "Cambios de Alcance del Proyecto" en Secciones 1-5 — Plan de Implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use colbPowers:subagent-driven-development (recommended) or colbPowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Feature Reference:** Memoria TFG — actualización de secciones 1-5 para reflejar el alcance final del proyecto.

**Goal:** Eliminar la sección "Cambios de Alcance del Proyecto" distribuyendo su contenido en las secciones 1-5 de memoria.tex mediante cambios quirúrgicos, produciendo una narrativa cohesiva sin sección redundante.

**Architecture:** Ediciones directas sobre `memoria.tex` usando el tool Edit. Cada tarea es atómica y committable de forma independiente.

**Tech Stack:** LaTeX, git

---

## Task 1: Cambio estructural global — reorganizar jerarquía de secciones

**Files:**
- Modify: `memoria.tex` (líneas 341 y 536)

El objetivo es convertir `\section{Planificación}` en `\subsection{Planificación}` dentro de `\section{Gestión del Proyecto}`, moviendo la sección de Gestión del Proyecto para que preceda a Planificación.

- [x] **Step 1: Insertar `\section{Gestión del Proyecto}` antes de Planificación y eliminar la línea duplicada**

Reemplazar (línea ~341):
```latex
\section{Planificación}
\label{sec:descripcion_tareas}
```
Por:
```latex
\section{Gestión del Proyecto}
\label{sec:gestion_proyecto}

\subsection{Planificación}
\label{sec:descripcion_tareas}
```

- [x] **Step 2: Eliminar el `\section{Gestión del Proyecto}` original (línea ~536)**

Reemplazar:
```latex
\section{Gestión del Proyecto}
\label{sec:gestion_proyecto}

\subsection{Gestión de riesgos: Planes alternativos y obstáculos}
```
Por:
```latex
\subsection{Gestión de riesgos: Planes alternativos y obstáculos}
```

- [x] **Step 3: Bajar un nivel todos los `\subsection` dentro de Planificación**

Hacer los siguientes reemplazos (replace_all=false, uno por uno):

```
\subsection{GP - Gestión del proyecto}  →  \subsubsection{GP - Gestión del proyecto}
\subsection{TP - Trabajo Previo}        →  \subsubsection{TP - Trabajo Previo}
\subsection{DA - Desarrollo Ágil}       →  \subsubsection{DA - Desarrollo Ágil}
\subsection{PV - Pruebas y Validación}  →  \subsubsection{PV - Pruebas y Validación}
\subsection{Recursos}                   →  \subsubsection{Recursos}
\subsection{Tabla resumen de tareas}    →  \subsubsection{Tabla resumen de tareas}
\subsection{Diagrama de Gantt}          →  \subsubsection{Diagrama de Gantt}
```

- [x] **Step 4: Bajar un nivel todos los `\subsubsection` dentro de Planificación**

```
\subsubsection{Recursos Materiales}       →  \paragraph{Recursos Materiales}
\subsubsection{Recursos de Software}      →  \paragraph{Recursos de Software}
\subsubsection{Recursos Humanos}          →  \paragraph{Recursos Humanos}
\subsubsection{Desglose de horas por rol} →  \paragraph{Desglose de horas por rol}
```

- [x] **Step 5: Commit**

```bash
git add memoria.tex
git commit -m "refactor: mover Planificación como subsección de Gestión del Proyecto"
```

---

## Task 2: Sección 1 — Ampliar Estado del arte

**Files:**
- Modify: `memoria.tex` (subsección Estado del arte, ~líneas 175-200)

- [x] **Step 1: Ampliar subsección de herramientas de transcripción**

Reemplazar:
```latex
Para reuniones telemáticas, las plataformas de videoconferencia más extendidas (Microsoft Teams, Google Meet, Zoom) ofrecen transcripción automática integrada con diarización nativa, ya que cada participante habla desde su propio dispositivo. Para reuniones presenciales, las alternativas principales son Whisper \cite{radford2022whisper}, el modelo de reconocimiento de voz de OpenAI (ejecución local, sin coste de API, pero sin diarización nativa), y Azure Speech Service (servicio cloud con diarización de hablantes), que es la solución adoptada en este proyecto al estar incluida en la suscripción de Azure de Colb.AI.
```
Por:
```latex
Para reuniones telemáticas, las plataformas de videoconferencia más extendidas (Microsoft Teams, Google Meet, Zoom) ofrecen transcripción automática integrada con diarización nativa, ya que cada participante habla desde su propio dispositivo. Para reuniones presenciales, las alternativas principales son Whisper \cite{radford2022whisper}, el modelo de reconocimiento de voz de OpenAI (ejecución local, sin coste de API, pero sin diarización nativa), y \textbf{Azure Speech Service} (servicio cloud con diarización de hablantes). Se optó por Azure Speech Service al estar incluido en la suscripción de Azure de Colb.AI y por ofrecer resultados satisfactorios en las pruebas realizadas.
```

- [x] **Step 2: Ampliar subsección de herramientas de documentación de reuniones**

Reemplazar:
```latex
Existen herramientas comerciales orientadas a la generación automática de resúmenes y documentación post-reunión, como Otter.ai, Fireflies.ai o Microsoft Copilot for Teams. Sin embargo, estas soluciones generan resúmenes genéricos no parametrizables: no producen documentación con el formato estructurado específico que cada empresa de consultoría requiere, ni permiten adaptar la salida en función del tipo de reunión o del cliente. Esta limitación justifica el desarrollo de una solución propia que se integre con el flujo de trabajo y las plantillas de Colb.AI.
```
Por:
```latex
Existen herramientas comerciales orientadas a la generación automática de resúmenes y documentación post-reunión, como Otter.ai, Fireflies.ai o Microsoft Copilot for Teams. Sin embargo, estas soluciones generan resúmenes genéricos no parametrizables: no producen documentación con el formato estructurado específico que cada empresa de consultoría requiere, ni permiten adaptar la salida en función del tipo de reunión o del cliente. Esta limitación justifica el desarrollo de una solución propia que se integre con el flujo de trabajo y las plantillas de Colb.AI.

\subsubsection{Asistentes CLI extensibles}
\label{sec:asistentes_cli}
Las herramientas de asistencia a la programación de tipo CLI (\textit{Command-Line Interface}) representan una categoría diferenciada de los asistentes integrados en el IDE. Operan directamente desde la terminal con acceso nativo al sistema de archivos y exponen mecanismos de extensibilidad nativos ---plugins, hooks de ciclo de vida y el protocolo MCP (\textit{Model Context Protocol})--- que permiten definir flujos de trabajo de programación estructurados de forma composable. Las dos principales herramientas de este tipo son ClaudeCode \cite{claude_code_2024} (Anthropic) y OpenCode \cite{opencode_2025} (open source, compatible con modelos locales y remotos).

\subsubsection{superpowers plugin}
\label{sec:superpowers}
\textit{superpowers} es un plugin open source para ClaudeCode que implementa el patrón orquestador + subagentes mediante skills. Proporciona una arquitectura base para flujos de trabajo \textit{Spec-First}, en la que un agente orquestador coordina subagentes especializados a través de skills reutilizables. Sin embargo, carece de un mecanismo de constitución ni de features compartidas entre sesiones o desarrolladores distintos, lo que limita su capacidad para garantizar coherencia arquitectónica a lo largo del ciclo de vida de un proyecto.
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: ampliar estado del arte con CLI extensibles y superpowers"
```

---

## Task 3: Sección 1 — Análisis comparativo

**Files:**
- Modify: `memoria.tex` (subsección Análisis comparativo, ~líneas 201-228)

- [x] **Step 1: Añadir dos filas nuevas a la tabla comparativa**

Reemplazar:
```latex
    \hline
    \textbf{Copilot/Cursor} & \textit{Code-Driven} & Fomenta el \textit{slop code}, falta de planificación & Alta (pero sin contexto global) \\ 
    \hline
\end{tabularx}
\caption{Comparativa de soluciones existentes. [Fuente: Elaboración propia]}
\label{tab:comparativa_herramientas}
\end{table}
```
Por:
```latex
    \hline
    \textbf{Copilot/Cursor} & \textit{Code-Driven} & Fomenta el \textit{slop code}, falta de planificación & Alta (pero sin contexto global) \\ 
    \hline
    \textbf{ClaudeCode / OpenCode} & CLI extensible mediante plugins y MCP & Requiere plugin/configuración para imponer flujo \textit{Spec-First} & Alta \\
    \hline
    \textbf{superpowers} & Orquestador + subagentes via skills & Sin constitución ni \textit{features} globales entre sesiones & Alta \\
    \hline
\end{tabularx}
\caption{Comparativa de soluciones existentes. [Fuente: Elaboración propia]}
\label{tab:comparativa_herramientas}
\end{table}
```

- [x] **Step 2: Añadir párrafo de conclusión tras la tabla**

Reemplazar:
```latex
A la vista de estas limitaciones, la creación de una solución propia resulta razonable.
```
Por:
```latex
De las herramientas analizadas, \textit{superpowers} fue evaluado como candidato directo al problema planteado. Resuelve la orquestación de agentes, pero no garantiza coherencia arquitectónica entre sesiones ni entre desarrolladores distintos, ya que carece de un mecanismo de contexto persistente y compartido. Se decidió adoptarlo como base y extenderlo: el resultado es \textbf{colbPowers}, que añade la capa de \texttt{constitution.md} (reglas y estándares del proyecto) y \texttt{features.md} (registro de funcionalidades) como fuente de verdad compartida para todos los agentes.

A la vista de estas limitaciones, la creación de una solución propia resulta razonable.
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: ampliar análisis comparativo con CLI extensibles y superpowers"
```

---

## Task 4: Sección 1 — Reescribir Propuesta de implementación

**Files:**
- Modify: `memoria.tex` (subsección Propuesta de implementación, ~líneas 230-236)

- [x] **Step 1: Reescribir la subsección completa**

Reemplazar:
```latex
En lugar de depender de ecosistemas cerrados o frameworks pesados, hemos optado por aprovechar un concepto introducido recientemente en los IDEs más avanzados: los Agentes de Código \cite{vscode_agents} y las \textit{AgentSkills}\cite{agentskills_home}. Mediante la extensión y personalización de estas capacidades nativas de los entornos de desarrollo, propondremos un sistema híbrido de administración, planificación de tareas y generación de código que evite la fricción documental sin sacrificar la calidad estructural del proyecto. 
```
Por:
```latex
Aprovechando la arquitectura de \textit{superpowers}, el proyecto propone el desarrollo de \textbf{colbPowers}: un plugin para ClaudeCode y OpenCode que extiende el patrón orquestador/subagentes añadiendo una capa de contexto persistente basada en \texttt{constitution.md} y \texttt{features.md}. Este plugin estructura el ciclo de vida del software en torno a tres pilares complementarios:

\begin{enumerate}
    \item \textbf{Toma de requerimientos:} transformar transcripciones de reuniones en planes de implementación estructurados mediante búsqueda semántica web.
    \item \textbf{Spec-Driven Development:} garantizar que cada implementación esté precedida de una especificación validada, coordinada por un agente orquestador que invoca subagentes especializados (implementador, revisor de código, revisor de compatibilidad con specs/constitución/features).
    \item \textbf{Seguimiento del cliente:} automatizar la generación de documentación post-reunión con el formato específico de Colb.AI.
\end{enumerate}

Originalmente se contempló construir este sistema desde cero. Durante la fase de investigación previa (TP1) se descubrió que \textit{superpowers} ya ofrecía la arquitectura base necesaria, lo que permitió redirigir el esfuerzo hacia la contribución diferencial: la capa de constitución y features, y los tres pilares del ciclo de vida del software.
```

- [x] **Step 2: Commit**

```bash
git add memoria.tex
git commit -m "docs: reescribir propuesta de implementación con colbPowers y tres pilares"
```

---

## Task 5: Sección 2 — Reescribir apertura y Objetivo General

**Files:**
- Modify: `memoria.tex` (~líneas 242-248)

- [x] **Step 1: Reescribir párrafo de apertura de la sección**

Reemplazar:
```latex
De acuerdo con las necesidades de \textit{Colb.Ai} y la filosofía de documentar primero reglas y planes de implementación, y luego basar el código desarrollado en estos planes, este proyecto se centrará en el diseño e implementación de un ecosistema de agentes basados en el entorno de desarrollo para orquestar un flujo de trabajo basado en la metodología de \textit{Spec-Driven Development (SDD)}.
```
Por:
```latex
De acuerdo con las necesidades de \textit{Colb.Ai} y la filosofía de documentar primero reglas y planes de implementación, este proyecto se centrará en el desarrollo de \textbf{colbPowers}: un plugin para los asistentes CLI ClaudeCode y OpenCode que extiende el patrón orquestador/subagentes de \textit{superpowers} añadiendo una capa de contexto persistente basada en \texttt{constitution.md} y \texttt{features.md}. Este plugin cubre el ciclo de vida completo de un proyecto software, desde la toma de requerimientos hasta el seguimiento del cliente, estructurando el desarrollo bajo la metodología \textit{Spec-Driven Development (SDD)}.
```

- [x] **Step 2: Cambio quirúrgico en el párrafo principal del Objetivo General**

Reemplazar:
```latex
El objetivo principal de este proyecto es diseñar y desarrollar un sistema de asistencia a la programación compuesto por un equipo especializado de agentes de IA.
```
Por:
```latex
El objetivo principal de este proyecto es desarrollar \textbf{colbPowers} como extensión de \textit{superpowers} que añade \texttt{constitution.md} y \texttt{features.md} como contexto global compartido, estructurando el flujo de desarrollo mediante un agente orquestador que coordina subagentes especializados.
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: reescribir apertura y objetivo general de la sección de alcance"
```

---

## Task 6: Sección 2 — Actualizar sub-objetivos

**Files:**
- Modify: `memoria.tex` (~líneas 251-259)

- [x] **Step 1: Actualizar sub-objetivo "Separación de responsabilidades"**

Reemplazar:
```latex
\item \textbf{Separación efectiva de responsabilidades en el ciclo de desarrollo:} Conseguir que cada fase del proceso (diseño, implementación y revisión) sea ejecutada con criterios y restricciones propios, garantizando que ninguna etapa sea omitida y que el sistema reproduzca la dinámica de un equipo de desarrollo real con roles diferenciados (agente diseñador, agente desarrollador, agente revisor).
```
Por:
```latex
\item \textbf{Separación efectiva de responsabilidades en el ciclo de desarrollo:} Conseguir que cada fase del proceso (diseño, implementación y revisión) sea ejecutada con criterios y restricciones propios, garantizando que ninguna etapa sea omitida. Esta separación se materializa mediante skills que invocan subagentes especializados: un agente implementador, un agente revisor de código y un agente revisor de compatibilidad con las especificaciones, la constitución y las features del proyecto.
```

- [x] **Step 2: Actualizar sub-objetivo "Coherencia arquitectónica"**

Reemplazar:
```latex
\item \textbf{Coherencia arquitectónica mantenida a lo largo de todo el proyecto:} Lograr que los agentes dispongan en todo momento de un contexto actualizado con las reglas del proyecto, su \textit{roadmap} y el estado de las tareas, eliminando las inconsistencias causadas por la pérdida de memoria entre sesiones y asegurando que todas las decisiones de implementación sean coherentes con la arquitectura definida.
```
Por:
```latex
\item \textbf{Coherencia arquitectónica mantenida a lo largo de todo el proyecto:} Lograr que los agentes dispongan en todo momento de un contexto actualizado con las reglas del proyecto, su \textit{roadmap} y el estado de las tareas, eliminando las inconsistencias causadas por la pérdida de memoria entre sesiones. Esta coherencia se implementa concretamente mediante \texttt{constitution.md} y \texttt{features.md} como fuente de verdad compartida entre sesiones y desarrolladores.
```

- [x] **Step 3: Actualizar sub-objetivo "Trazabilidad"**

Reemplazar:
```latex
\item \textbf{Trazabilidad completa entre especificación y código entregado:} Garantizar que cada funcionalidad implementada pueda rastrearse desde su especificación original hasta el código final revisado, ofreciendo evidencia verificable de que lo entregado es coherente con lo planificado y cumple los estándares de calidad definidos.
```
Por:
```latex
\item \textbf{Trazabilidad completa entre especificación y código entregado:} Garantizar que cada funcionalidad implementada pueda rastrearse desde su especificación original hasta el código final revisado. Esta trazabilidad se garantiza porque todo cambio debe ser coherente con \texttt{constitution.md} y \texttt{features.md} antes de ser implementado, ofreciendo evidencia verificable de que lo entregado es coherente con lo planificado y cumple los estándares de calidad definidos.
```

- [x] **Step 4: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar sub-objetivos con referencias a constitution.md y subagentes"
```

---

## Task 7: Sección 2 — Actualizar requerimientos

**Files:**
- Modify: `memoria.tex` (~líneas 261-279)

- [x] **Step 1: Añadir dos nuevos requerimientos funcionales**

Reemplazar:
```latex
    \item Se le ha de ofrecer al desarrollador métricas para analizar la calidad y la estructura del código generado. Métricas como la \textit{Complejidad Ciclomática}\cite{McCabe_Complexity} del código, el Indice de Sostenibilidad del Código, y otras que se explorarán mas adelante.
\end{itemize}
```
Por:
```latex
    \item Se le ha de ofrecer al desarrollador métricas para analizar la calidad y la estructura del código generado. Métricas como la \textit{Complejidad Ciclomática}\cite{McCabe_Complexity} del código, el Indice de Sostenibilidad del Código, y otras que se explorarán mas adelante.
    \item El sistema debe incluir un módulo de procesamiento de transcripciones capaz de generar planes de implementación estructurados a partir de reuniones con el cliente, explorando automáticamente los \textit{frameworks} y tecnologías relevantes mediante búsqueda semántica en la web.
    \item El sistema debe incluir un módulo de generación de documentación de seguimiento post-reunión con el formato específico de Colb.AI, a partir de la transcripción de reuniones periódicas con el cliente.
\end{itemize}
```

- [x] **Step 2: Actualizar requerimiento no funcional "Integración Local"**

Reemplazar:
```latex
    \item \textbf{Integración Local:} El ecosistema debe poder acoplarse al entorno de desarrollo integrado (IDE) del usuario, utilizando protocolos de intercomunicación que permitan a los agentes actuar directamente sobre los archivos locales del proyecto.
```
Por:
```latex
    \item \textbf{Integración con asistentes CLI:} El plugin debe ser compatible con ClaudeCode y OpenCode, utilizando sus mecanismos nativos de extensibilidad (MCP, hooks, skills) para actuar directamente sobre los archivos locales del proyecto.
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: añadir requerimientos para módulos de transcripción y seguimiento"
```

---

## Task 8: Sección 2 — Actualizar Métricas de Evaluación

**Files:**
- Modify: `memoria.tex` (~líneas 281-294)

- [x] **Step 1: Actualizar referencia al mecanismo de cálculo**

Reemplazar:
```latex
Para validar empíricamente la calidad del código generado por el sistema, se emplearán métricas de análisis estático ampliamente adoptadas en la ingeniería del software \cite{sommerville_se_2015}. Estas métricas serán calculadas de forma automatizada por el agente \textit{Reviewer} sobre el código del repositorio local, y sus resultados se presentarán al desarrollador como parte de la auditoría.
```
Por:
```latex
Para validar empíricamente la calidad del código generado por el sistema, se emplearán métricas de análisis estático ampliamente adoptadas en la ingeniería del software \cite{sommerville_se_2015}. Estas métricas serán calculadas mediante \textbf{radon}, una herramienta Python de análisis estático de código. Es importante destacar que las métricas no forman parte del flujo automatizado de los agentes: constituyen una herramienta de evaluación independiente que el desarrollador utiliza para analizar manualmente la calidad del código generado y contrastar los resultados entre distintas ejecuciones del sistema.
```

- [x] **Step 2: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar métricas de evaluación para referenciar radon"
```

---

## Task 9: Sección 2 — Añadir subsección "Revisión del alcance inicial"

**Files:**
- Modify: `memoria.tex` (después de Obstáculos y Riesgos, ~línea 312)

- [x] **Step 1: Añadir la nueva subsección antes del `\newpage`**

Reemplazar:
```latex
    \item \textbf{Dependencia de la calidad de las especificaciones:} La eficacia del sistema está directamente condicionada por la calidad de la documentación que el desarrollador proporciona como entrada. Si las especificaciones son ambiguas, incompletas o contradictorias, los agentes generarán código igualmente deficiente, trasladando el problema en lugar de resolverlo. Este riesgo es especialmente relevante en equipos con poca cultura de documentación previa. La mitigación pasa por diseñar el agente diseñador con capacidad de detectar ambigüedades y solicitar aclaraciones antes de proceder, manteniendo siempre al desarrollador humano como árbitro final (\textit{Human in the Loop}).
\end{itemize}

\newpage

\section{Metodología y Rigor}
```
Por:
```latex
    \item \textbf{Dependencia de la calidad de las especificaciones:} La eficacia del sistema está directamente condicionada por la calidad de la documentación que el desarrollador proporciona como entrada. Si las especificaciones son ambiguas, incompletas o contradictorias, los agentes generarán código igualmente deficiente, trasladando el problema en lugar de resolverlo. Este riesgo es especialmente relevante en equipos con poca cultura de documentación previa. La mitigación pasa por diseñar el agente diseñador con capacidad de detectar ambigüedades y solicitar aclaraciones antes de proceder, manteniendo siempre al desarrollador humano como árbitro final (\textit{Human in the Loop}).
\end{itemize}

\subsection{Revisión del alcance inicial}
\label{sec:revision_alcance}

La planificación inicial del proyecto (GEP) establecía como objetivo principal la construcción desde cero de un ecosistema de tres agentes especializados (Architect, Developer, Reviewer) integrados en el entorno de desarrollo. Durante la fase de Trabajo Previo (TP1), la investigación del ecosistema de asistentes CLI reveló que \textit{superpowers} ya ofrecía la arquitectura orquestador/subagentes necesaria, haciendo redundante construir ese núcleo desde cero.

\begin{table}[H]
\centering
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}
    \hline
    \textbf{Alcance GEP} & \textbf{Alcance final} \\
    \hlineB{3}
    Construir agentes Architect, Developer y Reviewer desde cero & Desarrollar colbPowers como extensión de \textit{superpowers} \\
    \hline
    Integración en el IDE & Integración con asistentes CLI (ClaudeCode, OpenCode) \\
    \hline
    Un único pilar: SDD & Tres pilares: Toma de requerimientos, SDD, Seguimiento del cliente \\
    \hline
    Sin mecanismo de contexto persistente & \texttt{constitution.md} y \texttt{features.md} como fuente de verdad compartida \\
    \hline
\end{tabularx}
\caption{Comparativa entre el alcance comprometido en el GEP y el alcance final ejecutado. Elaboración propia.}
\label{tab:comparativa_alcance}
\end{table}

La justificación del cambio es doble. Por un lado, la adopción de \textit{superpowers} como base eliminó la necesidad de construir la capa de orquestación desde cero, redirigiendo el esfuerzo hacia la contribución diferencial: la capa de \texttt{constitution.md} y \texttt{features.md}. Por otro lado, la reducción de esfuerzo en el núcleo SDD liberó capacidad para incorporar los módulos de toma de requerimientos y seguimiento del cliente, ampliando el alcance del proyecto para cubrir el ciclo de vida completo del software. Los cuatro sub-objetivos originales (separación de responsabilidades, coherencia arquitectónica, agentes autónomos y trazabilidad) se mantienen intactos en su esencia; únicamente cambia el mecanismo de implementación.

\newpage

\section{Metodología y Rigor}
```

- [x] **Step 2: Commit**

```bash
git add memoria.tex
git commit -m "docs: añadir subsección de revisión del alcance inicial vs. GEP"
```

---

## Task 10: Sección 3 — Añadir párrafo sobre SCRUM y cambio de alcance

**Files:**
- Modify: `memoria.tex` (~líneas 319-325)

- [x] **Step 1: Añadir párrafo al final de la subsección Metodología de Trabajo**

Reemplazar:
```latex
Una pieza fundamental de esta metodología serán las reuniones diarias . Estas sesiones breves se llevarán a cabo de forma telemática mediante \textbf{Microsoft Teams} junto al equipo de \textit{Colb.Ai}. En ellas se expondrá el progreso realizado el día anterior y se iterará sobre las ideas del proceso actual. Esto asegurará que el desarrollo se mantenga alineado con los objetivos de la empresa y los estándares de calidad esperados.
```
Por:
```latex
Una pieza fundamental de esta metodología serán las reuniones diarias . Estas sesiones breves se llevarán a cabo de forma telemática mediante \textbf{Microsoft Teams} junto al equipo de \textit{Colb.Ai}. En ellas se expondrá el progreso realizado el día anterior y se iterará sobre las ideas del proceso actual. Esto asegurará que el desarrollo se mantenga alineado con los objetivos de la empresa y los estándares de calidad esperados.

Un ejemplo concreto de esta metodología en acción fue el cambio de alcance producido al finalizar la fase TP1. Los hallazgos sobre la extensibilidad de los asistentes CLI y la existencia de \textit{superpowers} fueron presentados al director del proyecto al cierre del sprint, permitiendo reorientar el Sprint Backlog en consecuencia sin comprometer la planificación global ni el presupuesto estimado.
```

- [x] **Step 2: Commit**

```bash
git add memoria.tex
git commit -m "docs: añadir párrafo sobre SCRUM absorbiendo el cambio de alcance"
```

---

## Task 11: Sección 4 — Actualizar apertura y TP1

**Files:**
- Modify: `memoria.tex` (~líneas 343 y 362)

- [x] **Step 1: Actualizar párrafo de apertura de Planificación**

Reemplazar:
```latex
Para garantizar el éxito en la implementación del ecosistema de agentes basados en Spec-Driven Development (SDD), se ha elaborado una planificación temporal detallada.
```
Por:
```latex
Para garantizar el éxito en el desarrollo de colbPowers y los módulos complementarios de toma de requerimientos y seguimiento del cliente, se ha elaborado una planificación temporal detallada.
```

- [x] **Step 2: Reescribir descripción de TP1**

Reemplazar:
```latex
    \item \textbf{TP1 - Estudio estado del arte (30h)}: Investigar las tecnologías, código y estructura que utilizan las alternativas como GitHub SpecKit y AgenOS. Se usará las ideas de estas como referencia para el desarrollo de la alternativa que trabajaremos en el TFG.
```
Por:
```latex
    \item \textbf{TP1 - Estudio estado del arte (30h)}: Investigar el ecosistema de asistentes CLI extensibles (ClaudeCode, OpenCode) y plugins existentes, especialmente \textit{superpowers}. Este estudio reveló que la arquitectura base ya existía y que su adopción era viable dentro del alcance del TFG. Este descubrimiento, unido a la constatación de que el esfuerzo de implementación del núcleo SDD era menor del previsto, permitió expandir el alcance del proyecto para incluir dos pilares adicionales: el módulo de toma de requerimientos y el módulo de seguimiento del cliente.
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar apertura planificación y descripción TP1"
```

---

## Task 12: Sección 4 — Actualizar DA1 y DA2

**Files:**
- Modify: `memoria.tex` (~líneas 378-390)

- [x] **Step 1: Reescribir DA1**

Reemplazar:
```latex
    \item \textbf{DA1 - Sprint 1: MVP (50h)}: Implementar la versión base funcional de los agentes asistentes en un entorno IDE (como VSCode).
    \begin{itemize}
        \item \textbf{DA1.1} Implementación del agente \textbf{Architect} y generación de contexto estático (15h).
        \item \textbf{DA1.2} Implementación del agente \textbf{Developer} para la lectura de requerimientos y generación de código (20h).
        \item \textbf{DA1.3} Implementación del agente \textbf{Reviewer} para auditoría básica (15h).
    \end{itemize}
```
Por:
```latex
    \item \textbf{DA1 - Sprint 1: MVP (50h)}: Implementar la versión base funcional de colbPowers: configuración del plugin en ClaudeCode y OpenCode, definición de la estructura de \texttt{constitution.md} y \texttt{features.md}, e implementación del agente orquestador con las skills base.
    \begin{itemize}
        \item \textbf{DA1.1} Configuración del plugin e integración con ClaudeCode y OpenCode (15h).
        \item \textbf{DA1.2} Definición de la estructura de \texttt{constitution.md} y \texttt{features.md} (20h).
        \item \textbf{DA1.3} Implementación del agente orquestador y skills base (15h).
    \end{itemize}
```

- [x] **Step 2: Reescribir DA2**

Reemplazar:
```latex
    \item \textbf{DA2 - Sprint 2: Implementación de Métricas de Evaluación (50h)}: Integrar herramientas y lógica para medir la calidad y sostenibilidad del código generado por el MVP.
    \begin{itemize}
        \item \textbf{DA2.1} Investigación, selección y configuración de métricas clave (Complejidad Ciclomática, Índice de Sostenibilidad, cobertura de código) (15h).
        \item \textbf{DA2.2} Desarrollo de \textit{scripts} de análisis automatizado para extraer estas métricas del repositorio local (20h).
        \item \textbf{DA2.3} Integración de las métricas en el flujo del agente \textbf{Reviewer} para enriquecer sus auditorías y bloqueos (15h).
    \end{itemize}
```
Por:
```latex
    \item \textbf{DA2 - Sprint 2: Subagentes especializados y métricas de evaluación (50h)}: Implementar los subagentes especializados de colbPowers e integrar radon como herramienta de análisis estático independiente del flujo de agentes.
    \begin{itemize}
        \item \textbf{DA2.1} Implementación del subagente implementador (15h).
        \item \textbf{DA2.2} Implementación de los subagentes revisores: revisor de código y revisor de compatibilidad con specs/constitución/features (20h).
        \item \textbf{DA2.3} Desarrollo de scripts de \textbf{radon} como herramienta de evaluación manual de la calidad del código generado (15h).
    \end{itemize}
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: reescribir descripciones de DA1 y DA2"
```

---

## Task 13: Sección 4 — Actualizar DA3 y DA4

**Files:**
- Modify: `memoria.tex` (~líneas 392-404)

- [x] **Step 1: Actualizar DA3**

Reemplazar:
```latex
    \item \textbf{DA3 - Sprint 3: Habilidades e Integración MCP (80h)}: Dotar a los agentes de capacidades de interacción con el entorno y aplicar el \textit{feedback} de las iteraciones anteriores.
    \begin{itemize}
        \item \textbf{DA3.1} Desarrollo de \textit{AgentSkills} básicas, control de versiones, creación de archivos específicos... (30h).
        \item \textbf{DA3.2} Integración de Model Context Protocols (MCPs) para proporcionarle al modelo más herramientas (25h).
        \item \textbf{DA3.3} Análisis de errores de los Sprints anteriores, corrección de \textit{prompts} y mejoras de estabilidad (25h).
    \end{itemize}
```
Por:
```latex
    \item \textbf{DA3 - Sprint 3: Habilidades e Integración MCP (80h)}: Ampliar las capacidades de colbPowers mediante MCPs adicionales y refinar el flujo completo basándose en el \textit{feedback} de los sprints anteriores.
    \begin{itemize}
        \item \textbf{DA3.1} Desarrollo de skills adicionales para colbPowers: control de versiones, gestión de archivos de especificación... (30h).
        \item \textbf{DA3.2} Integración de Model Context Protocols (MCPs) para ampliar las herramientas disponibles para los agentes (25h).
        \item \textbf{DA3.3} Análisis de errores de los sprints anteriores, corrección de prompts y mejoras de estabilidad del plugin (25h).
    \end{itemize}
```

- [x] **Step 2: Reescribir DA4**

Reemplazar:
```latex
    \item \textbf{DA4 - Sprint 4: Recuperación de Información y Refinamiento (80h)}: Ampliar el contexto de los agentes en repositorios grandes y finalizar el sistema.
    \begin{itemize}
        \item \textbf{DA4.1} Implementación de técnicas de \textit{Information Retrieval} para que los agentes puedan buscar información de frameworks y tecnologías nuevas (35h).
        \item \textbf{DA4.2} Integración de MCPs avanzados y herramientas externas (ej. conexión con GitHub para leer \textit{issues}) (25h).
        \item \textbf{DA4.3} Refinamiento del bucle colaborativo, optimización del uso de \textit{tokens} y resolución de \textit{bugs} finales (20h).
    \end{itemize}
```
Por:
```latex
    \item \textbf{DA4 - Sprint 4: Módulos complementarios y refinamiento final (80h)}: Implementar el módulo de toma de requerimientos y el módulo de seguimiento del cliente, y refinar el sistema completo.
    \begin{itemize}
        \item \textbf{DA4.1} Módulo de transcripción: integración con Azure Speech Service para transcripción con diarización de reuniones presenciales (35h).
        \item \textbf{DA4.2} Módulo de procesamiento de requerimientos: implementación con LangChain y Tavily para generación de planes de implementación a partir de transcripciones (25h).
        \item \textbf{DA4.3} Módulo de seguimiento del cliente y refinamiento global del sistema (20h).
    \end{itemize}
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: reescribir descripciones de DA3 y DA4"
```

---

## Task 14: Sección 4 — Actualizar PV, Recursos de Software y Tabla resumen

**Files:**
- Modify: `memoria.tex` (~líneas 411, 429-438, 482-485)

- [x] **Step 1: Actualizar PV1**

Reemplazar:
```latex
    \item \textbf{PV1 - Pruebas unitarias de las Agent Skills (20h)}: Verificación técnica de los \textit{scripts} locales en Python y bash para asegurar que interactúan correctamente con el sistema de archivos y el IDE.
```
Por:
```latex
    \item \textbf{PV1 - Pruebas unitarias de las Agent Skills (20h)}: Verificación técnica de los scripts de radon y las configuraciones del plugin colbPowers para asegurar que interactúan correctamente con el sistema de archivos y los asistentes CLI.
```

- [x] **Step 2: Actualizar Recursos de Software**

Reemplazar:
```latex
    \item \textbf{Servicios de Inteligencia Artificial:} Suscripciones activas o acceso a APIs de proveedores de modelos de lenguaje (LLMs) y agentes de código, como \textit{GitHub Copilot}, \textit{Claude Code} o las APIs de Anthropic/OpenAI.
```
Por:
```latex
    \item \textbf{Servicios de Inteligencia Artificial:} Suscripciones activas o acceso a APIs de proveedores de modelos de lenguaje (LLMs) y agentes de código, como \textit{Claude Code}, \textit{OpenCode} o las APIs de Anthropic/OpenAI. Adicionalmente, \textbf{Azure Speech Service} para la transcripción de reuniones presenciales con diarización, y \textbf{Tavily} como motor de búsqueda semántica para el módulo de toma de requerimientos.
    \item \textbf{Análisis de código:} \textbf{radon}, herramienta Python de análisis estático para el cálculo de métricas de calidad del código generado.
    \item \textbf{Orquestación:} \textbf{LangChain} para la construcción del pipeline de procesamiento de requerimientos.
```

- [x] **Step 3: Actualizar descripciones de DA en la tabla resumen**

Reemplazar:
```latex
\textbf{DA1} & Sprint 1: MVP & 50h & TP2 & Autor, PC, VSCode, APIs LLM \\
\textbf{DA2} & Sprint 2: Métricas de Evaluación & 50h & DA1 & Autor, PC, VSCode \\
\textbf{DA3} & Sprint 3: Habilidades e Int. MCP & 80h & DA1 & Autor, PC, VSCode, Git, Bash, Python \\
\textbf{DA4} & Sprint 4: Recup. Info. y Refinamiento & 80h & DA3 & Autor, PC, VSCode, Git, APIs LLM, Bash, Python \\
```
Por:
```latex
\textbf{DA1} & Sprint 1: MVP colbPowers & 50h & TP2 & Autor, PC, ClaudeCode, OpenCode \\
\textbf{DA2} & Sprint 2: Subagentes y métricas & 50h & DA1 & Autor, PC, Python, radon \\
\textbf{DA3} & Sprint 3: Habilidades e Int. MCP & 80h & DA1 & Autor, PC, Git, Bash, Python \\
\textbf{DA4} & Sprint 4: Módulos compl. y refinamiento & 80h & DA3 & Autor, PC, Azure Speech, LangChain, Tavily \\
```

- [x] **Step 4: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar PV1, recursos de software y tabla resumen"
```

---

## Task 15: Sección 4 — Añadir subsubsección "Revisión de la planificación inicial"

**Files:**
- Modify: `memoria.tex` (después del Diagrama de Gantt, ~línea 532)

- [x] **Step 1: Añadir nueva subsubsección después del bloque del Diagrama de Gantt**

Reemplazar:
```latex
\end{landscape}

\newpage

\subsection{Gestión de riesgos: Planes alternativos y obstáculos}
```
Por:
```latex
\end{landscape}

\subsubsection{Revisión de la planificación inicial}
\label{sec:revision_planificacion}

La planificación establecida en el GEP estructuraba el desarrollo en cuatro sprints centrados en la construcción de agentes desde cero. El cambio de alcance producido al finalizar TP1 implicó una redistribución del contenido de los sprints, manteniendo el número de fases y el total de horas estimado (~540h) sin desviación significativa.

\begin{table}[H]
\centering
\begin{tabularx}{\textwidth}{|>{\centering\arraybackslash}p{1cm}|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}
    \hline
    \textbf{Sprint} & \textbf{Planificación GEP} & \textbf{Planificación final} \\
    \hlineB{3}
    DA1 & Agentes Architect, Developer y Reviewer desde cero & Plugin colbPowers base: constitution.md, features.md, orquestador \\
    \hline
    DA2 & Métricas de evaluación integradas en el agente Reviewer & Subagentes especializados + scripts de radon como evaluación manual independiente \\
    \hline
    DA3 & AgentSkills e integración MCP & Ampliación de MCPs y refinamiento del flujo colbPowers --- sin cambio significativo \\
    \hline
    DA4 & Information Retrieval y MCPs avanzados & Módulo de toma de requerimientos (Azure Speech + LangChain/Tavily) y módulo de seguimiento del cliente \\
    \hline
\end{tabularx}
\caption{Comparativa entre la planificación del GEP y la planificación final ejecutada. Elaboración propia.}
\label{tab:comparativa_planificacion}
\end{table}

La justificación de estos cambios es consistente con lo descrito en la sección \ref{sec:revision_alcance}: la adopción de \textit{superpowers} redujo el esfuerzo necesario en DA1 y DA2, liberando capacidad que se reinvirtió en DA4 para los módulos complementarios. Las horas totales por fase se mantienen dentro del margen estimado; en la tabla \ref{tab:resumen_tareas} se recogen las horas estimadas, y en el apartado de gestión económica (\ref{sec:revision_costes}) se cuantifica el impacto económico real.

\newpage

\subsection{Gestión de riesgos: Planes alternativos y obstáculos}
```

- [x] **Step 2: Commit**

```bash
git add memoria.tex
git commit -m "docs: añadir subsubsección de revisión de la planificación inicial vs. GEP"
```

---

## Task 16: Sección 5 — Añadir outcomes a Riesgos 1 y 4

**Files:**
- Modify: `memoria.tex` (~líneas 543-581)

- [x] **Step 1: Añadir nota de outcome al Riesgo 1**

Reemplazar:
```latex
    \item \textbf{Recursos adicionales necesarios:} Horas extra del autor y disponibilidad del Director del proyecto para una sesión de rediseño.
\end{itemize}

\subsubsection{Riesgo 2: Bloqueo tecnológico
```
Por:
```latex
    \item \textbf{Recursos adicionales necesarios:} Horas extra del autor y disponibilidad del Director del proyecto para una sesión de rediseño.
    \item \textbf{Resultado:} Este riesgo se materializó durante la fase TP1. El mecanismo de revisión de sprint absorbió el cambio de alcance de forma controlada, reorientando el Sprint Backlog sin comprometer la planificación global ni el presupuesto estimado.
\end{itemize}

\subsubsection{Riesgo 2: Bloqueo tecnológico
```

- [x] **Step 2: Añadir nota de outcome al Riesgo 4**

Reemplazar:
```latex
    \item \textbf{Recursos adicionales necesarios:} Tiempo de diseño de \textit{prompts} por parte del autor y elaboración de documentación del flujo de uso dirigida al desarrollador.
\end{itemize}

\subsubsection{Riesgo 5: Desbordamiento
```
Por:
```latex
    \item \textbf{Recursos adicionales necesarios:} Tiempo de diseño de \textit{prompts} por parte del autor y elaboración de documentación del flujo de uso dirigida al desarrollador.
    \item \textbf{Resultado:} Este riesgo se manifestó parcialmente. Los mecanismos nativos de extensibilidad de ClaudeCode y OpenCode (MCP, hooks, skills) resultaron suficientes para implementar el flujo de trabajo requerido.
\end{itemize}

\subsubsection{Riesgo 5: Desbordamiento
```

- [x] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: añadir outcomes a Riesgo 1 y Riesgo 4"
```

---

## Task 17: Sección 5 — Actualizar Gestión económica y añadir revisión de costes

**Files:**
- Modify: `memoria.tex` (~líneas 646-670 y después de línea 835)

- [x] **Step 1: Actualizar descripción de DA1 en "Coste por actividad"**

Reemplazar:
```latex
    \item \textbf{DA1 (Sprint 1 - MVP):} Consta de 50 horas en total. Al tratarse de la implementación técnica de los agentes base en el entorno IDE, asignaremos la totalidad de estas horas al \textit{Programador junior}.
```
Por:
```latex
    \item \textbf{DA1 (Sprint 1 - MVP colbPowers):} Consta de 50 horas en total. Al tratarse de la configuración del plugin e implementación del agente orquestador base, asignaremos la totalidad de estas horas al \textit{Programador junior}.
```

- [ ] **Step 2: Actualizar descripción de DA2 en "Coste por actividad"**

Reemplazar:
```latex
    \item \textbf{DA2 (Sprint 2 - Métricas de Evaluación):} Consta de 50 horas. Las 15 horas iniciales de investigación y selección de métricas serán llevadas a cabo por el \textit{Investigador y documentador}, mientras que las 35 horas restantes de desarrollo de scripts e integración recaerán sobre el \textit{Programador junior}.
```
Por:
```latex
    \item \textbf{DA2 (Sprint 2 - Subagentes y métricas):} Consta de 50 horas. Las 15 horas iniciales de investigación y configuración de radon serán llevadas a cabo por el \textit{Investigador y documentador}, mientras que las 35 horas restantes de implementación de subagentes y scripts recaerán sobre el \textit{Programador junior}.
```

- [ ] **Step 3: Actualizar descripción de DA4 en "Coste por actividad"**

Reemplazar:
```latex
    \item \textbf{DA4 (Sprint 4 - Recuperación de Información y Refinamiento):} Cuenta con 80 horas totales. Asignaremos 20 horas al \textit{Investigador y documentador} para analizar y diseñar las técnicas de \textit{Information Retrieval}, y las 60 horas restantes al \textit{Programador junior} para la integración final y resolución de \textit{bugs}.
```
Por:
```latex
    \item \textbf{DA4 (Sprint 4 - Módulos complementarios y refinamiento):} Cuenta con 80 horas totales. Asignaremos 20 horas al \textit{Investigador y documentador} para el diseño de los módulos de transcripción y seguimiento, y las 60 horas restantes al \textit{Programador junior} para la implementación de los módulos y el refinamiento final del sistema.
```

- [ ] **Step 4: Añadir subsubsección de revisión de costes después del Coste total**

Reemplazar:
```latex
\subsubsection{Control de gestión}
\label{sec:control_gestion}
```
Por:
```latex
\subsubsection{Revisión de los costes iniciales}
\label{sec:revision_costes}

El presupuesto comprometido en el GEP ascendía a \textbf{14.099,81\euro}. El cambio de alcance producido durante TP1 tuvo un impacto económico prácticamente neutro: las horas previstas para construir agentes desde cero se redistribuyeron entre la investigación del ecosistema de extensibilidad (TP1 ampliado) y la implementación de los módulos complementarios (DA4 reorientado), sin incrementar el total de horas estimado.

\begin{table}[H]
    \centering
    \begin{tabular}{|l|c|c|}
         \hline
         \textbf{Partida} & \textbf{Estimación GEP} & \textbf{Estimación final} \\ 
         \hline
         \hline
         Coste de Personal & 10.262,02\euro & 10.262,02\euro \\
         Costes Genéricos & 1.488,07\euro & 1.488,07\euro \\
         Contingencias (15\%) & 1.762,52\euro & 1.762,52\euro \\
         Imprevistos & 587,20\euro & 587,20\euro \\
         \hline
         \textbf{TOTAL} & \textbf{14.099,81\euro} & \textbf{14.099,81\euro} \\
         \hline
    \end{tabular}
    \caption{Comparativa entre el presupuesto del GEP y la valoración económica final. Elaboración propia.}
    \label{tab:comparativa_costes}
\end{table}

La redistribución de horas entre fases no alteró los costes de personal porque los roles implicados en las tareas nuevas (DA4 reorientado) son los mismos que en las tareas sustituidas (DA1-DA2 originales). Los costes genéricos tampoco variaron de forma significativa: las herramientas nuevas incorporadas (Azure Speech Service, Tavily) están cubiertas por las suscripciones existentes de Colb.AI o tienen un coste marginal absorbible dentro de la partida de APIs LLM ya presupuestada.

\subsubsection{Control de gestión}
\label{sec:control_gestion}
```

- [ ] **Step 5: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar gestión económica y añadir revisión de costes iniciales"
```

---

## Task 18: Sección 5 — Actualizar Sostenibilidad y Leyes

**Files:**
- Modify: `memoria.tex` (~líneas 906-947)

- [ ] **Step 1: Añadir frase en Dimensión económica**

Reemplazar:
```latex
\textbf{Vida Útil:} Actualmente, la industria aborda el desarrollo asistido por IA de forma impulsiva (Code-Driven), lo que reduce costes iniciales pero dispara los de mantenimiento debido a la deuda técnica.
```
Por:
```latex
\textbf{Vida Útil:} Actualmente, la industria aborda el desarrollo asistido por IA de forma impulsiva (Code-Driven), lo que reduce costes iniciales pero dispara los de mantenimiento debido a la deuda técnica. La adopción de \textit{superpowers} como base redujo significativamente las horas de desarrollo previstas, contribuyendo a mantener el presupuesto dentro de lo estimado y liberando capacidad para los módulos complementarios.
```

- [ ] **Step 2: Añadir frase en Dimensión social**

Reemplazar:
```latex
\textbf{Vida Útil:} Existe una necesidad real en el mercado debido al creciente estrés y frustración profesional que genera trabajar con bases de código incoherentes.
```
Por:
```latex
\textbf{Vida Útil:} Existe una necesidad real en el mercado debido al creciente estrés y frustración profesional que genera trabajar con bases de código incoherentes. El uso de colbPowers como capa de abstracción reduce la curva de aprendizaje para nuevos desarrolladores, al proporcionar un marco de trabajo consistente independientemente del asistente CLI concreto que se utilice.
```

- [ ] **Step 3: Actualizar Propiedad intelectual en Leyes y regulaciones**

Reemplazar:
```latex
    El flujo Spec-Driven Development implementado en este proyecto sitúa explícitamente la generación de código en la categoría de IA asistida: el desarrollador define la especificación, valida el plan de implementación antes de que comience la escritura de código, y revisa el resultado entregado por el subagente. Toda esta intervención queda registrada en el repositorio git del proyecto, proporcionando la documentación requerida para acreditar la autoría humana.
```
Por:
```latex
    El flujo Spec-Driven Development implementado en este proyecto sitúa explícitamente la generación de código en la categoría de IA asistida: el desarrollador define la especificación, valida el plan de implementación antes de que comience la escritura de código, y revisa el resultado entregado por el subagente. Toda esta intervención queda registrada en el repositorio git del proyecto, proporcionando la documentación requerida para acreditar la autoría humana. Por otro lado, colbPowers es una obra derivada de \textit{superpowers}, distribuido bajo licencia open source, con contribuciones originales documentadas en el repositorio git del proyecto que constituyen la aportación diferencial del TFG.
```

- [ ] **Step 4: Commit**

```bash
git add memoria.tex
git commit -m "docs: actualizar sostenibilidad y leyes con referencias a colbPowers"
```

---

## Task 19: Eliminar Sección 6 — Cambios de Alcance del Proyecto

**Files:**
- Modify: `memoria.tex` (~líneas 951-1080)

- [ ] **Step 1: Verificar que no quedan `\ref{}` apuntando a labels de la sección a eliminar**

```bash
grep -n "ref{sec:cambios_alcance\|ref{sec:nuevos_objetivos\|ref{sec:estado_arte_actualizado\|ref{sec:impacto_planificacion" /home/adri/Desktop/UPC/8e_quatri/TFG/projects_documentation_latex/MemoriaTFG/memoria.tex
```
Esperado: sin resultados.

- [ ] **Step 2: Eliminar la sección completa**

Reemplazar el bloque completo (desde el `\newpage` previo hasta antes de `\section{Toma de Requerimientos}`):
```latex
\newpage

\section{Cambios de Alcance del Proyecto}
\label{sec:cambios_alcance}
```
hasta:
```latex
\newpage

\section{Toma de Requerimientos}
```

Dejando únicamente:
```latex
\newpage

\section{Toma de Requerimientos}
```

- [ ] **Step 3: Commit**

```bash
git add memoria.tex
git commit -m "docs: eliminar sección Cambios de Alcance del Proyecto (contenido integrado en S1-S5)"
```

---

## Task 20: Verificación final

**Files:**
- Read: `memoria.tex`

- [ ] **Step 1: Verificar que la sección 6 ya no aparece**

```bash
grep -n "Cambios de Alcance" /home/adri/Desktop/UPC/8e_quatri/TFG/projects_documentation_latex/MemoriaTFG/memoria.tex
```
Esperado: sin resultados.

- [ ] **Step 2: Verificar que los tres subapartados de revisión existen**

```bash
grep -n "revision_alcance\|revision_planificacion\|revision_costes" /home/adri/Desktop/UPC/8e_quatri/TFG/projects_documentation_latex/MemoriaTFG/memoria.tex
```
Esperado: 3 resultados (uno por label).

- [ ] **Step 3: Commit final**

```bash
git add memoria.tex
git commit -m "docs: verificación final — fusión de Cambios de Alcance completada"
```
