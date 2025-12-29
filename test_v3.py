# import requests
# import json
#
# # Tu cookie de sesión (la que pegaste)
# CANVAS_SESSION = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"
#
# url = "https://utpl.instructure.com/api/v1/users/self/todo"
#
# # Es importante mandar los headers para que no sospechen
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }
#
# cookies = {
#     "canvas_session": CANVAS_SESSION
# }
#
# print("Consultando la lista de To-Do...")
# response = requests.get(url, headers=headers, cookies=cookies)
#
# if response.status_code == 200:
#     tareas = response.json()
#     print(f"Se encontraron {len(tareas)} items en tu To-Do.\n")
#
#     for item in tareas:
#         # Aquí está el truco: buscamos el objeto 'assignment'
#         tarea = item.get('assignment', {})
#         titulo = tarea.get('name', 'Sin título')
#
#         # El estado de la entrega está en 'submission'
#         submission = item.get('submission', {})
#         completada = submission.get('workflow_state')  # Puede ser 'unsubmitted', 'submitted', 'graded'
#
#         icon = "✅" if completada in ['submitted', 'graded'] else "❌"
#
#         print(f"{icon} {titulo}")
#         print(f"   Estado: {completada}")
#         print("-" * 40)
# else:
#     print(f"Error: {response.status_code}")
#     print("Es posible que la cookie haya expirado o sea incorrecta.")

# import requests
# import json
# from datetime import datetime
#
# # 1. CONFIGURACIÓN
# SESSION_COOKIE = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"
# URL = "https://utpl.instructure.com/api/v1/planner/items"
#
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept": "application/json"
# }
#
# COOKIES = {"canvas_session": SESSION_COOKIE}
#
#
# def sync_canvas():
#     print(f"--- Iniciando Sincronización UTPL ({datetime.now().strftime('%H:%M:%S')}) ---")
#
#     try:
#         response = requests.get(URL, headers=HEADERS, cookies=COOKIES)
#
#         if response.status_code != 200:
#             print(f"❌ Error {response.status_code}: Revisa tu sesión.")
#             return
#
#         items = response.json()
#         print(f"Se encontraron {len(items)} items en el calendario.\n")
#
#         for item in items:
#             plannable = item.get('plannable', {})
#             titulo = plannable.get('title', 'Sin título')
#             tipo = item.get('plannable_type', 'evento')
#
#             # 1. Chequeamos el flag principal de completado
#             esta_completado = item.get('completed', False)
#
#             # 2. Manejo robusto de 'submissions' (aquí estaba el error)
#             info_entrega = item.get('submissions')
#             ya_entregado = False
#
#             # Si es un diccionario, buscamos las llaves 'submitted' o 'graded'
#             if isinstance(info_entrega, dict):
#                 ya_entregado = info_entrega.get('submitted') or info_entrega.get('graded')
#             # Si es un booleano (a veces pasa), lo usamos directamente
#             elif isinstance(info_entrega, bool):
#                 ya_entregado = info_entrega
#
#             # Fecha de vencimiento
#             fecha_raw = plannable.get('due_at') or plannable.get('todo_date')
#             if fecha_raw:
#                 try:
#                     fecha_dt = datetime.strptime(fecha_raw, "%Y-%m-%dT%H:%M:%SZ")
#                     fecha_str = fecha_dt.strftime("%d/%m/%Y %H:%M")
#                 except:
#                     fecha_str = fecha_raw
#             else:
#                 fecha_str = "Evento/Feriado"
#
#             # Lógica de icono
#             if esta_completado or ya_entregado:
#                 icono = "✅ HECHA"
#             else:
#                 icono = "❌ PENDIENTE"
#
#             print(f"{icono} | {titulo}")
#             print(f"   📅 Vence: {fecha_str} | 📂 Tipo: {tipo}")
#             print("-" * 50)
#
#     except Exception as e:
#         print(f"Ocurrió un error inesperado: {e}")
#
#
# if __name__ == "__main__":
#     sync_canvas()

