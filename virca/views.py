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
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.shortcuts import render
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



class ProductionOrderView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    op.id_orden_producción,
                    op.cantidad,
                    l.id_lote,
                    l.cantidad AS cantidad_lote,
                    tc.nombre AS tipo_corte,
                    COUNT(c.id_corte) AS cantidad_cortes,
                    e.nombre AS estado_orden,
                    (SELECT
                        (SUM(l2.cantidad) / op.cantidad) * 100
                     FROM lote l2
                     INNER JOIN corte c2 ON l2.id_lote = c2.id_lote
                     INNER JOIN orden_producción op2 ON op2.id_dim_corte = c2.id_dim_corte
                     WHERE op2.id_orden_producción = op.id_orden_producción) AS progreso_produccion
                FROM orden_producción op
                INNER JOIN estado e ON op.id_estado = e.id_estado
                INNER JOIN dimension_corte dc ON op.id_dim_corte = dc.id_dim_corte
                INNER JOIN corte c ON dc.id_dim_corte = c.id_dim_corte
                INNER JOIN lote l ON c.id_lote = l.id_lote
                INNER JOIN parte_corte_detalle pcd ON dc.id_dim_parte_prenda = pcd.id_dim_parte_prenda
                INNER JOIN tipo_corte tc ON pcd.id_tipo_corte = tc.id_tipo_corte
                GROUP BY
                    op.id_orden_producción,
                    op.cantidad,
                    l.id_lote,
                    l.cantidad,
                    tc.nombre,
                    e.nombre
                ORDER BY
                    op.id_orden_producción,
                    tc.nombre,
                    cantidad_cortes DESC;
            """)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]

        return JsonResponse(data, safe=False)
    
    
    
    
class LotesViewC(View):
    def get(self, request):
        query = """
            SELECT 
                l.fecha_creacion::date AS dia,
                COUNT(l.id_lote) AS cantidad_lotes
            FROM 
                lote l
            JOIN 
                actividad_diaria ad ON l.id_actividad = ad.id_actividad
            JOIN 
                orden_producción op ON ad.id_orden_producción = op.id_orden_producción
            JOIN 
                area a ON op.id_area = a.id_area
            WHERE 
                a.nombre = 'Corte'
                AND DATE_TRUNC('month', l.fecha_creacion) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY 
                l.fecha_creacion::date
            ORDER BY 
                dia DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        data = [{'dia': row[0], 'cantidad_lotes': row[1]} for row in rows]
        return JsonResponse(data, safe=False)
    
    #
    
    

def get_activities(request):
    query = """
        SELECT 
            ma.id_maquina,
            m.capacidad_total,
            COUNT(ad.id_actividad) AS cantidad_actividades,
            ad.fecha_actividad
        FROM 
            actividad_diaria ad
        JOIN 
            maquina_actividad ma ON ad.id_actividad = ma.id_actividad
        JOIN 
            maquina m ON ma.id_maquina = m.id_maquina

        GROUP BY 
            ma.id_maquina, m.capacidad_total, ad.fecha_actividad
        ORDER BY 
            ad.fecha_actividad DESC;
            
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    
    data = [
        {
            "id_maquina": row[0],
            "capacidad_total": row[1],
            "cantidad_actividades": row[2],
            "fecha_actividad": row[3]
        } for row in result
    ]
    
    return JsonResponse(data, safe=False)

def get_activity_details(request, id_actividad):
    query = """
        SELECT
            ad.id_actividad,
            ad.fecha_actividad,
            COUNT(c.id_corte) AS cantidad_cortes,
            op.cantidad AS cantidad_orden_preproduccion,
            (SUM(l.cantidad) / op.cantidad) * 100 AS progreso_preproduccion
        FROM actividad_diaria ad
        JOIN orden_producción op ON ad.id_orden_producción = op.id_orden_producción
        JOIN lote l ON ad.id_actividad = l.id_actividad
        JOIN corte c ON l.id_lote = c.id_lote
        WHERE ad.id_actividad = %s
        GROUP BY
            ad.id_actividad,
            ad.fecha_actividad,
            op.cantidad
        ORDER BY
            ad.fecha_actividad DESC;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [id_actividad])
        result = cursor.fetchall()
    
    data = [
        {
            "id_actividad": row[0],
            "fecha_actividad": row[1],
            "cantidad_cortes": row[2],
            "cantidad_orden_preproduccion": row[3],
            "progreso_preproduccion": row[4]
        } for row in result
    ]
    
    return JsonResponse(data, safe=False)



