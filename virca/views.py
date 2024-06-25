from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Acabado
from django.db import connection
from django.http import JsonResponse

# views.py
from django.http import JsonResponse
from django.views import View
from django.db import connection
from .models import Empleado





# Create your views here.

#acabados > acabados

def empleado_list_a(request):
    empleados = Empleado.objects.filter(id_area=5).values('nombre')
    return JsonResponse(list(empleados), safe=False)


def datos_list_a(request):
    empleado = request.GET.get('empleado', '')
    query = f"""
    SELECT DISTINCT(caja_prenda.id_caja) AS ID_Caja, 
       empleado.nombre, 
       caja_prenda.cantidad,
       guia_confeccion.id_guia_confeccion AS ID_guia, 
       tipo_prenda.nombre AS tipo_prenda, 
       estilo_prenda.nombre AS estilo_prenda, 
       talla.nombre AS talla, 
       genero.nombre AS genero,
       COALESCE(guia_confeccion.medida_longitud::text, ' ') AS ml,
       COALESCE(guia_confeccion.medida_hombro::text, ' ') AS mh,
       COALESCE(guia_confeccion.medida_pecho::text, ' ') AS mp,
       COALESCE(guia_confeccion.medida_manga::text, ' ') AS mm,
       COALESCE(guia_confeccion.medida_cintura::text, ' ') AS mc,
       COALESCE(guia_confeccion.medida_cadera::text, ' ') AS mca,
       COALESCE(guia_confeccion.medida_muslo::text, ' ') AS mmu
    FROM dimension_confeccion 
    JOIN guia_confeccion ON dimension_confeccion.id_guia_confeccion = guia_confeccion.id_guia_confeccion
    JOIN tipo_prenda ON dimension_confeccion.id_tipo_prenda = tipo_prenda.id_tipo_prenda
    JOIN estilo_prenda ON dimension_confeccion.id_estilo_prenda = estilo_prenda.id_estilo_prenda
    JOIN talla ON dimension_confeccion.id_talla = talla.id_talla
    JOIN genero ON dimension_confeccion.id_genero = genero.id_genero
    JOIN dimension_prenda ON dimension_confeccion.id_dim_confeccion = dimension_prenda.id_dim_confeccion
    JOIN caja_prenda ON dimension_prenda.id_dim_prenda = caja_prenda.id_dim_prenda
    JOIN prenda ON caja_prenda.id_caja = prenda.id_caja
    JOIN empleado ON prenda.id_empleado = empleado.id_empleado
    WHERE empleado.nombre = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [empleado])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    return JsonResponse(result, safe=False)

#############


#Reporte

class ReporteAcabadosView(View):
    def get(self, request):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        query = """
        SELECT DISTINCT e.id_empleado, e.nombre, e.primer_apellido,
                        e.segundo_apellido, e.id_correo, e.dni, e.id_cargo,
                        caja_prenda.id_caja, caja_prenda.fecha_creacion,
                        tipo_prenda.nombre 
        FROM empleado e
        JOIN prenda ON e.id_empleado = prenda.id_empleado
        JOIN caja_prenda ON prenda.id_caja = caja_prenda.id_caja
        JOIN dimension_prenda ON caja_prenda.id_dim_prenda = dimension_prenda.id_dim_prenda
        JOIN dimension_confeccion ON dimension_prenda.id_dim_confeccion = dimension_confeccion.id_dim_confeccion
        JOIN guia_confeccion ON dimension_confeccion.id_guia_confeccion = guia_confeccion.id_guia_confeccion
        JOIN tipo_prenda ON dimension_confeccion.id_tipo_prenda = tipo_prenda.id_tipo_prenda
        WHERE id_area=5 AND id_cargo=2
        AND caja_prenda.fecha_creacion BETWEEN %s AND %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [fecha_inicio, fecha_fin])
            rows = cursor.fetchall()

        resultados = [
            {
                "id_empleado": row[0],
                "nombre": row[1],
                "primer_apellido": row[2],
                "segundo_apellido": row[3],
                "id_correo": row[4],
                "dni": row[5],
                "id_cargo": row[6],
                "id_caja": row[7],
                "fecha_creacion": row[8],
                "tipo_prenda": row[9],
            }
            for row in rows
        ]

        return JsonResponse(resultados, safe=False)
    
    
    
    
    

class EmpleadoListView(View):
    def get(self, request):
         with connection.cursor() as cursor:
            cursor.execute("SELECT id_empleado, nombre FROM empleado WHERE id_area = 5")
            rows = cursor.fetchall()
            result = [
                    {'id_empleado': row[0], 'nombre': row[1]}
                    for row in rows
                ]
            return JsonResponse(result, safe=False)



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