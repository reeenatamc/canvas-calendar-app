import requests
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

# --- CONFIGURACIÓN (Tu Cookie y URL) ---
# He puesto la cookie que usabas en test_v3.py.
# Si caduca, solo actualiza esta variable.
SESSION_COOKIE = "4ryxaDHUUgO-8PgTkIxLCw+hHX2HOpusjgMQeEq4hEBub3zCH4l9SGxtZtCU6NmuIlmqpTXN901Io4RNSGdNcMAM9QzQ3ls7EaCMJH2r_GRIWq7J8CqiZmlcBZHxQFwJuSuI2h18EnU_P76G8_9-28DQE2l_V0oDHUZS10o-i-fQhUTAwca_izUNjxk_D7DBCkTtqBcf16aS8c0-VSASGaEDKWx2E6yL9CVOqKbdEdwT0JoNh2eOfYreqd3J1iQJA9MkLTdFcsNu6hr1O8UhJahUK2pWWYZFJAvVW3gBsyoSdtdBXdKiTjXjtv78cTZ-KhkatHMiy1UmLFLf8YaePjv3i9zexXrB82vKqT3ziUZCx8JSTnbv6zTc_lP2MOhi7trYj1zC_rrilORwvdFjuMavzEJz7ax-bGvaggABVfe1hjHtmpieg-LqeFlUlOppWxSV-cZLHg1Wdm4SVq01axei3t9IjgtI17JZznvhAS-ZCpCT1AHuCJuQIQzNoaNhrvatg3D0S6qng1FLvo75952JJcMENhtq8PMqFOH3_7LqA.PRWYYxeULg5k5nS9f18vWoSRMj4.aVITMg"
URL_PLANNER = "https://utpl.instructure.com/api/v1/planner/items"


# --- LÓGICA DE SINCRONIZACIÓN (Integrada) ---
def sync_canvas_tasks():
    print("🔄 Iniciando sincronización con Canvas...")

    # Rango de fechas: Desde Navidad hasta fin de semestre (Marzo 2026)
    start_date = "2025-12-20T00:00:00Z"
    end_date = "2026-03-30T23:59:59Z"

    params = {
        'start_date': start_date,
        'end_date': end_date,
        'per_page': 100
    }

    cookies = {"canvas_session": SESSION_COOKIE}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        response = requests.get(URL_PLANNER, params=params, cookies=cookies, headers=headers)

        if response.status_code != 200:
            return False, f"Error Canvas: {response.status_code}"

        items = response.json()
        count_nuevas = 0

        for item in items:
            # 1. Filtramos solo lo importante (Tareas, Quices, Foros)
            tipo = item.get('plannable_type')
            if tipo not in ['assignment', 'quiz', 'discussion_topic']:
                continue

            plannable = item.get('plannable', {})
            canvas_id = str(plannable.get('id'))

            # 2. Verificar si está completado en Canvas
            info_entrega = item.get('submissions')
            esta_completado_canvas = item.get('completed', False)

            ya_entregado = False
            if isinstance(info_entrega, dict):
                ya_entregado = info_entrega.get('submitted') or info_entrega.get('graded')
            elif isinstance(info_entrega, bool):
                ya_entregado = info_entrega

            # El estado final es: O Canvas dice que está lista, O ya la entregaste
            final_status = esta_completado_canvas or ya_entregado

            # 3. Guardar en Base de Datos (Upsert)
            # update_or_create: Si existe actualiza, si no crea.
            obj, created = Task.objects.update_or_create(
                canvas_id=canvas_id,
                defaults={
                    'title': plannable.get('title', 'Sin título'),
                    'due_date': parse_datetime(plannable.get('due_at')) if plannable.get('due_at') else None,
                    'platform_type': tipo,
                    # IMPORTANTE: Si Canvas dice que está hecha, la marcamos hecha.
                    # Si Canvas dice que NO, respetamos si tú la marcaste hecha localmente.
                    # (Lógica: True de Canvas sobrescribe False local, pero no al revés necesariamente)
                }
            )

            # Si Canvas dice que está hecha, actualizamos el modelo
            if final_status:
                obj.is_completed = True
                obj.save()

            if created:
                count_nuevas += 1

        return True, f"Sincronización exitosa. {count_nuevas} tareas nuevas detectadas."

    except Exception as e:
        return False, f"Error de conexión: {str(e)}"


# --- VISTAS DE LA API ---

class TaskListView(APIView):
    """
    GET: Devuelve la lista de tareas ordenadas por fecha.
    """

    def get(self, request):
        # Ordenar: Primero las pendientes (is_completed=False), luego por fecha
        tasks = Task.objects.all().order_by('is_completed', 'due_date')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class SyncView(APIView):
    """
    GET/POST: Fuerza la sincronización con Canvas.
    """

    def get(self, request):
        return self._run_sync()

    def post(self, request):
        return self._run_sync()

    def _run_sync(self):
        success, message = sync_canvas_tasks()
        if success:
            return Response(
                {"status": "success", "message": "✅ " + message},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "error", "message": "❌ " + message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )