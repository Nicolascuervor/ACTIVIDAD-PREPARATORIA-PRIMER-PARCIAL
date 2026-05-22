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
