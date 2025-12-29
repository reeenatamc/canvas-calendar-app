import requests
from icalendar import Calendar
from datetime import datetime

# Tu URL de la UTPL
ICAL_URL = "https://utpl.instructure.com/feeds/calendars/user_YJtudqZ7BdUOKqyPp98Tc2ffrYPgb37BquKYN32c.ics"


def obtener_tareas_utpl():
    print("Conectando con el calendario de la UTPL...")
    try:
        respuesta = requests.get(ICAL_URL)
        respuesta.raise_for_status()  # Verifica que la descarga fue exitosa

        gcal = Calendar.from_ical(respuesta.content)
        print(f"--- TAREAS PENDIENTES ---")

        encontradas = 0
        for componente in gcal.walk():
            if componente.name == "VEVENT":
                titulo = componente.get('summary')
                fecha_entrega = componente.get('dtstart').dt

                # Comprobar si es fecha (algunos eventos son todo el día)
                if isinstance(fecha_entrega, datetime):
                    ahora = datetime.now(fecha_entrega.tzinfo)
                    if fecha_entrega > ahora:
                        print(f"\n📌 Tarea: {titulo}")
                        print(f"📅 Entrega: {fecha_entrega.strftime('%d/%m/%Y %H:%M')}")
                        encontradas += 1

        if encontradas == 0:
            print("No se encontraron tareas próximas. ¡Estás al día!")

    except Exception as e:
        print(f"Hubo un error: {e}")


if __name__ == "__main__":
    obtener_tareas_utpl()