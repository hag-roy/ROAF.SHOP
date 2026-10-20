import json
import random
from datetime import datetime, timedelta, timezone

# Cargar boletos
with open('boletos.json', 'r', encoding='utf-8') as file:
    participantes = json.load(file)

# Configurar hora exacta de México (UTC-6)
mexico_tz = timezone(timedelta(hours=-6))
ahora = datetime.now(mexico_tz)
hora = ahora.hour

activos = [p for p in participantes if not p['eliminado']]

# 1. A las 7:00 PM (19:00 hrs) sacamos al Gran Ganador de entre los últimos finalistas
if hora >= 19:
    if len(activos) > 1:
        ganador = random.choice(activos)
        for p in participantes:
            if not p['eliminado'] and p['boleto'] != ganador['boleto']:
                p['eliminado'] = True
                p['hora_eliminacion'] = ahora.strftime("%I:%M %p")
        print(f"¡Sorteo finalizado a las 7 PM! Ganador: {ganador['nombre']}")
    else:
        print("El ganador ya estaba decidido.")

# 2. De 3:00 PM a 6:30 PM, eliminamos de 5 en 5 cada media hora
elif hora >= 15:
    if len(activos) > 2: 
        # Calcula cuántos eliminar (5 por defecto, pero asegurando que mínimo queden 2 vivos)
        cantidad_eliminar = min(5, len(activos) - 2)
        victimas = random.sample(activos, cantidad_eliminar)
        
        nombres_eliminados = []
        for victima in victimas:
            for p in participantes:
                if p['boleto'] == victima['boleto']:
                    p['eliminado'] = True
                    p['hora_eliminacion'] = ahora.strftime("%I:%M %p")
                    nombres_eliminados.append(p['nombre'])
                    break
                    
        print(f"Eliminados a las {ahora.strftime('%I:%M %p')}: {', '.join(nombres_eliminados)}")
    else:
        print("Ya están los 2 finalistas listos. Esperando a las 7 PM.")
        
else:
    print("Aún no son las 3:00 PM. No hacemos nada.")

# Guardar actualización
with open('boletos.json', 'w', encoding='utf-8') as file:
    json.dump(participantes, file, indent=4, ensure_ascii=False)
