# Módulo de Registro de Notas Académicas

## Análisis de Pruebas (PARTE 1)

### 1.1 — Particiones de Equivalencia

Para el requerimiento "La nota debe estar entre 0.0 y 5.0", identificamos las siguientes particiones, tanto válidas como inválidas:

| Nombre de la Partición | Rango | Valor Representativo | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **INVÁLIDA (Negativa)** | `(-∞, 0.0)` | `-1.0` | Lanzar error (Nota inválida) |
| **VÁLIDA (Reprobado)** | `[0.0, 2.9]` | `2.5` | Registrar nota, el estudiante reprueba la materia |
| **VÁLIDA (Deficiente)** | `[3.0, 3.5]` | `3.2` | Registrar nota, resultado deficiente pero aprueba |
| **VÁLIDA (Debe Mejorar)** | `[3.6, 4.5]` | `4.0` | Registrar nota, resultado aceptable |
| **VÁLIDA (Aprobado)** | `[4.6, 5.0]` | `4.8` | Registrar nota, aprueba exitosamente |
| **INVÁLIDA (Exceso)** | `(5.0, ∞)` | `6.0` | Lanzar error (Nota inválida) |

### 1.2 — Análisis de Valores Límite

A continuación, los valores críticos en cada borde de los rangos definidos (0.0 a 5.0 y el límite de aprobación 3.0):

| Límite Analizado | Justo Antes del Límite | Límite Exacto | Justo Después del Límite |
| :--- | :--- | :--- | :--- |
| **Límite Inferior (0.0)** | `-0.1` (Fuera, Error) | `0.0` (Dentro, Reprobado) | `0.1` (Dentro, Reprobado) |
| **Límite de Aprobación (3.0)** | `2.9` (Reprobado) | `3.0` (Aprobado) | `3.1` (Aprobado) |
| **Límite Superior (5.0)** | `4.9` (Dentro, Aprobado) | `5.0` (Dentro, Aprobado) | `5.1` (Fuera, Error) |

### 1.3 — Preguntas al Product Owner

Respecto al requerimiento *"No se puede registrar dos notas para la misma materia en el mismo semestre. Si se intenta, el sistema debe lanzar un error claro"*, surgen estas preguntas:

1. **¿Se debe permitir la corrección de una nota ya ingresada en el mismo semestre si un profesor comete un error de digitación?**
   * **Justificación:** Impacta el diseño de casos de prueba porque define si debo probar un mecanismo de *actualización/sobrescritura* de nota (ej. `actualizar_nota()`) o si el error de duplicidad es un bloqueo absoluto de inserciones adicionales, obligando a diseñar casos de prueba donde cualquier segundo intento siempre falle.

2. **¿Qué sucede con el promedio acumulado si un estudiante pierde la materia y la repite en un semestre posterior (ej. misma materia, distinto semestre)?**
   * **Justificación:** Impacta los casos de prueba para el cálculo del promedio. Define si debo probar que el promedio suma ambas notas (la perdida y la repetida) o si la nota nueva reemplaza a la antigua en el cómputo final del promedio histórico del estudiante.