#####################################################################################
###################################################################################
## CALIDAD


def dictfetchalla(cursor):
    "Retorna todas las filas de un cursor como un diccionario"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_inspeccionescal(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT
                OP2.ID_ORDEN_PRODUCCIÓN,
                I.ID_INSPECCION,
                I.ID_LOTE,
                I.FECHA_INSPECCION::date,
                I.ID_AQL_LOTE_RANGO,
                I.CANTIDAD_DEFECTUOSOS,
                I.ID_AQL_CODIGO,
                I.ID_AQL_NIVEL,
                I.ID_AQL_SIGNIFICANCIA,
                I.ID_ESTADO,
                I.ID_RESULTADO
            FROM
                INSPECCION_CALIDAD I
                JOIN LOTE LT ON I.ID_LOTE = LT.ID_LOTE
                JOIN ACTIVIDAD_DIARIA ad ON LT.ID_ACTIVIDAD = ad.ID_ACTIVIDAD
                JOIN ORDEN_PRODUCCIÓN OP2 ON ad.ID_ORDEN_PRODUCCIÓN = OP2.ID_ORDEN_PRODUCCIÓN
            ORDER BY OP2.ID_ORDEN_PRODUCCIÓN DESC;
        ''')
        rows = dictfetchalla(cursor)
    return JsonResponse(rows, safe=False)

def get_ordenes_produccioncal(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT
                ID_ORDEN_PRODUCCIÓN
            FROM
                ORDEN_PRODUCCIÓN
            ORDER BY ID_ORDEN_PRODUCCIÓN DESC;
        ''')
        rows = dictfetchalla(cursor)
    return JsonResponse(rows, safe=False)


###################################################################
##########################################################################333333
# ALMACÉN CENTRAL

class LoteListView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        estado = data.get('estado', None)
        tipo_materia_prima = data.get('tipo_materia_prima', None)
        query = """
            SELECT    
                l.id_lote, 
                p.denominacion_social,
                e.id_espacio,
                le.fecha_entrada,
                tmp.nombre as tipo_materia_prima
            FROM lote l
            JOIN materia_prima mp ON l.id_lote = mp.id_lote
            JOIN proveedor p on mp.id_proveedor = p.id_proveedor
            JOIN espacio e on l.id_lote = e.id_lote
            JOIN lote_entrada le on l.id_lote = le.id_lote
            join estado e2 on l.id_estado = e2.id_estado
            join dimension_materia_prima dmp on mp.id_dim_materia_prima = dmp.id_dim_materia_prima
            join tipo_materia_prima tmp ON dmp.id_tipo_materia_prima =tmp.id_tipo_materia_prima 
            WHERE e2.nombre = %s
        """
        params = [estado]
        if tipo_materia_prima is not None:
            query += " AND tmp.nombre = %s"
            params.append(tipo_materia_prima)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    'id_lote': row[0],
                    'denominacion_social': row[1],
                    'id_espacio': row[2],
                    'fecha_entrada': row[3],
                    'tipo_materia_prima': row[4],
                })
        return JsonResponse(result, safe=False)

class LotesEntreFechasView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin', None)
        with connection.cursor() as cursor:
            cursor.callproc('get_lotes_entre_fechas', [fecha_inicio, fecha_fin])
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    'fecha_entrada': row[0],
                    'id_lote': row[1],
                    'id_estanteria': row[2],
                    'id_espacio': row[3],
                    'denominacion_social': row[4],
                    'id_materia_prima': row[5],
                })
        return JsonResponse(result, safe=False)

    
class ProveedorMateriaPrimaView(View):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        denominacion_social = data.get('denominacion_social', None)
        nombre = data.get('nombre', None)
        
        query = """
            SELECT 
                tmp.nombre AS materia_prima,
                p.denominacion_social AS proveedor,
                COUNT(*) AS cantidad_lotes
            FROM 
                proveedor p
            JOIN materia_prima mp ON p.id_proveedor = mp.id_proveedor
            JOIN lote l ON mp.id_lote = l.id_lote
            JOIN dimension_materia_prima dmp ON mp.id_dim_materia_prima = dmp.id_dim_materia_prima
            JOIN tipo_materia_prima tmp ON dmp.id_tipo_materia_prima = tmp.id_tipo_materia_prima
            WHERE l.id_estado = 12
            group by tmp.nombre,p.denominacion_social ;
        """
        
        params = []
        if denominacion_social:
            query += " AND p.denominacion_social = %s"
            params.append(denominacion_social)
        if nombre:
            query += " AND tmp.nombre = %s"
            params.append(nombre)
        
        query += " GROUP BY tmp.nombre, p.denominacion_social"
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = [{'materia_prima': row[0], 'proveedor': row[1], 'cantidad_lotes': row[2]} for row in rows]
        
        return JsonResponse(result, safe=False)

