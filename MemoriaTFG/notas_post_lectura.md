Lectura entera TFG con apuntes:
# Review post lectura mia
---

- Introducción: presento 3 (Toma de req, Desarrollo de código y Seguimiento del cliente)módulos y luego lo convierto en solo 2 (Solo hay dos apartados de implementación)
- 1.1.2: párrafo final contradice lo que se termina aplicando, se podría borrar tal cual
- 1.2.3: Agent Skill definición se podría mejorar. Ahora se dice que es cómo una herramienta o script que el agente puede usar, pero en realidad es un prompt que puede incluir scripts en subcarpetas que SÍ puede ejecutar, pero primero debe leer el prompt al activar la Skill.
- 1.2.4: Se introduce el apartado de transcripción por la cara cuando no se ha mencionado previamente in ningún momento.

- 1.4:
	+ En general quizás se podrían expandir estos apartados
	+ Se debería citar tanto 1.4.5 como 1.4.7.

---

2: Cambiada introducción
2.1: Se siguen planteando La toma de requerimientos y el módulo de seguimiento del cliente como apartados diferentes. Además

---

3: Este apartado prácticamente NO ha cambiado
3.3: Preguntarle a David por este apartado.

---

4.1.3: Revisar estos sprints, cambiarle la definición a alguno de ellos pero sin tener que actualizar el diagrama de GANTT.

4.4.4: Apartado identificado como crítico, le tengo que preguntar a David si esto se lo van a mirar.

---

6.2.2 El flujo de funcionamiento de los agentes no se ve del todo claro, puesto que tenemos los pasos como \paragraph, y luego tenemos el apartado de "Similitud con ClaudeCode." también como paragraph, cuesta distinguir que es una sección y no un paso mas de el flujo de opencode.

6.3.1 code-review-graph, explicación demasiado breve, falta poner ejemplos de reducción de tokens. En el GitHub hay un par. También hay que explicar que se tuvieron que implementar plugins personalizados con Opencode para implementar esta herramienta.

---

7.2: Añadir un tipo de recuadro en gris que sea una nota aclarando que con n=3, estos resultados son meramente indicativos y se deberían sacar conclusiones con cautela?

Se explica bien la metodología estadistica que se ha seguido?? 

---

9. 
	+ Añadir en las conclusiones si se han cubierto los requisitos funcionales y no funcionales definidos anteriormente. [Done]
	+ Repasar conclusiones de resultados estadísticos.

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
