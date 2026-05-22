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

    def materia_aprobada(self, estudiante: str, materia: str, semestre: str) -> bool:
        nota = self.notas.get(estudiante, {}).get(materia, {}).get(semestre)
        if nota is None:
            raise ValueError("No se encontró nota para la materia en el semestre especificado")
        return nota >= 3.0

    def calcular_promedio(self, estudiante: str) -> float:
        notas_estudiante = self.notas.get(estudiante, {})
        todas_las_notas = [
            nota 
            for semestres in notas_estudiante.values() 
            for nota in semestres.values()
        ]
        
        return sum(todas_las_notas) / len(todas_las_notas) if todas_las_notas else 0.0





