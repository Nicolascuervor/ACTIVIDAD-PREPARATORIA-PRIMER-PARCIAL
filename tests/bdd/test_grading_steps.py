import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.sistema_de_notas import SistemaDeNotas
from src.exceptions import NotaDuplicadaError

scenarios('features/grading.feature')

@pytest.fixture
def context():
    return {}

@given('que el sistema de registro de notas está iniciado')
def iniciar_sistema(context):
    context['sistema'] = SistemaDeNotas()
    context['error'] = None

@given(parsers.parse('soy el estudiante "{estudiante}" registrado en el sistema'))
def establecer_estudiante(context, estudiante):
    context['estudiante'] = estudiante

@given(parsers.parse('que he cursado la materia de "{materia}" en el semestre "{semestre}"'))
def cursar_materia(context, materia, semestre):
    context['materia_actual'] = materia
    context['semestre_actual'] = semestre

@given(parsers.parse('registro una nota de {nota:f} para esa materia en "{semestre}"'))
def registrar_nota_previa(context, nota, semestre):
    context['sistema'].registrar_nota(
        context['estudiante'], 
        context['materia_actual'], 
        semestre, 
        nota
    )

@given(parsers.parse('registro una nota de {nota:f} para la materia "{materia}" en el semestre "{semestre}"'))
def registrar_nota_previa_completa(context, nota, materia, semestre):
    context['sistema'].registrar_nota(context['estudiante'], materia, semestre, nota)

@given(parsers.parse('que he registrado las notas de matemáticas {nota_mat:f}, física {nota_fis:f}, y química {nota_quim:f}'))
def registrar_multiples_notas(context, nota_mat, nota_fis, nota_quim):
    estudiante = context['estudiante']
    context['sistema'].registrar_nota(estudiante, "Matemáticas", "2023-1", nota_mat)
    context['sistema'].registrar_nota(estudiante, "Física", "2023-1", nota_fis)
    context['sistema'].registrar_nota(estudiante, "Química", "2023-1", nota_quim)

@given('que no tengo ninguna nota registrada en el sistema')
def sin_notas(context):
    pass

@when(parsers.parse('registro una nota de {nota:f} para esa materia'))
def registrar_nota_when(context, nota):
    estudiante = context['estudiante']
    materia = context['materia_actual']
    semestre = context['semestre_actual']
    context['sistema'].registrar_nota(estudiante, materia, semestre, nota)

@when(parsers.parse('registro una nota de {nota:f} para la materia "{materia}" en el semestre "{semestre}"'))
def registrar_nota_when_completa(context, nota, materia, semestre):
    context['sistema'].registrar_nota(context['estudiante'], materia, semestre, nota)

@when('consulto mi promedio general')
def consultar_promedio(context):
    context['promedio'] = context['sistema'].calcular_promedio(context['estudiante'])

@when(parsers.parse('intento registrar una nueva nota de {nota:f} para la materia "{materia}" en el semestre "{semestre}"'))
def intentar_registrar_nota_duplicada(context, nota, materia, semestre):
    try:
        context['sistema'].registrar_nota(context['estudiante'], materia, semestre, nota)
    except Exception as e:
        context['error'] = e

@when(parsers.parse('intento registrar una nueva nota de {nota:f} para la materia "{materia}" en el mismo semestre "{semestre}"'))
def intentar_registrar_nota_duplicada_mismo(context, nota, materia, semestre):
    try:
        context['sistema'].registrar_nota(context['estudiante'], materia, semestre, nota)
    except Exception as e:
        context['error'] = e

@then(parsers.parse('el sistema me indica que la materia esta "{estado}"'))
def verificar_estado_materia(context, estado):
    estudiante = context['estudiante']
    materia = context['materia_actual']
    semestre = context['semestre_actual']
    aprobada = context['sistema'].materia_aprobada(estudiante, materia, semestre)
    
    if estado == "aprobada":
        assert aprobada is True
    elif estado == "reprobada":
        assert aprobada is False
    else:
        pytest.fail(f"Estado desconocido: {estado}")

@then(parsers.parse('mi promedio general calculado es {promedio_esperado:f}'))
def verificar_promedio(context, promedio_esperado):
    assert context['promedio'] == promedio_esperado

@then('el sistema acepta el registro exitosamente')
def verificar_registro_exitoso(context):
    assert context['error'] is None

@then(parsers.parse('la materia "{materia}" tiene notas guardadas tanto en "{sem1}" como en "{sem2}"'))
def verificar_notas_diferentes_semestres(context, materia, sem1, sem2):
    notas = context['sistema'].obtener_notas(context['estudiante'])[materia]
    assert sem1 in notas
    assert sem2 in notas

@then('el sistema lanza un error indicando duplicidad')
def verificar_error_duplicidad(context):
    assert context['error'] is not None
    assert isinstance(context['error'], NotaDuplicadaError)
