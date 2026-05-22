# Módulo de Registro de Notas Académicas

## Análisis de Pruebas (PARTE 1)

### 1.1 — Particiones de Equivalencia

Para el requerimiento "La nota debe estar entre 0.0 y 5.0", identificamos las siguientes particiones, tanto válidas como inválidas:

| Nombre de la Partición | Rango | Valor Representativo | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Valor negativo | `( menor a 0 , 0.0)` | `-1.0` | Se lanza un error debido a que la nota es inválida |
| El estudiante reprobó | `[0.0, 2.9]` | `2.5` | Registrar nota y el estudiante reprueba la materia |
| Deficiente | `[3.0, 3.5]` | `3.2` | Registrar nota y resultado deficiente pero aprueba |
| Debe Mejorar | `[3.6, 4.5]` | `4.0` | Registrar nota y resultado aceptable |
| Aprobado | `[4.6, 5.0]` | `4.8` | Registrar nota, aprueba exitosamente |
| Exceso | `(5.0, ∞)` | `6.0` | Se lanza un error debido a que la nota es inválida y sobrepasa los límites establecidos |

### 1.2 — Análisis de Valores Límite

A continuación, los valores críticos en cada borde de los rangos definidos (0.0 a 5.0 y el límite de aprobación 3.0):

| Límite Analizado | Justo Antes del Límite | Límite Exacto | Justo Después del Límite |
| :--- | :--- | :--- | :--- |
| **Límite Inferior (0.0)** | `-0.1` (Fuera, Error) | `0.0` (Dentro, Reprobado) | `0.1` (Dentro, Reprobado) |
| **Límite de Aprobación (3.0)** | `2.9` (Reprobado) | `3.0` (Aprobado) | `3.1` (Aprobado) |
| **Límite Superior (5.0)** | `4.9` (Dentro, Aprobado) | `5.0` (Dentro, Aprobado) | `5.1` (Fuera, Error) |

### 1.3 — Preguntas al Product Owner

Respecto al requerimiento mencionado de  "No se puede registrar dos notas para la misma materia en el mismo semestre. Si se intenta, el sistema debe lanzar un error claro y sugerente", surgen estas preguntas:

¿Se debe permitir o debe ser posible la corrección de una nota ya ingresada en el mismo semestre si un profesor comete un error de digitación?

Esto lo pregunto ya que directamente Impacta el diseño de casos de prueba porque define si debo probar un mecanismo de actualización/sobrescritura de nota o si el error de duplicidad es un bloqueo absoluto de inserciones adicionales, llevándome a diseñar casos de prueba donde cualquier segundo intento siempre falle.

¿Qué pasará con el promedio acumulado si un estudiante pierde la materia y la repite en un semestre posterior, ejemplo una misma materia pero distinto semestre)? 

Esto es debido al impacto en los casos de prueba para el cálculo del promedio. Ya que definen si debo probar que el promedio suma ambas notas, la pérdida y la repetida o si la nota nueva reemplaza a la antigua en el cómputo final del promedio histórico del estudiante.

## Diseño formal de casos de prueba (PARTE 2)

A continuación, se presentan los casos de prueba diseñados con base en el análisis previo.

