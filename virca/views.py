from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado

from django.http import JsonResponse

# Create your views here.

class AcabadoViewSet(viewsets.ModelViewSet):
    queryset = Acabado.objects.all()
    serializer_class = AcabadoSerializer

def listar_acabados(request):
    acabados = list(Acabado.objects.raw('SELECT * FROM acabado'))
    data = [{'id_acabado': acabado.id_acabado, 'nombre': acabado.nombre} for acabado in acabados]
    return JsonResponse(data, safe=False)