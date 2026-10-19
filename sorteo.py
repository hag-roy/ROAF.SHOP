import json
import random
from datetime import datetime

# Cargar la base de datos de la rifa
with open('boletos.json', 'r', encoding='utf-8') as file:
    participantes = json.load(file)

# Filtrar a los que siguen vivos en la rifa
activos = [p for p in participantes if not p['eliminado']]

# Si hay más de un activo, eliminamos a uno
if len(activos) > 1:
    victima = random.choice(activos)
    
    # Actualizar el estado del eliminado
    for p in participantes:
        if p['boleto'] == victima['boleto']:
            p['eliminado'] = True
            p['hora_eliminacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Eliminado: {p['nombre']} (Boleto {p['boleto']})")
            break
            
    # Guardar los cambios en el JSON
    with open('boletos.json', 'w', encoding='utf-8') as file:
        json.dump(participantes, file, indent=4, ensure_ascii=False)
else:
    print("Sorteo finalizado, ya tenemos ganador.")