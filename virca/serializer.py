from rest_framework import serializers
from .models import Acabado

class AcabadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acabado
        fields = ['id_acabado', 'nombre']
        # fields = '__all__'