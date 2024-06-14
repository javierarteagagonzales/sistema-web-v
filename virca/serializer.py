from rest_framework import serializers
from .models import (
    Acabado, ActividadDiaria, AqlCodigo, AqlLoteRango, AqlMuestra, AqlNivel, AqlResultadoRango, 
    AqlSignificancia, Area, AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, 
    AuthUserGroups, AuthUserUserPermissions, CajaLote, CajaPrenda, CajaSalida, Cargo, Color, 
    Confeccion, Correo, Corte, DimConfeccionDetalle, DimPrendaDetalle, DimensionConfeccion, 
    DimensionCorte, DimensionMateriaPrima, DimensionPartePrenda, DimensionPrenda, Direccion, 
    DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession, Empleado, 
    EmpleadoActividad, Espacio, Estado, Estanteria, EstiloPrenda, Genero, GuiaConfeccion, 
    InspeccionCalidad, InspeccionDescripcion, Lote, LoteEntrada, LoteSalida, Maquina, 
    MaquinaActividad, MateriaPrima, OrdenPedido, OrdenProduccin
)

class AcabadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acabado
        fields = '__all__'

class ActividadDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadDiaria
        fields = '__all__'

class AqlCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlCodigo
        fields = '__all__'

class AqlLoteRangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlLoteRango
        fields = '__all__'

class AqlMuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlMuestra
        fields = '__all__'

class AqlNivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlNivel
        fields = '__all__'

class AqlResultadoRangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlResultadoRango
        fields = '__all__'

class AqlSignificanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AqlSignificancia
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroup
        fields = '__all__'

class AuthGroupPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroupPermissions
        fields = '__all__'

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermission
        fields = '__all__'

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class AuthUserGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserGroups
        fields = '__all__'

class AuthUserUserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserUserPermissions
        fields = '__all__'

class CajaLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CajaLote
        fields = '__all__'

class CajaPrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CajaPrenda
        fields = '__all__'

class CajaSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CajaSalida
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ConfeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Confeccion
        fields = '__all__'

class CorreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correo
        fields = '__all__'

class CorteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corte
        fields = '__all__'

class DimConfeccionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimConfeccionDetalle
        fields = '__all__'

class DimPrendaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimPrendaDetalle
        fields = '__all__'

class DimensionConfeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionConfeccion
        fields = '__all__'

class DimensionCorteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionCorte
        fields = '__all__'

class DimensionMateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionMateriaPrima
        fields = '__all__'

class DimensionPartePrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionPartePrenda
        fields = '__all__'

class DimensionPrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionPrenda
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class DjangoAdminLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoAdminLog
        fields = '__all__'

class DjangoContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoContentType
        fields = '__all__'

class DjangoMigrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoMigrations
        fields = '__all__'

class DjangoSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoSession
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class EmpleadoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpleadoActividad
        fields = '__all__'

class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class EstanteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estanteria
        fields = '__all__'

class EstiloPrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstiloPrenda
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class GuiaConfeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaConfeccion
        fields = '__all__'

class InspeccionCalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspeccionCalidad
        fields = '__all__'

class InspeccionDescripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspeccionDescripcion
        fields = '__all__'

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class LoteEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteEntrada
        fields = '__all__'

class LoteSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteSalida
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'

class MaquinaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaquinaActividad
        fields = '__all__'

class MateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaPrima
        fields = '__all__'

class OrdenPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenPedido
        fields = '__all__'

class OrdenProduccinSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenProduccin
        fields = '__all__'
