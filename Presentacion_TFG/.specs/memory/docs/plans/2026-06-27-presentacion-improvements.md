# Presentación TFG — Improvements Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use colbPowers:subagent-driven-development (recommended) or colbPowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Feature Reference:** N/A — standalone document improvement plan for TFG defense presentation.

**Goal:** Apply 6 targeted edits to `presentacion.tex` that strengthen argumentation, add missing quantitative evidence, correct attribution of superpowers vs. colbPowers, and restructure methodology into 3 slides.

**Architecture:** All changes are self-contained edits to a single LaTeX/Beamer file (`presentacion.tex`). No new files. Each task is one logical change; compile after each to catch breakage early.

**Tech Stack:** LaTeX (Beamer, Madrid theme), `pdflatex` for compilation.

---

## Files

- Modify: `presentacion.tex` (all tasks)

---

### Task 1: Add 44% vulnerability statistic to Slide 3 (El problema)

**Context:** The problem slide lists the vicious cycle steps but gives no hard evidence. The thesis cites Pearce et al. (2022): 44% of Copilot-generated programs had security vulnerabilities. Adding this anchors the problem with a concrete number for the tribunal.

**Files:**
- Modify: `presentacion.tex` — inside the `\begin{column}{0.38\textwidth}` block of Slide 3, after `\end{itemize}` (~line 102)

- [ ] **Step 1: Locate the anchor**

  Find `% SLIDE 3`. Locate the `\end{itemize}` that closes the 5-item vicious cycle list (~line 102). The insertion goes immediately after it, before `\end{column}`.

- [ ] **Step 2: Insert the call-out**

  Replace:
  ```latex
              \end{itemize}
          \end{column}
          \begin{column}{0.58\textwidth}
  ```
  With:
  ```latex
              \end{itemize}
              \vspace{0.3cm}
              \footnotesize\textcolor{gray}{\textbf{44\%} de los programas generados con Copilot contienen vulnerabilidades de seguridad (Pearce et al., 2022).}
          \end{column}
          \begin{column}{0.58\textwidth}
  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  cd /home/adria/UPC/TFG/projects_documentation_latex/Presentacion_TFG
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; gray stat line appears below the bullet list on Slide 3 without column overflow.

- [ ] **Step 4: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Add Pearce et al. 44% statistic to problem slide"
  ```

---

### Task 2: Replace Slides 20–21 (Metodología) with 3 slides: casos → métricas → configuraciones

**Context:** Slides 20–21 mix the cases, statistical analysis, configurations and formulas in a confusing order. The user wants: cases first (what is being tested), then quality metrics (how it is measured), then configurations + statistical method (how the experiment is set up). This is also where the CC/MI thresholds (previously missing) get added.

**Files:**
- Modify: `presentacion.tex` — replace the two frames for Slides 20 and 21 with three new frames

- [ ] **Step 1: Locate the two frames to replace**

  Find `% SLIDE 20: METODOLOGÍA – PARTE 1` and `% SLIDE 21: METODOLOGÍA – PARTE 2`. The replacement spans from the `\begin{frame}{Metodología -- Parte 1}` line of Slide 20 to the `\end{frame}` line of Slide 21 (approximately lines 523–569).

