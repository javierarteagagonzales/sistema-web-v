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


from django.views.decorators.csrf import csrf_exempt




# Create your views here.

#acabados > acabados

def empleado_list_a(request):
    empleados = Empleado.objects.filter(id_area=5).values('nombre')
    return JsonResponse(list(empleados), safe=False)


def datos_list_a(request):
    empleado = request.GET.get('empleado', '')
    query = f"""
    SELECT caja_prenda.id_caja,
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
    
    
#dataview

class MyDataView(View):
    def get(self, request):
        query = '''
        SELECT area.id_area, 
       caja_lote.id_caja, 
       actividad_diaria.fecha_actividad, 
       estado.nombre
FROM registro_transformacion_caja
JOIN caja_lote ON registro_transformacion_caja.id_caja = caja_lote.id_caja
JOIN actividad_diaria ON registro_transformacion_caja.id_actividad = actividad_diaria.id_actividad
JOIN estado ON caja_lote.id_estado = estado.id_estado
JOIN orden_producción ON actividad_diaria.id_orden_producción = orden_producción.id_orden_producción
JOIN area ON orden_producción.id_area = area.id_area
WHERE area.id_area = 5
ORDER BY actividad_diaria.fecha_actividad DESC
LIMIT 10;

        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        data = [
            {
                'id': f"{row[0]}_{row[1]}",  # Combina id_area y id_caja para formar un id único
                'id_area': row[0],
                'id_caja': row[1],
                'fecha_actividad': row[2],
                'nombre': row[3],
            } for row in rows
        ]

        return JsonResponse(data, safe=False)
    
    

def get_caja_salida_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT caja_lote.id_caja, 
       caja_salida.id_salida, 
       caja_salida.fecha_salida::date  
FROM caja_salida
FULL JOIN caja_lote ON caja_salida.id_caja = caja_lote.id_caja
JOIN registro_transformacion_caja ON caja_lote.id_caja = registro_transformacion_caja.id_caja
JOIN actividad_diaria ON registro_transformacion_caja.id_actividad = actividad_diaria.id_actividad
WHERE caja_salida.id_area = 5
ORDER BY actividad_diaria.fecha_actividad;

        """)
        rows = cursor.fetchall()
        
    data = [
        {"id_caja": row[0], "id_salida": row[1], "fecha_salida": row[2]}
        for row in rows
    ]
    
    return JsonResponse(data, safe=False)


#############################################

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_ordenes_produccion(request):
    query = """
    SELECT
        o.id_orden_producción,
        o.fecha_inicio,
        o.fecha_fin,
        o.cantidad,
        e.nombre AS estado_orden,
        a.nombre AS area,
        tc.nombre AS tipo_corte,
        tmp.nombre AS tipo_materia_prima,
        o.id_orden_trabajo,
        o.fecha_creacion
    FROM
        orden_producción o
    JOIN
        estado e ON o.id_estado = e.id_estado
    JOIN
        area a ON o.id_area = a.id_area
    JOIN
        dimension_corte dc ON o.id_dim_corte = dc.id_dim_corte
    JOIN
        parte_corte_detalle pcd ON dc.id_dim_parte_prenda = pcd.id_dim_parte_prenda
    JOIN
        tipo_corte tc ON pcd.id_tipo_corte = tc.id_tipo_corte
    JOIN
        actividad_diaria ad ON o.id_orden_producción = ad.id_orden_producción
    JOIN
        registro_uso_lote rul ON ad.id_actividad = rul.id_actividad
    JOIN
        lote l ON rul.id_lote = l.id_lote
    JOIN
        dimension_materia_prima dmp ON l.id_dim_materia_prima = dmp.id_dim_materia_prima
    JOIN
        tipo_materia_prima tmp ON dmp.id_tipo_materia_prima = tmp.id_tipo_materia_prima
    WHERE
        a.nombre = 'Corte'
    GROUP BY
        o.id_orden_producción, o.fecha_inicio, o.fecha_fin, o.cantidad, e.nombre, a.nombre, tc.nombre, tmp.nombre,       
        o.id_orden_trabajo, o.fecha_creacion
    ORDER BY
        o.fecha_inicio DESC;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = dictfetchall(cursor)
    return JsonResponse(results, safe=False)

@csrf_exempt
def asignar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha_actividad = data['fecha_actividad']
        id_orden_produccion = data['id_orden_produccion']
        id_maquina = data['id_maquina']
        cantidad_hecha = data['cantidad_hecha']

        query1 = "INSERT INTO actividad_diaria (fecha_actividad, id_orden_producción) VALUES (%s, %s) RETURNING id_actividad"
        query2 = "INSERT INTO maquina_actividad (id_actividad, id_maquina, cantidad_hecha) VALUES (%s, %s, %s)"
        
        with connection.cursor() as cursor:
            cursor.execute(query1, [fecha_actividad, id_orden_produccion])
            id_actividad = cursor.fetchone()[0]
            cursor.execute(query2, [id_actividad, id_maquina, cantidad_hecha])
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)




def actividad_diaria(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                a.fecha_actividad,
                o.id_orden_producción,
                o.cantidad AS cantidad_orden,
                m.id_maquina,
                ma.cantidad_hecha AS cantidad_realizar,
                tc.nombre AS tipo_corte
            FROM actividad_diaria a
            JOIN maquina_actividad ma ON a.id_actividad = ma.id_actividad
            JOIN maquina m ON ma.id_maquina = m.id_maquina
            JOIN orden_producción o ON a.id_orden_producción = o.id_orden_producción
            JOIN corte c ON c.id_lote = o.id_dim_corte
            JOIN dimension_corte dc ON c.id_dim_corte = dc.id_dim_corte
            JOIN parte_corte_detalle pcd ON dc.id_dim_parte_prenda = pcd.id_dim_parte_prenda
            JOIN tipo_corte tc ON pcd.id_tipo_corte = tc.id_tipo_corte
            ORDER BY a.fecha_actividad DESC ;
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
    
    return JsonResponse(results, safe=False)




@csrf_exempt
def insertar_datos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        id_tipo_lote = 2  # el valor constante como especificaste
        cantidad = data.get('cantidad')
        id_dim_corte = data.get('id_dim_corte')
        id_estado = data.get('id_estado')
        id_actividad = data.get('id_actividad')
        fecha_creacion = data.get('fecha_creacion')
        cantidad_usada = data.get('cantidad_usada')
        
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO lote (id_tipo_lote, cantidad, id_dim_corte, id_estado, id_dim_confeccion, id_dim_materia_prima, id_actividad, fecha_creacion)
                VALUES (%s, %s, %s, %s, NULL, NULL, %s, %s) RETURNING id;
                ''',
                [id_tipo_lote, cantidad, id_dim_corte, id_estado, id_actividad, fecha_creacion]
            )
            id_lote = cursor.fetchone()[0]
            
            cursor.execute(
                '''
                INSERT INTO Registro_uso_lote (id_actividad, id_lote, cantidad_usada)
                VALUES (%s, %s, %s);
                ''',
                [id_actividad, id_lote, cantidad_usada]
            )
        
        return JsonResponse({'success': True, 'id_lote': id_lote})
    return JsonResponse({'error': 'Invalid request method'}, status=400)