# import requests
# from datetime import datetime
#
# # 1. CONFIGURACIÓN
# SESSION_COOKIE = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"
#
# # Definimos el rango del semestre (Octubre 2025 a Marzo 2026)
# START_DATE = "2025-10-01T00:00:00Z"
# END_DATE = "2026-03-01T23:59:59Z"
#
# # Agregamos los parámetros a la URL
# URL = f"https://utpl.instructure.com/api/v1/planner/items?start_date={START_DATE}&end_date={END_DATE}"
#
# COOKIES = {"canvas_session": SESSION_COOKIE}
# HEADERS = {"User-Agent": "Mozilla/5.0"}
#
#
# def obtener_tareas_reales():
#     print(f"--- Buscando tareas del semestre ({datetime.now().strftime('%H:%M:%S')}) ---")
#
#     try:
#         response = requests.get(URL, cookies=COOKIES, headers=HEADERS)
#         if response.status_code != 200:
#             print(f"❌ Error {response.status_code}. Revisa la cookie.")
#             return
#
#         items = response.json()
#         encontradas = 0
#
#         for item in items:
#             # FILTRO CLAVE: Solo queremos tareas y cuestionarios
#             tipo = item.get('plannable_type')
#             if tipo not in ['assignment', 'quiz', 'discussion_topic']:
#                 continue
#
#             plannable = item.get('plannable', {})
#             titulo = plannable.get('title', 'Sin título')
#             fecha_vence = plannable.get('due_at')
#
#             # Verificamos estado
#             info_entrega = item.get('submissions', {})
#             esta_completado = item.get('completed', False)
#
#             # Si es un dict, vemos si se envió
#             ya_entregado = False
#             if isinstance(info_entrega, dict):
#                 ya_entregado = info_entrega.get('submitted') or info_entrega.get('graded')
#
#             if esta_completado or ya_entregado:
#                 icono = "✅ HECHA"
#             else:
#                 icono = "❌ PENDIENTE"
#
#             print(f"{icono} | {titulo}")
#             if fecha_vence:
#                 fecha_dt = datetime.strptime(fecha_vence, "%Y-%m-%dT%H:%M:%SZ")
#                 print(f"   📅 Vence: {fecha_dt.strftime('%d/%m/%Y %H:%M')}")
#             print("-" * 50)
#             encontradas += 1
#
#         if encontradas == 0:
#             print("No se encontraron tareas en este rango de fechas.")
#             print("Prueba ajustando START_DATE y END_DATE en el código.")
#
#     except Exception as e:
#         print(f"Error: {e}")
#
#
# if __name__ == "__main__":
#     obtener_tareas_reales()
#

import requests
from datetime import datetime

# 1. CONFIGURACIÓN
SESSION_COOKIE = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"

# Hoy es 29 de diciembre. Vamos a buscar desde Navidad hasta el final del ciclo.
START_DATE = "2025-12-20T00:00:00Z"
END_DATE = "2026-03-30T23:59:59Z"

# Agregamos per_page=100 para que no se nos escape nada
URL = f"https://utpl.instructure.com/api/v1/planner/items?start_date={START_DATE}&end_date={END_DATE}&per_page=100"

COOKIES = {"canvas_session": SESSION_COOKIE}
HEADERS = {"User-Agent": "Mozilla/5.0"}


def obtener_tareas_pendientes():
    print(f"--- 🚀 BUSCANDO TAREAS PENDIENTES (Rango: Dic-Mar) ---")

    try:
        response = requests.get(URL, cookies=COOKIES, headers=HEADERS)
        items = response.json()

        tareas_lista = []

        for item in items:
            tipo = item.get('plannable_type')
            # Solo nos interesan las que tienen nota
            if tipo in ['assignment', 'quiz', 'discussion_topic']:
                plannable = item.get('plannable', {})

                # Estado de entrega
                info_entrega = item.get('submissions')
                esta_completado = item.get('completed', False)
                ya_entregado = False
                if isinstance(info_entrega, dict):
                    ya_entregado = info_entrega.get('submitted') or info_entrega.get('graded')

                # Solo añadir a la lista si NO está hecha (esto es lo que "debes hacer")
                if not esta_completado and not ya_entregado:
                    tareas_lista.append({
                        "titulo": plannable.get('title'),
                        "fecha": plannable.get('due_at'),
                        "tipo": tipo
                    })

        # Imprimir resultados ordenados por fecha
        if not tareas_lista:
            print("¡Felicidades! No tienes tareas pendientes en el sistema para este rango.")
        else:
            for t in sorted(tareas_lista, key=lambda x: x['fecha'] if x['fecha'] else ""):
                fecha_dt = datetime.strptime(t['fecha'], "%Y-%m-%dT%H:%M:%SZ")
                print(f"❌ PENDIENTE | {t['titulo']}")
                print(f"   📅 Vence: {fecha_dt.strftime('%d/%m/%Y %H:%M')} | 📂 {t['tipo']}")
                print("-" * 55)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    obtener_tareas_pendientes()