- [ ] **Step 2: Replace both frames with three new frames**

  Delete everything from `% SLIDE 20` comment through the `\end{frame}` of Slide 21, and insert:

  ```latex
  % ============================================================
  % SLIDE 20: METODOLOGÍA – LOS CASOS
  % ============================================================
  \begin{frame}{Metodología -- Los casos}
      \begin{columns}[T]
          \begin{column}{0.48\textwidth}
              \begin{block}{Caso 1 -- Repo existente (DCM)}
                  \footnotesize
                  Eliminamos funcionalidades de un repositorio de \textit{colb.AI}. Se deben reimplementar en Flutter coordinando llamadas a API e interacción con base de datos.
              \end{block}
          \end{column}
          \begin{column}{0.48\textwidth}
              \begin{block}{Caso 2 -- Proyecto nuevo}
                  \footnotesize
                  Implementamos desde cero un proyecto Python para visualizar el funcionamiento de diversos algoritmos de clasificación.
              \end{block}
          \end{column}
      \end{columns}
  \end{frame}

  % ============================================================
  % SLIDE 21: METODOLOGÍA – MÉTRICAS DE CALIDAD
  % ============================================================
  \begin{frame}{Metodología -- Métricas de calidad}
      \textbf{Complejidad ciclomática} (McCabe):
      \begin{equation}
          \mathcal{CC}(G) = |E| - |V| + 2p
      \end{equation}

      \vspace{0.1cm}
      \textbf{Índice de mantenibilidad} (Halstead + CC):
      \begin{equation}
          V_H = (N_1 + N_2)\log_2(\eta_1 + \eta_2)
      \end{equation}
      \begin{equation}
          MI = \max\!\left(0,\;\frac{171 - 5{,}2\ln(V_H) - 0{,}23\,\mathcal{CC} - 16{,}2\ln(LoC)}{171} \times 100\right)
      \end{equation}
      \vspace{0.2cm}
      \footnotesize
      \textbf{Umbrales de referencia:}\;
      CC $\leq 10$ \textrightarrow{} módulo simple;\quad
      MI $< 20$ \textrightarrow{} código difícil de mantener.
  \end{frame}

  % ============================================================
  % SLIDE 21b: METODOLOGÍA – CONFIGURACIONES Y ANÁLISIS ESTADÍSTICO
  % ============================================================
  \begin{frame}{Metodología -- Configuraciones y análisis estadístico}
      \begin{columns}[T]
          \begin{column}{0.48\textwidth}
              \begin{block}{Configuraciones}
                  \footnotesize
                  \textbf{Baseline}: CLI sin ningún plugin.\\
                  \textbf{SDD}: colbPowers + code-review-graph.\\[0.2cm]
                  Probado con \textbf{Opencode} (Deepseek-V4-Flash) y \textbf{Claudecode} (Haiku 4.5).
              \end{block}
          \end{column}
          \begin{column}{0.48\textwidth}
              \begin{block}{Análisis estadístico}
                  \footnotesize
                  \textit{T de Welch} (no asume varianza similar) y \textbf{g de Hedges} (adecuada para n=3 muestras pequeñas).
              \end{block}
          \end{column}
      \end{columns}
  \end{frame}
  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; three new slides appear where the two old ones were.

- [ ] **Step 4: Verify slide order in PDF**

  Open `presentacion.pdf` and confirm the three metodología slides appear in order: cases → metrics (with thresholds) → configurations + stats.

- [ ] **Step 5: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Split metodología into 3 slides: cases, metrics, configurations"
  ```

---

### Task 3: Elevate homogenization finding in Slide 29 (Conclusiones) to alertblock (softened claim)

**Context:** The thesis observes that with colbPowers active, quality differences between OpenCode and ClaudeCode shrink noticeably — but calling it full statistical homogenization overstates the result. The alertblock should convey the trend without overclaiming. Currently the finding is buried as the third bullet in a flat list; an alertblock makes it visually prominent without asserting more than the data supports.

**Files:**
- Modify: `presentacion.tex` — inside Slide 29, around lines 697–699 (shifts after Task 2)

- [ ] **Step 1: Locate the anchor**

  Find `% SLIDE 29`. Inside the `\itemize`, find:
  ```latex
          \item \textbf{Resultado inesperado:} con colbPowers activo, las diferencias de calidad entre OpenCode y ClaudeCode desaparecen estadísticamente --- el flujo SDD \textbf{homogeneiza} la calidad con independencia del asistente.
          \vspace{0.1cm}
          \item \textbf{Sobrecoste de tokens:} $\times$2,2 -- $\times$4,5 respecto al baseline, constante en todos los experimentos.
      \end{itemize}
  ```

- [ ] **Step 2: Move the finding out of the list into a softened alertblock**

  Replace with:
  ```latex
          \item \textbf{Sobrecoste de tokens:} $\times$2,2 -- $\times$4,5 respecto al baseline, constante en todos los experimentos.
      \end{itemize}
      \vspace{0.1cm}
      \begin{alertblock}{Resultado inesperado}
          \footnotesize
          Con colbPowers activo, las diferencias de calidad entre OpenCode y ClaudeCode \textbf{se reducen notablemente} --- el flujo SDD \textbf{tiende a igualar} la calidad con independencia del asistente.
      \end{alertblock}
  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; alertblock appears below the bullet list without overflow. If it overflows, reduce `\vspace{0.1cm}` before the alertblock.

- [ ] **Step 4: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Add softened homogenization finding as alertblock in conclusions slide"
  ```

