from collections import defaultdict
from src.exceptions import NotaInvalidaError

class SistemaDeNotas:
    def __init__(self):
        self.notas = defaultdict(lambda: defaultdict(dict))

    def registrar_nota(self, estudiante, materia, semestre, nota):
        if not (0.0 <= nota <= 5.0):
            raise NotaInvalidaError("La nota debe estar entre 0.0 y 5.0")
        self.notas[estudiante][materia][semestre] = nota

    def obtener_notas(self, estudiante):
        return self.notas[estudiante]

