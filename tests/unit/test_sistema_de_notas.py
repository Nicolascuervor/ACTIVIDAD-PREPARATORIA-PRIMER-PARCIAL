import pytest
from src.sistema_de_notas import SistemaDeNotas
from src.exceptions import NotaInvalidaError

def test_registrar_nota_valida_dentro_del_rango():
    """CP01: Registrar una nota válida dentro del rango (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.0)
    assert sistema.obtener_notas("estudiante_1")["Matemáticas"]["2023-1"] == 4.0

def test_registrar_nota_invalida_superior_al_maximo():
    """CP02: Intentar registrar una nota superior al límite máximo (Negativo)"""
    sistema = SistemaDeNotas()
    with pytest.raises(NotaInvalidaError):
        sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 6.0)

def test_registrar_nota_borde_inferior():
    """CP03: Registrar una nota en el límite exacto inferior (Borde)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 0.0)
    assert sistema.obtener_notas("estudiante_1")["Matemáticas"]["2023-1"] == 0.0

def test_aprobar_materia_borde_exacto():
    """CP04: Registrar nota en el límite exacto de aprobación (Borde)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 3.0)
    assert sistema.materia_aprobada("estudiante_1", "Matemáticas", "2023-1") is True

def test_reprobar_materia_debajo_del_borde():
    """CP05: Registrar nota justo por debajo del límite de aprobación (Borde)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 2.9)
    assert sistema.materia_aprobada("estudiante_1", "Matemáticas", "2023-1") is False

def test_aprobar_materia_holgadamente():
    """CP06: Registrar nota por encima del límite de aprobación (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.2)
    assert sistema.materia_aprobada("estudiante_1", "Matemáticas", "2023-1") is True

def test_calcular_promedio_estudiante_sin_notas():
    """CP07: Calcular promedio de un estudiante sin notas registradas (Borde)"""
    sistema = SistemaDeNotas()
    assert sistema.calcular_promedio("estudiante_nuevo") == 0.0

def test_calcular_promedio_una_sola_nota():
    """CP08: Calcular promedio con una sola nota registrada (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Física", "2023-1", 4.5)
    assert sistema.calcular_promedio("estudiante_1") == 4.5

def test_calcular_promedio_multiples_notas():
    """CP09: Calcular promedio con múltiples notas (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 3.0)
    sistema.registrar_nota("estudiante_1", "Física", "2023-1", 4.0)
    sistema.registrar_nota("estudiante_1", "Química", "2023-1", 5.0)
    assert sistema.calcular_promedio("estudiante_1") == 4.0

def test_bloquear_nota_duplicada_mismo_semestre():
    """CP10: Registrar dos notas para la misma materia en el mismo semestre (Negativo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.0)
    from src.exceptions import NotaDuplicadaError
    with pytest.raises(NotaDuplicadaError):
        sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.5)

def test_permitir_misma_materia_diferente_semestre():
    """CP11: Registrar notas para la misma materia en semestres diferentes (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.0)
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-2", 4.5)
    notas = sistema.obtener_notas("estudiante_1")["Matemáticas"]
    assert len(notas) == 2
    assert notas["2023-1"] == 4.0
    assert notas["2023-2"] == 4.5

def test_permitir_diferente_materia_mismo_semestre():
    """CP12: Registrar notas para materias diferentes en el mismo semestre (Positivo)"""
    sistema = SistemaDeNotas()
    sistema.registrar_nota("estudiante_1", "Matemáticas", "2023-1", 4.0)
    sistema.registrar_nota("estudiante_1", "Física", "2023-1", 3.5)
    notas = sistema.obtener_notas("estudiante_1")
    assert "Matemáticas" in notas
    assert "Física" in notas
    assert notas["Matemáticas"]["2023-1"] == 4.0
    assert notas["Física"]["2023-1"] == 3.5



