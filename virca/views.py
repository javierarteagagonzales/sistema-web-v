from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Acabado
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def empleados_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre FROM empleado WHERE id_area = 5")
        rows = cursor.fetchall()
        empleados = [{'nombre': row[0]} for row in rows]
    return JsonResponse(empleados, safe=False)


class AcabadoViewSet(viewsets.ModelViewSet):
    queryset = Acabado.objects.all()
    serializer_class = AcabadoSerializer


class AcabadoListView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_acabado, nombre FROM acabado")
            data = cursor.fetchall()
        
        # Formatear los resultados en un diccionario
        resultados = [{'id_acabado': row[0], 'nombre': row[1]} for row in data]

        return Response(resultados)
    


def get_lote_entrada_vista(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT le.id_entrada, le.fecha_entrada, l.id_tipo_lote, l.cantidad, dc.id_dim_confeccion, dc.id_guia_confeccion
            FROM lote_entrada le
            JOIN lote l ON le.id_lote = l.id_lote
            JOIN dimension_confeccion dc ON l.id_dim_confeccion = dc.id_dim_confeccion
            LIMIT 200;
        """)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(results, safe=False)