| ID | Requerimiento | Descripción | Precondición | Datos de entrada | Pasos | Resultado esperado | Tipo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CP01** | REQ1 - Nota entre 0.0 y 5.0 | Registrar una nota válida dentro del rango (Partición Válida) | Estudiante y materia existen en el sistema | Nota = 4.0 | 1. Seleccionar estudiante y materia. 2. Ingresar la nota 4.0. 3. Guardar el registro. | La nota se registra exitosamente en el sistema | Positivo |
| **CP02** | REQ1 - Nota entre 0.0 y 5.0 | Intentar registrar una nota superior al límite máximo (Partición Inválida) | Estudiante y materia existen en el sistema | Nota = 6.0 | 1. Seleccionar estudiante y materia. 2. Ingresar la nota 6.0. 3. Guardar el registro. | El sistema rechaza el ingreso y lanza un error indicando que la nota es inválida | Negativo |
| **CP03** | REQ1 - Nota entre 0.0 y 5.0 | Registrar una nota en el límite exacto inferior (Valor Límite) | Estudiante y materia existen en el sistema | Nota = 0.0 | 1. Seleccionar estudiante y materia. 2. Ingresar la nota 0.0. 3. Guardar el registro. | La nota se registra exitosamente | Borde |
| **CP04** | REQ2 - Aprobar/Reprobar | Registrar nota en el límite exacto de aprobación | Estudiante y materia existen en el sistema | Nota = 3.0 | 1. Ingresar nota 3.0. 2. Consultar estado de la materia para el estudiante. | El sistema registra la nota y determina que el estudiante **aprueba** la materia | Borde |
| **CP05** | REQ2 - Aprobar/Reprobar | Registrar nota justo por debajo del límite de aprobación | Estudiante y materia existen en el sistema | Nota = 2.9 | 1. Ingresar nota 2.9. 2. Consultar estado de la materia para el estudiante. | El sistema registra la nota y determina que el estudiante **reprueba** la materia | Borde |
| **CP06** | REQ2 - Aprobar/Reprobar | Registrar nota por encima del límite de aprobación | Estudiante y materia existen en el sistema | Nota = 4.2 | 1. Ingresar nota 4.2. 2. Consultar estado de la materia para el estudiante. | El sistema registra la nota y determina que el estudiante **aprueba** la materia | Positivo |
| **CP07** | REQ3 - Calcular promedio | Calcular promedio de un estudiante sin notas registradas | El estudiante existe pero no tiene notas en el sistema | Ninguno | 1. Solicitar el cálculo del promedio para el estudiante. | El sistema retorna 0.0 (sin fallar por división entre cero) | Borde |
| **CP08** | REQ3 - Calcular promedio | Calcular promedio con una sola nota registrada | El estudiante tiene exactamente 1 nota registrada | Nota = 4.5 (Física) | 1. Solicitar el cálculo del promedio para el estudiante. | El sistema retorna exactamente 4.5 como promedio | Positivo |
| **CP09** | REQ3 - Calcular promedio | Calcular promedio con múltiples notas | El estudiante tiene 3 notas registradas | Notas: Mat(3.0), Fis(4.0), Quim(5.0) | 1. Solicitar el cálculo del promedio para el estudiante. | El sistema retorna 4.0 como promedio | Positivo |
| **CP10** | REQ4 - No duplicar nota | Registrar dos notas para la misma materia en el mismo semestre | El estudiante ya tiene registrada la materia Matemáticas en el semestre 2023-1 | Materia = Matemáticas, Semestre = 2023-1, Nota = 4.0 | 1. Intentar registrar una segunda nota para Matemáticas en 2023-1. | El sistema bloquea el registro y lanza un error claro de duplicidad | Negativo |
| **CP11** | REQ4 - No duplicar nota | Registrar notas para la misma materia en semestres diferentes | El estudiante ya tiene registrada la materia Matemáticas en 2023-1 | Materia = Matemáticas, Semestre = 2023-2, Nota = 4.5 | 1. Registrar nota para Matemáticas en 2023-2. | La nota se registra exitosamente (materias repetidas en distinto semestre) | Positivo |
| **CP12** | REQ4 - No duplicar nota | Registrar notas para materias diferentes en el mismo semestre | El estudiante ya tiene registrada la materia Matemáticas en 2023-1 | Materia = Física, Semestre = 2023-1, Nota = 3.5 | 1. Registrar nota para Física en 2023-1. | La nota se registra exitosamente (son materias distintas) | Positivo |

## Cobertura de Pruebas (PARTE 3)

Se implementaron los requerimientos utilizando la metodología TDD (Red-Green-Refactor). La cobertura de código obtenida superó el umbral requerido (85%). A continuación, se presenta el reporte de cobertura final:

```text
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.14.0-final-0 _______________

Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src\__init__.py               0      0   100%
src\exceptions.py             4      0   100%
src\models.py                 0      0   100%
src\sistema_de_notas.py      23      1    96%   25
-------------------------------------------------------
TOTAL                        27      1    96%
============================= 12 passed in 0.11s ==============================
```

## Reflexión (PARTE 6)

**¿Qué diferencia notaste entre diseñar los casos de prueba en la tabla antes de escribir código versus simplemente ponerte a programar directamente?**
Diseñar los casos de prueba primero obliga a adoptar una mentalidad analítica orientada al producto (pensamiento de tester). Permite vislumbrar de antemano los escenarios borde, las precondiciones, y qué comportamientos son inválidos antes de escribir una sola línea lógica. Cuando uno se lanza a programar directamente, es fácil perder de vista los requerimientos de negocio u obviar caminos excepcionales, ya que la mente está ocupada resolviendo el "cómo" técnico en lugar del "qué" necesita el usuario. En resumen, la tabla funciona como un mapa que garantiza construir el software correcto.

**¿Qué fue lo más difícil de seguir el ciclo TDD y en qué momento sentiste la tentación de saltarte algún paso?**
Lo más complejo del ciclo TDD es desarrollar la disciplina de contención. Constantemente surge la tentación de escribir más código del estrictamente necesario para que pase la prueba actual (saltarse la regla del código mínimo en la fase GREEN) o de escribir la lógica y la prueba al mismo tiempo. Esto ocurrió particularmente en el Requerimiento 2 y 4, donde la implementación era tan breve (como un simple `if nota >= 3.0`) que el impulso natural es escribir el método completo sin antes haber visto fallar el test en la fase RED. Resistir esa tentación asegura una cobertura real y protege el código a futuro.








