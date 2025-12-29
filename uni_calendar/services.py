import requests
from django.utils.dateparse import parse_datetime
from django.conf import settings
from .models import Task

# Mueve esto a un archivo .env en el futuro
SESSION_COOKIE = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"
URL_PLANNER = "https://utpl.instructure.com/api/v1/planner/items"


def sync_canvas_tasks():
    print("🔄 Iniciando sincronización inteligente...")

    # Definir rango de fechas (como lo hiciste en tu script)
    start_date = "2025-12-20T00:00:00Z"
    end_date = "2026-03-30T23:59:59Z"

    params = {
        'start_date': start_date,
        'end_date': end_date,
        'per_page': 100
    }

    cookies = {"canvas_session": SESSION_COOKIE}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(URL_PLANNER, params=params, cookies=cookies, headers=headers)
        response.raise_for_status()
        items = response.json()

        for item in items:
            # Filtro de tipos
            if item.get('plannable_type') not in ['assignment', 'quiz', 'discussion_topic']:
                continue

            plannable = item.get('plannable', {})
            canvas_id = str(plannable.get('id'))

            # Lógica de completado (Traída de tu script v3)
            info_entrega = item.get('submissions', {})
            esta_completado_canvas = item.get('completed', False)

            ya_entregado = False
            if isinstance(info_entrega, dict):
                ya_entregado = info_entrega.get('submitted') or info_entrega.get('graded')
            elif isinstance(info_entrega, bool):
                ya_entregado = info_entrega

            final_status = esta_completado_canvas or ya_entregado

            # Upsert (Actualizar si existe, Crear si no)
            Task.objects.update_or_create(
                canvas_id=canvas_id,
                defaults={
                    'title': plannable.get('title', 'Sin título'),
                    'due_date': parse_datetime(plannable.get('due_at')) if plannable.get('due_at') else None,
                    'platform_type': item.get('plannable_type'),
                    # Solo marcamos como completado si Canvas dice que sí.
                    # Si Canvas dice "No", respetamos si tú lo marcaste "Sí" localmente.
                    'is_completed': final_status
                }
            )
        return True, "Sincronización completada"

    except Exception as e:
        return False, str(e)