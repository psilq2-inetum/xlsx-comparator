from time import time

def autorise_ecart(seuil: float):
    return lambda a, b: abs(float(a) - float(b)) <= seuil

def comparer_float():
    return lambda a, b: float(a) == float(b)

def round_float(precision: int):
    return lambda a, b: round(float(a), precision) == round(float(b), precision)

def print_avancement(lignes_traitees, lignes_totales, lignes_manquantes, delais_message, last_time):
    current_time = time()
    if current_time - last_time > delais_message:
        print(f"Progress: {lignes_traitees / lignes_totales * 100}% ({lignes_traitees}/{lignes_totales}) - Manquantes: {lignes_manquantes}")
        return current_time
    return last_time

def comparer_lowercase():
    return lambda a,b: a.lower() == b.lower() 
