from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado
# Create your views here.

class AcabadoViewSet(viewsets.ModelViewSet):
    queryset = Acabado.objects.all()
    serializer_class = AcabadoSerializer
    