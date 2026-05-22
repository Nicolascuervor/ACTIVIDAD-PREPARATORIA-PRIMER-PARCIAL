# language: es
Característica: Registro y Consulta de Notas Académicas
  Como estudiante de la Universidad Regional del Sur
  Quiero que el sistema registre y gestione mis calificaciones
  Para poder llevar un control claro de mi rendimiento académico, saber si apruebo las materias y conocer mi promedio general.

  Antecedentes:
    Dado que el sistema de registro de notas está iniciado
    Y soy el estudiante "estudiante_1" registrado en el sistema

  @smoke @critical
  Escenario: Aprobar una materia con la nota mínima
    Dado que he cursado la materia de "Matemáticas" en el semestre "2023-1"
    Cuando registro una nota de 3.0 para esa materia
    Entonces el sistema me indica que la materia esta "aprobada"

  @regression
  Escenario: Reprobar una materia por no alcanzar la nota mínima
    Dado que he cursado la materia de "Matemáticas" en el semestre "2023-1"
    Cuando registro una nota de 2.9 para esa materia
    Entonces el sistema me indica que la materia esta "reprobada"

  @smoke @regression
  Esquema del escenario: Calcular el promedio con múltiples notas
    Dado que he registrado las notas de matemáticas <nota_matematicas>, física <nota_fisica>, y química <nota_quimica>
    Cuando consulto mi promedio general
    Entonces mi promedio general calculado es <promedio_esperado>

    Ejemplos:
      | nota_matematicas | nota_fisica | nota_quimica | promedio_esperado |
      | 3.0              | 4.0         | 5.0          | 4.0               |
      | 4.0              | 4.0         | 4.0          | 4.0               |
      | 2.0              | 3.0         | 4.0          | 3.0               |

  @regression
  Escenario: Consultar promedio sin tener notas registradas
    Dado que no tengo ninguna nota registrada en el sistema
    Cuando consulto mi promedio general
    Entonces mi promedio general calculado es 0.0

  @critical
  Escenario: Registrar notas de una misma materia en semestres diferentes
    Dado que he cursado la materia de "Matemáticas" en el semestre "2023-1"
    Y registro una nota de 4.0 para la materia "Matemáticas" en el semestre "2023-1"
    Cuando registro una nota de 4.5 para la materia "Matemáticas" en el semestre "2023-2"
    Entonces el sistema acepta el registro exitosamente
    Y la materia "Matemáticas" tiene notas guardadas tanto en "2023-1" como en "2023-2"

  @regression @critical
  Escenario: Error al intentar registrar dos notas para la misma materia en el mismo semestre
    Dado que he cursado la materia de "Matemáticas" en el semestre "2023-1"
    Y registro una nota de 4.0 para la materia "Matemáticas" en el semestre "2023-1"
    Cuando intento registrar una nueva nota de 4.5 para la materia "Matemáticas" en el semestre "2023-1"
    Entonces el sistema lanza un error indicando duplicidad
