from django.urls import path, include
# from rest_framework import routers
#from virca import views
from .views import AcabadoViewSet
from rest_framework.routers import DefaultRouter

from . import views
from .views import AcabadoListView

router = DefaultRouter()
router.register(r'acabado', AcabadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('acabados/', AcabadoListView.as_view(), name='acabados-list'),
]