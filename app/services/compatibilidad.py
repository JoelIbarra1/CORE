from services.estrategias import estrategias

def calcular_coincidencia_por_tipo(r1: str, r2: str, tipo: str) -> float:
    estrategia = estrategias.get(tipo)
    if not estrategia:
        return 0.0  # Tipo desconocido
    return estrategia(r1, r2)
