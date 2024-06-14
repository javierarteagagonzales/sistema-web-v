from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Acabado
from django.db import connection

# Create your views here.

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