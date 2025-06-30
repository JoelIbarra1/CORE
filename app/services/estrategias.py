# services/estrategias.py

def binaria_match(r1, r2):
    return 1.0 if r1.lower() == r2.lower() else 0.0

def multiple_match(r1, r2):
    try:
        set1 = set(opt.strip().lower() for opt in r1.split(','))
        set2 = set(opt.strip().lower() for opt in r2.split(','))
        interseccion = len(set1 & set2)
        union = len(set1 | set2)
        return interseccion / union if union > 0 else 0.0
    except:
        return binaria_match(r1, r2)

def escala_match(r1, r2):
    try:
        v1 = float(r1)
        v2 = float(r2)
        return max(0.0, 1.0 - abs(v1 - v2) / 4.0)
    except:
        return 0.0

# Diccionario de estrategias
estrategias = {
    "binaria": binaria_match,
    "multiple": multiple_match,
    "escala": escala_match
}
