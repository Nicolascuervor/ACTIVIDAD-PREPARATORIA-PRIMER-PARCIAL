from collections import defaultdict
from typing import Dict
from src.exceptions import NotaInvalidaError

class SistemaDeNotas:
    def __init__(self) -> None:
        self.notas: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(lambda: defaultdict(dict))

    def registrar_nota(self, estudiante: str, materia: str, semestre: str, nota: float) -> None:
        if not (0.0 <= nota <= 5.0):
            raise NotaInvalidaError("La nota debe estar entre 0.0 y 5.0")
        self.notas[estudiante][materia][semestre] = nota

    def obtener_notas(self, estudiante: str) -> Dict[str, Dict[str, float]]:
        return self.notas[estudiante]