class ProveedorDropdownView(View):
    def get(self, request, *args, **kwargs):
        query = "SELECT denominacion_social FROM proveedor"
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            result = [{'denominacion_social': row[0]} for row in rows]
        return JsonResponse(result, safe=False)

class MateriaPrimaDropdownView(View):
    def get(self, request, *args, **kwargs):
        query = "SELECT nombre FROM tipo_materia_prima"
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            result = [{'nombre': row[0]} for row in rows]
        return JsonResponse(result, safe=False) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

class LotesEntradaView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        fecha_entrada = data.get('fecha_entrada')
        nombre_material = data.get('nombre_material', None)
        nombre_proveedor = data.get('nombre_proveedor', None)
        query = """
            SELECT 
                le.fecha_entrada, 
                l.id_lote, 
                tmp.nombre AS nombre_material, 
                p.denominacion_social AS nombre_proveedor, 
                l.cantidad 
            FROM lote_entrada le 
            JOIN lote l ON le.id_lote = l.id_lote 
            JOIN materia_prima mp ON l.id_lote = mp.id_lote 
            JOIN dimension_materia_prima dmp ON mp.id_dim_materia_prima = dmp.id_dim_materia_prima 
            JOIN tipo_materia_prima tmp ON dmp.id_tipo_materia_prima = tmp.id_tipo_materia_prima 
            JOIN proveedor p ON mp.id_proveedor = p.id_proveedor 
            WHERE DATE(le.fecha_entrada) = DATE(%s)
        """
        params = [fecha_entrada]
        if nombre_material is not None:
            query += " AND tmp.nombre = %s"
            params.append(nombre_material)
        if nombre_proveedor is not None:
            query += " AND p.denominacion_social = %s"
            params.append(nombre_proveedor)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    'fecha_entrada': row[0],
                    'id_lote': row[1],
                    'nombre_material': row[2],
                    'nombre_proveedor': row[3],
                    'cantidad': row[4],
                })
        return JsonResponse(result, safe=False)

class LotesSalidaView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        fecha_salida = data.get('fecha_salida')
        nombre_material = data.get('nombre_material', None)
        nombre_proveedor = data.get('nombre_proveedor', None)
        query = """
            SELECT
                ls.fecha_salida,
                l.id_lote,
                tmp.nombre AS nombre_material,
                p.denominacion_social AS nombre_proveedor,
                l.cantidad,
                a.nombre AS nombre_area
            FROM lote_salida ls
            JOIN lote l ON ls.id_lote = l.id_lote
            JOIN materia_prima mp ON l.id_lote = mp.id_lote
            JOIN dimension_materia_prima dmp ON mp.id_dim_materia_prima = dmp.id_dim_materia_prima
            JOIN tipo_materia_prima tmp ON dmp.id_tipo_materia_prima = tmp.id_tipo_materia_prima
            JOIN proveedor p ON mp.id_proveedor = p.id_proveedor
            JOIN area a ON ls.area_envio = a.id_area
            WHERE DATE(ls.fecha_salida) = DATE(%s)
        """
        params = [fecha_salida]
        if nombre_material is not None:
            query += " AND tmp.nombre = %s"
            params.append(nombre_material)
        if nombre_proveedor is not None:
            query += " AND p.denominacion_social = %s"
            params.append(nombre_proveedor)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append({
                    'fecha_salida': row[0],
                    'id_lote': row[1],
                    'nombre_material': row[2],
                    'nombre_proveedor': row[3],
                    'cantidad': row[4],
                    'nombre_area': row[5],
                })
        return JsonResponse(result, safe=False)

class CrearProveedorView(APIView):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        _descripcion_direccion = data.get('_descripcion_direccion')
        _direccion_correo = data.get('_direccion_correo')
        _numero_telefono = data.get('_numero_telefono')
        _ruc = data.get('_ruc')
        _denominacion_social = data.get('_denominacion_social')
        with connection.cursor() as cursor:
            cursor.execute("CALL crear_proveedor(%s, %s, %s, %s, %s)", [_descripcion_direccion, _direccion_correo, _numero_telefono, _ruc, _denominacion_social])
        return JsonResponse({"message": "Proveedor creado exitosamente"}, status=201)