from django.urls import path, include
# from rest_framework import routers
#from virca import views
from .views import AcabadoViewSet
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'acabado', AcabadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('acabados/', views.listar_acabados, name='listar_acabados'),
]