from django.urls import path, include
# from rest_framework import routers
#from virca import views
from .views import AcabadoViewSet
from rest_framework.routers import DefaultRouter
from . import views
from .views import AcabadoListView
from .views import get_lote_entrada_vista
from .views import ReporteAcabadosView
from .views import MyDataView
from .views import get_caja_salida_data
from .views import insertar_datos
from .views import ProductionOrderView
router = DefaultRouter()
router.register(r'acabado', AcabadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cajas/', views.CajaPrendaListView.as_view(), name='caja_prenda_list'),
    path('cajas/<int:id_caja>/', views.CajaPrendaDetailView.as_view(), name='caja_prenda_detail'),
   path('acabadoreporte/', ReporteAcabadosView.as_view(), name='reporte_acabados'),

    path('empleados/',views.EmpleadoListView.as_view(), name='empleado_list'),
    path('acabados/', AcabadoListView.as_view(), name='acabados-list'),
    path('lote-entrada-vista/', get_lote_entrada_vista, name='lote-entrada-vista'),
    
    # acabados acabados
 path('empleadosa/', views.empleado_list_a, name='empleado_list_a'),

    path('datosa/', views.datos_list_a, name='datos_list_a'),
    path('data/', MyDataView.as_view(), name='data-view'),
    path('caja_salida/', views.get_caja_salida_data, name='get_caja_salida_data'),
    
     # almacen
     
     #corte
     
path('ordenes-produccion/', views.get_ordenes_produccion, name='get_ordenes_produccion'),
path('asignar/', views.asignar, name='asignar'),

path('actividad-diaria/', views.actividad_diaria, name='actividad_diaria'),

path('insertar/', insertar_datos, name='insertar_datos'),
path('production-orders/', ProductionOrderView.as_view(), name='production_orders'),

     path('lotesC1/', views.LotesViewC.as_view(), name='lotes'),
     
     
 path('activities/', views.get_activities, name='get_activities'),
    path('activity_details/<int:id_actividad>/', views.get_activity_details, name='get_activity_details'),
     # confeccion
     
     #transito
     
     #pcp
     
     # calidad
      path('inspeccionescal/', views.get_inspeccionescal, name='inspeccion-list'),
    path('ordenes-produccioncal/',views.get_ordenes_produccioncal, name='orden-produccion-list'),

    
    
    
]