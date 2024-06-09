from django.shortcuts import render
from rest_framework import viewsets
from .serializer import AcabadoSerializer
from .models import Acabado
# Create your views here.

class VircaView(viewsets.ModelViewSet):
    serializer_class = AcabadoSerializer
    queryset = Task.objects.all()