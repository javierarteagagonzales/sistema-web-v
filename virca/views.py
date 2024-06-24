from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado
from django.views import View
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



class CajaPrendaListView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT cp.id_caja, tp.nombre, cp.cantidad, cp.fecha_creacion, e.nombre, dc.id_dim_confeccion, gc.id_guia_confeccion
                FROM caja_prenda cp
                JOIN estado e ON cp.id_estado = e.id_estado
                JOIN dimension_prenda dp ON cp.id_dim_prenda = dp.id_dim_prenda
                JOIN dimension_confeccion dc ON dp.id_dim_confeccion = dc.id_dim_confeccion
                JOIN guia_confeccion gc ON dc.id_guia_confeccion = gc.id_guia_confeccion
                JOIN tipo_prenda tp ON dc.id_tipo_prenda = tp.id_tipo_prenda
                ORDER BY cp.fecha_creacion DESC
            ''')
            rows = cursor.fetchall()

            result = [
                {
                    'id_caja': row[0],
                    'tipo_prenda': row[1],
                    'cantidad': row[2],
                    'fecha_creacion': row[3],
                    'estado': row[4],
                    'id_dim_confeccion': row[5],
                    'id_guia_confeccion': row[6]
                }
                for row in rows
            ]

        return JsonResponse(result, safe=False)

class CajaPrendaDetailView(View):
    def get(self, request, id_caja):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT cp.id_caja, tp.nombre, cp.cantidad, cp.fecha_creacion, e.nombre, dc.id_dim_confeccion, gc.id_guia_confeccion
                FROM caja_prenda cp
                JOIN estado e ON cp.id_estado = e.id_estado
                JOIN dimension_prenda dp ON cp.id_dim_prenda = dp.id_dim_prenda
                JOIN dimension_confeccion dc ON dp.id_dim_confeccion = dc.id_dim_confeccion
                JOIN guia_confeccion gc ON dc.id_guia_confeccion = gc.id_guia_confeccion
                JOIN tipo_prenda tp ON dc.id_tipo_prenda = tp.id_tipo_prenda
                WHERE cp.id_caja = %s
            ''', [id_caja])
            row = cursor.fetchone()

            if row:
                result = {
                    'id_caja': row[0],
                    'tipo_prenda': row[1],
                    'cantidad': row[2],
                    'fecha_creacion': row[3],
                    'estado': row[4],
                    'id_dim_confeccion': row[5],
                    'id_guia_confeccion': row[6]
                }
            else:
                result = {}

        return JsonResponse(result)