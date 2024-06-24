from django.urls import path, include
# from rest_framework import routers
#from virca import views
from .views import AcabadoViewSet
from rest_framework.routers import DefaultRouter
from . import views
from .views import AcabadoListView
from .views import get_lote_entrada_vista

router = DefaultRouter()
router.register(r'acabado', AcabadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cajas/', views.CajaPrendaListView.as_view(), name='caja_prenda_list'),
    path('cajas/<int:id_caja>/', views.CajaPrendaDetailView.as_view(), name='caja_prenda_detail'),
       
    path('empleados/',views.EmpleadoListView.as_view(), name='empleado_list'),
    path('acabados/', AcabadoListView.as_view(), name='acabados-list'),
    path('lote-entrada-vista/', get_lote_entrada_vista, name='lote-entrada-vista'),
]