---

### Task 4: Fix Slide 8 attribution (superpowers vs. colbPowers) and add production note

**Context:** Slide 8 currently presents the isolated subagents and the `using-colbPowers` skill as if they were entirely original. In reality, the subagent orchestration mechanism comes from `superpowers`; `using-colbPowers` is a *modified version* of `using-superpowers`. colbPowers' real additions are: `constitution.md`/`features.md` as persistent context, the `defining-*` skills, and restricting subagent context to the explicit `design.md`. The right-column blocks need to be reworded to reflect this honestly. Additionally the slide should mention that colbPowers is already in production at Colb.AI.

**Files:**
- Modify: `presentacion.tex` — the right-column blocks of Slide 8 (~lines 289–300) and the frame closing (~line 301)

- [ ] **Step 1: Locate the right-column blocks**

  Find `% SLIDE 8`. In the right `\begin{column}{0.48\textwidth}`, find the two blocks:
  ```latex
              \begin{block}{Flujo SDD garantizado}
                  \footnotesize
                  Skill \textit{using-colbPowers} inyectada en \texttt{SessionStart}: las reglas de orquestación están activas \textbf{desde el primer mensaje}, sin depender de que el desarrollador las invoque.
              \end{block}
              \vspace{0.2cm}
              \begin{block}{Subagentes aislados}
                  \footnotesize
                  Implementador y revisor arrancan sin acceso al historial de conversación: solo ven el \texttt{design.md} explícito, eliminando la deriva conversacional.
              \end{block}
  ```

- [ ] **Step 2: Replace the two right-column blocks with corrected attribution**

  Replace with:
  ```latex
              \begin{block}{Flujo SDD garantizado}
                  \footnotesize
                  Skill \textit{using-colbPowers} (adaptación de \textit{using-superpowers}) inyectada en \texttt{SessionStart}: las reglas SDD activas \textbf{desde el primer mensaje}.
              \end{block}
              \vspace{0.2cm}
              \begin{block}{Subagentes aislados}
                  \footnotesize
                  Mecanismo de \textit{superpowers}; colbPowers restringe su contexto al \texttt{design.md} explícito, eliminando la deriva conversacional.
              \end{block}
  ```

- [ ] **Step 3: Add production note at the bottom of the frame**

  Find the frame closing:
  ```latex
  \end{columns}
  \end{frame}
  ```
  Replace with:
  ```latex
  \end{columns}
  \vspace{0.2cm}
  \footnotesize\centering\textit{Actualmente en producción en \textbf{Colb.AI} con valoración positiva desde su adopción.}
  \end{frame}
  ```

- [ ] **Step 4: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; Slide 8 right column now reads "adaptación de using-superpowers" and "Mecanismo de superpowers"; production note appears at the bottom.

- [ ] **Step 5: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Correct superpowers/colbPowers attribution on slide 8 + add production note"
  ```

---

### Task 5: Add token overhead figure to Slide 9 (Sostenibilidad — Ambiental)

**Context:** The Ambiental column currently says "Consumo inicial elevado" without a number. The thesis reports the structural overhead is ×2,2–×4,5 vs. baseline. Adding this makes the sustainability argument precise.

**Files:**
- Modify: `presentacion.tex` — Ambiental column of Slide 9 (~line 318, shifts after earlier tasks)

- [ ] **Step 1: Locate the anchor**

  Find `% SLIDE 9`. In the Ambiental column, find:
  ```latex
              Consumo inicial elevado, pero mejor documentado. La metodología SDD genera documentación que reduce el uso posterior de IA.\\[0.3cm]
  ```

- [ ] **Step 2: Add the overhead figure**

  Replace with:
  ```latex
              Consumo inicial elevado (sobrecoste estructural \textbf{×2,2--×4,5} respecto al baseline), pero genera documentación que reduce el uso posterior de IA.\\[0.3cm]
  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; ×2,2–×4,5 visible in the Ambiental column.

