import requests
from icalendar import Calendar
from datetime import datetime

ICAL_URL = "https://utpl.instructure.com/feeds/calendars/user_YJtudqZ7BdUOKqyPp98Tc2ffrYPgb37BquKYN32c.ics"


def obtener_todo():
    print("Conectando con el calendario de la UTPL...")
    try:
        respuesta = requests.get(ICAL_URL)
        respuesta.raise_for_status()

        gcal = Calendar.from_ical(respuesta.content)
        ahora = datetime.now()

        # Listas para organizar
        pasados = []
        futuros = []

        for componente in gcal.walk():
            if componente.name == "VEVENT":
                titulo = componente.get('summary')
                fecha_entrega = componente.get('dtstart').dt

                # Normalizar la fecha (algunas vienen sin hora)
                if not isinstance(fecha_entrega, datetime):
                    fecha_entrega = datetime.combine(fecha_entrega, datetime.min.time())

                # Quitar zona horaria para comparar si es necesario
                fecha_entrega_naive = fecha_entrega.replace(tzinfo=None)
                ahora_naive = ahora.replace(tzinfo=None)

                evento = {
                    "titulo": titulo,
                    "fecha": fecha_entrega_naive
                }

                if fecha_entrega_naive < ahora_naive:
                    pasados.append(evento)
                else:
                    futuros.append(evento)

        # Mostrar Resultados
        print(f"\n✅ --- EVENTOS PASADOS ({len(pasados)}) ---")
        # Ordenar por fecha más reciente primero
        for ev in sorted(pasados, key=lambda x: x['fecha'], reverse=True):
            print(f"✔️ {ev['fecha'].strftime('%d/%m/%y')} - {ev['titulo']}")

        print(f"\n🚀 --- TAREAS PENDIENTES ({len(futuros)}) ---")
        # Ordenar por fecha más cercana
        for ev in sorted(futuros, key=lambda x: x['fecha']):
            print(f"📌 {ev['fecha'].strftime('%d/%m/%y %H:%M')} - {ev['titulo']}")

    except Exception as e:
        print(f"Hubo un error: {e}")


if __name__ == "__main__":
    obtener_todo()