Lectura entera TFG con apuntes:
---

- Abstract: debería añadir "keywords"?

---

- Introducción: presento 3 (Toma de req, Desarrollo de código y Seguimiento del cliente)módulos y luego lo convierto en solo 2 (Solo hay dos apartados de implementación)
- 1.1.2: párrafo final contradice lo que se termina aplicando, se podría borrar tal cual
- 1.2.3: Agent Skill definición se podría mejorar. Ahora se dice que es cómo una herramienta o script que el agente puede usar, pero en realidad es un prompt que puede incluir scripts en subcarpetas que SÍ puede ejecutar, pero primero debe leer el prompt al activar la Skill.
- 1.2.4: Se introduce el apartado de transcripción por la cara cuando no se ha mencionado previamente in ningún momento.

- 1.4:
	+ En general quizás se podrían expandir estos apartados
	+ Se debería citar tanto 1.4.5 como 1.4.7.
- 1.5: Decir que colbPowers añade solamente constitution.md y features.md es pegarse un tiro en el pie. Lo simplifica muchísimo, cuando la implementación ha sido laboriosa.
- 1.6: 
	+ En la propuesta de implementación se vuelve a definirlos tres pilares de (Toma de req, Desarrollo de código y Seguimiento del cliente), cuando luego en la implementación simplemente junto el primer y segundo
	+ Explicar de nuevo que solo se ha añadido constitution.md y features.md es un understatement.
- 1.7: Esto me gusta, pero no sé si debería ir aquí.

---

2: Cambiada introducción
2.1: Se siguen planteando La toma de requerimientos y el módulo de seguimiento del cliente como apartados diferentes. Además 
2.5: 
	+ En la revisión del alcance vuelvo a hablar de los "tres pilares".
	+ De vuelta vuelvo a mencionar "constitution.md" + "features.md" como única diferencia entre superpowers.

---

3: Este apartado prácticamente NO ha cambiado
3.3: Preguntarle a David por este apartado.

---

4.1.3: Revisar estos sprints, cambiarle la definición a alguno de ellos pero sin tener que actualizar el diagrama de GANTT.

4.1.8: Revisar en mayor profundidad, pero otra vez estoy hablando de que colbPowers SOLO es consitution.md + features.md, cuando no es verdad.

4.4.4: Apartado identificado como crítico, le tengo que preguntar a David si esto se lo van a mirar.
4.5: Este apartado está bien, pero de nuevo he de preguntarle a David si alguien se va a mirar esto jaja.

---

---

5. Se me han colado un par de cosas en los diagramas. La transcripción NO hace el chunking, eso se hace directamente en la toma de requerimientos.

---

6.2.2 El flujo de funcionamiento de los agentes no se ve del todo claro, puesto que tenemos los pasos como \paragraph, y luego tenemos el apartado de "Similitud con ClaudeCode." también como paragraph, cuesta distinguir que es una sección y no un paso mas de el flujo de opencode.

6.3.1 code-review-graph, explicación demasiado breve, falta poner ejemplos de reducción de tokens. En el GitHub hay un par. También hay que explicar que se tuvieron que implementar plugins personalizados con Opencode para implementar esta herramienta.

---

7.2: Añadir un tipo de recuadro en gris que sea una nota aclarando que con n=3, estos resultados son meramente indicativos y se deberían sacar conclusiones con cautela?

---

9. Añadir en las conclusiones si se han cubierto los requisitos funcionales y no funcionales.