- [ ] **Step 4: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Add token overhead multiplier to sustainability slide"
  ```

---

### Task 6: Improve Slide 11 (Transcripción) — clarify hash and add diarization

**Context:** "Cálculo de hash" gives no hint as to why it matters. Diarización (up to 5 speakers) is a practical capability that distinguishes the system from simple transcription tools and is not currently mentioned.

**Files:**
- Modify: `presentacion.tex` — itemize inside Slide 11 (~lines 354–358, shifts after earlier tasks)

- [ ] **Step 1: Locate the anchor**

  Find `% SLIDE 11`. Inside the itemize, find:
  ```latex
              \item \textbf{FFmpeg} -- compresión de audio y cálculo de hash
              \item \textbf{Azure Speech-to-Text} -- transcripción
              \item \textbf{Azure Blob Storage} -- caché de resultados
  ```

- [ ] **Step 2: Replace with improved bullets**

  ```latex
              \item \textbf{FFmpeg} -- compresión y hash SHA-256 (evita re-transcripciones duplicadas)
              \item \textbf{Azure Speech-to-Text} -- transcripción con diarización (hasta 5 hablantes)
              \item \textbf{Azure Blob Storage} -- caché de resultados por hash
  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; updated bullet text on Slide 11.

- [ ] **Step 4: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Clarify hash purpose and add diarization detail to transcription slide"
  ```

---

---

### Task 7: Add slide on CLI extensibility mechanisms (before Slide 8)

**Context:** Slides 8, 16, 17, and 18 reference skills, the SessionStart hook, and MCP servers without ever defining them. The tribunal needs a one-slide primer on these three building blocks so the colbPowers explanation lands. The slide is minimal — a three-row table, no diagrams.

**Files:**
- Modify: `presentacion.tex` — insert a new frame immediately before `% SLIDE 8` (~line 272, shifts after earlier tasks)

- [ ] **Step 1: Locate the anchor**

  Find the comment `% SLIDE 8: LA DIFERENCIA: COLBPOWERS`. The new frame goes immediately before it.

- [ ] **Step 2: Insert the new frame**

  Insert before `% SLIDE 8`:
  ```latex
  % ============================================================
  % SLIDE 7b: MECANISMOS DE EXTENSIBILIDAD CLI
  % ============================================================
  \begin{frame}{Mecanismos de extensibilidad CLI}
      \vspace{0.2cm}
      \begin{tabular}{lp{0.72\textwidth}}
          \toprule
          \textbf{Skills} & Documentos Markdown que el agente lee bajo demanda para guiar su comportamiento en tareas específicas. \\[0.4cm]
          \textbf{Hooks}  & Comandos ejecutados automáticamente en eventos del ciclo de vida (p.ej.\ \texttt{SessionStart}). \\[0.4cm]
          \textbf{MCP}    & Servidores que exponen herramientas adicionales al agente vía el protocolo \textit{Model Context Protocol}. \\
          \bottomrule
      \end{tabular}
  \end{frame}

  ```

- [ ] **Step 3: Compile and verify**

  ```bash
  pdflatex -interaction=nonstopmode presentacion.tex 2>&1 | grep -E "^!" | head -10
  ```
  Expected: no errors; new slide appears between the simplified design diagram and the colbPowers difference slide, with a clean three-row table.

- [ ] **Step 4: Commit**

  ```bash
  git add presentacion.tex
  git commit -m "Add CLI extensibility concepts slide before colbPowers slide"
  ```

---

## Self-Review

**Spec coverage check:**
- [x] Add 44% stat → Task 1
- [x] Casos → métricas → configuraciones (3 slides) with CC/MI thresholds → Task 2
- [x] Softened homogenization alertblock → Task 3
- [x] Fix superpowers/colbPowers attribution + production note → Task 4
- [x] Token overhead in sustainability → Task 5
- [x] Diarization + hash clarification → Task 6

**Expected final page count:** 31 (original) + 1 (Task 2 adds one slide) = **32 pages**.

**Placeholder scan:** No TBDs or "implement later" items. Every step contains exact LaTeX.

**Consistency check:** All LaTeX fragments match the `\textbf`, `\footnotesize`, `\vspace`, `\begin{block}` patterns already in the file. No new packages required.
