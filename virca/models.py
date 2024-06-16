# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class LoteEntradaVista(models.Model):
    id_entrada = models.IntegerField()
    fecha_entrada = models.DateTimeField()
    id_tipo_lote = models.IntegerField()
    cantidad = models.IntegerField()
    id_dim_confeccion = models.IntegerField()
    id_guia_confeccion = models.IntegerField()

    class Meta:
        managed = False  # No crear tabla en la base de datos
        db_table = 'vista_lote_entrada'


class Acabado(models.Model):
    id_acabado = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'acabado'


class ActividadDiaria(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    fecha_actividad = models.DateField()
    id_orden_producción = models.ForeignKey('OrdenProduccin', models.DO_NOTHING, db_column='id_orden_producción')

    class Meta:
        managed = False
        db_table = 'actividad_diaria'


class AqlCodigo(models.Model):
    id_aql_codigo = models.CharField(primary_key=True, max_length=1)
    tamaño_muestra = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'aql_codigo'


class AqlLoteRango(models.Model):
    id_aql_lote_rango = models.AutoField(primary_key=True)
    min_lote = models.IntegerField()
    max_lote = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aql_lote_rango'


class AqlMuestra(models.Model):
    id_aql_nivel = models.OneToOneField('AqlNivel', models.DO_NOTHING, db_column='id_aql_nivel', primary_key=True)  # The composite primary key (id_aql_nivel, id_aql_lote_rango) found, that is not supported. The first column is selected.
    id_aql_lote_rango = models.ForeignKey(AqlLoteRango, models.DO_NOTHING, db_column='id_aql_lote_rango')
    id_aql_codigo = models.ForeignKey(AqlCodigo, models.DO_NOTHING, db_column='id_aql_codigo')

    class Meta:
        managed = False
        db_table = 'aql_muestra'
        unique_together = (('id_aql_nivel', 'id_aql_lote_rango'),)


class AqlNivel(models.Model):
    id_aql_nivel = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=2)

    class Meta:
        managed = False
        db_table = 'aql_nivel'


class AqlResultadoRango(models.Model):
    id_aql_codigo = models.OneToOneField(AqlCodigo, models.DO_NOTHING, db_column='id_aql_codigo', primary_key=True)  # The composite primary key (id_aql_codigo, id_aql_significancia) found, that is not supported. The first column is selected.
    id_aql_significancia = models.ForeignKey('AqlSignificancia', models.DO_NOTHING, db_column='id_aql_significancia')
    max_aceptacion = models.IntegerField()
    min_rechazo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aql_resultado_rango'
        unique_together = (('id_aql_codigo', 'id_aql_significancia'),)


class AqlSignificancia(models.Model):
    id_aql_significancia = models.AutoField(primary_key=True)
    nivel_significancia = models.DecimalField(unique=True, max_digits=4, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'aql_significancia'


class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'area'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CajaLote(models.Model):
    id_caja = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    id_lote = models.ForeignKey('Lote', models.DO_NOTHING, db_column='id_lote')
    id_estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='id_estado')

    class Meta:
        managed = False
        db_table = 'caja_lote'


class CajaPrenda(models.Model):
    id_caja = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    fecha_creacion = models.IntegerField()
    id_estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='id_estado')
    id_dim_prenda = models.ForeignKey('DimensionPrenda', models.DO_NOTHING, db_column='id_dim_prenda')
    id_actividad = models.ForeignKey(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad')

    class Meta:
        managed = False
        db_table = 'caja_prenda'


class CajaSalida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    fecha_salida = models.DateTimeField()
    id_caja = models.ForeignKey(CajaLote, models.DO_NOTHING, db_column='id_caja')
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area')

    class Meta:
        managed = False
        db_table = 'caja_salida'


class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'cargo'


class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'color'


class Confeccion(models.Model):
    id_confeccion = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', models.DO_NOTHING, db_column='id_lote')
    id_dim_confeccion = models.ForeignKey('DimensionConfeccion', models.DO_NOTHING, db_column='id_dim_confeccion')
    id_empleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='id_empleado')
    id_caja = models.ForeignKey(CajaLote, models.DO_NOTHING, db_column='id_caja', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'confeccion'


class Correo(models.Model):
    id_correo = models.AutoField(primary_key=True)
    direccion_correo = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'correo'


class Corte(models.Model):
    id_corte = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', models.DO_NOTHING, db_column='id_lote')
    id_dim_corte = models.ForeignKey('DimensionCorte', models.DO_NOTHING, db_column='id_dim_corte')
    id_maquina = models.ForeignKey('Maquina', models.DO_NOTHING, db_column='id_maquina')

    class Meta:
        managed = False
        db_table = 'corte'


class DimConfeccionDetalle(models.Model):
    id_dim_confeccion = models.OneToOneField('DimensionConfeccion', models.DO_NOTHING, db_column='id_dim_confeccion', primary_key=True)  # The composite primary key (id_dim_confeccion, id_dim_corte) found, that is not supported. The first column is selected.
    id_dim_corte = models.ForeignKey('DimensionCorte', models.DO_NOTHING, db_column='id_dim_corte')

    class Meta:
        managed = False
        db_table = 'dim_confeccion_detalle'
        unique_together = (('id_dim_confeccion', 'id_dim_corte'),)


class DimPrendaDetalle(models.Model):
    id_dim_prenda = models.OneToOneField('DimensionPrenda', models.DO_NOTHING, db_column='id_dim_prenda', primary_key=True)  # The composite primary key (id_dim_prenda, id_acabado) found, that is not supported. The first column is selected.
    id_acabado = models.ForeignKey(Acabado, models.DO_NOTHING, db_column='id_acabado')

    class Meta:
        managed = False
        db_table = 'dim_prenda_detalle'
        unique_together = (('id_dim_prenda', 'id_acabado'),)


class DimensionConfeccion(models.Model):
    id_dim_confeccion = models.AutoField(primary_key=True)
    id_tipo_prenda = models.ForeignKey('TipoPrenda', models.DO_NOTHING, db_column='id_tipo_prenda')
    id_estilo_prenda = models.ForeignKey('EstiloPrenda', models.DO_NOTHING, db_column='id_estilo_prenda')
    id_guia_confeccion = models.ForeignKey('GuiaConfeccion', models.DO_NOTHING, db_column='id_guia_confeccion')
    id_talla = models.ForeignKey('Talla', models.DO_NOTHING, db_column='id_talla')
    id_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='id_genero')

    class Meta:
        managed = False
        db_table = 'dimension_confeccion'


class DimensionCorte(models.Model):
    id_dim_corte = models.AutoField(primary_key=True)
    id_dim_materia_prima = models.ForeignKey('DimensionMateriaPrima', models.DO_NOTHING, db_column='id_dim_materia_prima')
    id_dim_parte_prenda = models.ForeignKey('DimensionPartePrenda', models.DO_NOTHING, db_column='id_dim_parte_prenda')

    class Meta:
        managed = False
        db_table = 'dimension_corte'


class DimensionMateriaPrima(models.Model):
    id_dim_materia_prima = models.AutoField(primary_key=True)
    id_tipo_materia_prima = models.ForeignKey('TipoMateriaPrima', models.DO_NOTHING, db_column='id_tipo_materia_prima')
    id_color = models.ForeignKey(Color, models.DO_NOTHING, db_column='id_color')

    class Meta:
        managed = False
        db_table = 'dimension_materia_prima'


class DimensionPartePrenda(models.Model):
    id_dim_parte_prenda = models.AutoField(primary_key=True)
    id_tipo_parte_prenda = models.ForeignKey('TipoPartePrenda', models.DO_NOTHING, db_column='id_tipo_parte_prenda')

    class Meta:
        managed = False
        db_table = 'dimension_parte_prenda'


class DimensionPrenda(models.Model):
    id_dim_prenda = models.AutoField(primary_key=True)
    id_dim_confeccion = models.ForeignKey(DimensionConfeccion, models.DO_NOTHING, db_column='id_dim_confeccion')

    class Meta:
        managed = False
        db_table = 'dimension_prenda'


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'direccion'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    dni = models.DecimalField(unique=True, max_digits=8, decimal_places=0)
    nombre = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=15)
    primer_apellido = models.CharField(max_length=15)
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area')
    id_direccion = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='id_direccion')
    id_telefono = models.ForeignKey('Telefono', models.DO_NOTHING, db_column='id_telefono')
    id_correo = models.ForeignKey(Correo, models.DO_NOTHING, db_column='id_correo')
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo')

    class Meta:
        managed = False
        db_table = 'empleado'


class EmpleadoActividad(models.Model):
    id_actividad = models.OneToOneField(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad', primary_key=True)  # The composite primary key (id_actividad, id_empleado) found, that is not supported. The first column is selected.
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado')
    cantidad_hecha = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'empleado_actividad'
        unique_together = (('id_actividad', 'id_empleado'),)


class Espacio(models.Model):
    id_espacio = models.DecimalField(primary_key=True, max_digits=9, decimal_places=0)
    ancho = models.DecimalField(max_digits=3, decimal_places=2)
    largo = models.DecimalField(max_digits=3, decimal_places=2)
    alto = models.DecimalField(max_digits=3, decimal_places=2)
    id_estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='id_estado')
    id_lote = models.OneToOneField('Lote', models.DO_NOTHING, db_column='id_lote', blank=True, null=True)
    id_estanteria = models.ForeignKey('Estanteria', models.DO_NOTHING, db_column='id_estanteria')

    class Meta:
        managed = False
        db_table = 'espacio'


class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'estado'


class Estanteria(models.Model):
    id_estanteria = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0)
    ancho_estanteria = models.DecimalField(max_digits=3, decimal_places=2)
    largo_estanteria = models.DecimalField(max_digits=3, decimal_places=2)
    alto_estanteria = models.DecimalField(max_digits=3, decimal_places=2)
    id_pasillo = models.ForeignKey('Pasillo', models.DO_NOTHING, db_column='id_pasillo')

    class Meta:
        managed = False
        db_table = 'estanteria'


class EstiloPrenda(models.Model):
    id_estilo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'estilo_prenda'


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'genero'


class GuiaConfeccion(models.Model):
    id_guia_confeccion = models.AutoField(primary_key=True)
    medida_pecho = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_cintura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_cadera = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_hombro = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_longitud = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_manga = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    medida_muslo = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guia_confeccion'


class InspeccionCalidad(models.Model):
    id_inspeccion = models.AutoField(primary_key=True)
    fecha_inspeccion = models.DateTimeField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    cantidad_defectuosos = models.IntegerField()
    id_lote = models.ForeignKey('Lote', models.DO_NOTHING, db_column='id_lote')
    id_aql_lote_rango = models.ForeignKey(AqlMuestra, models.DO_NOTHING, db_column='id_aql_lote_rango', to_field='id_aql_lote_rango')
    id_aql_nivel = models.IntegerField()
    id_aql_codigo = models.ForeignKey(AqlResultadoRango, models.DO_NOTHING, db_column='id_aql_codigo')
    id_aql_significancia = models.IntegerField()
    id_descripcion = models.ForeignKey('InspeccionDescripcion', models.DO_NOTHING, db_column='id_descripcion')
    id_resultado = models.ForeignKey('Resultado', models.DO_NOTHING, db_column='id_resultado')

    class Meta:
        managed = False
        db_table = 'inspeccion_calidad'


class InspeccionDescripcion(models.Model):
    id_descripcion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'inspeccion_descripcion'


class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    id_tipo_lote = models.ForeignKey('TipoLote', models.DO_NOTHING, db_column='id_tipo_lote')
    id_dim_corte = models.ForeignKey(DimensionCorte, models.DO_NOTHING, db_column='id_dim_corte', blank=True, null=True)
    id_dim_confeccion = models.ForeignKey(DimensionConfeccion, models.DO_NOTHING, db_column='id_dim_confeccion', blank=True, null=True)
    id_dim_materia_prima = models.ForeignKey(DimensionMateriaPrima, models.DO_NOTHING, db_column='id_dim_materia_prima', blank=True, null=True)
    id_actividad = models.ForeignKey(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad')
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lote'


class LoteEntrada(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    fecha_entrada = models.DateTimeField()
    id_lote = models.ForeignKey(Lote, models.DO_NOTHING, db_column='id_lote')
    id_espacio = models.ForeignKey(Espacio, models.DO_NOTHING, db_column='id_espacio')

    class Meta:
        managed = False
        db_table = 'lote_entrada'


class LoteSalida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    fecha_salida = models.DateTimeField()
    id_lote = models.ForeignKey(Lote, models.DO_NOTHING, db_column='id_lote')
    area_envio = models.ForeignKey(Area, models.DO_NOTHING, db_column='area_envio')

    class Meta:
        managed = False
        db_table = 'lote_salida'


class Maquina(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    capacidad_total = models.IntegerField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')

    class Meta:
        managed = False
        db_table = 'maquina'


class MaquinaActividad(models.Model):
    id_actividad = models.OneToOneField(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad', primary_key=True)  # The composite primary key (id_actividad, id_maquina) found, that is not supported. The first column is selected.
    id_maquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='id_maquina')
    cantidad_hecha = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'maquina_actividad'
        unique_together = (('id_actividad', 'id_maquina'),)


class MateriaPrima(models.Model):
    id_materia_prima = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey(Lote, models.DO_NOTHING, db_column='id_lote')
    id_dim_materia_prima = models.ForeignKey(DimensionMateriaPrima, models.DO_NOTHING, db_column='id_dim_materia_prima')
    id_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor')

    class Meta:
        managed = False
        db_table = 'materia_prima'


class OrdenPedido(models.Model):
    id_orden_pedido = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    fecha_entrega = models.DateTimeField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'orden_pedido'


class OrdenProduccin(models.Model):
    id_orden_producción = models.AutoField(primary_key=True)
    fecha_fin = models.DateField()
    fecha_inicio = models.DateField()
    cantidad = models.IntegerField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area')
    id_dim_prenda = models.ForeignKey(DimensionPrenda, models.DO_NOTHING, db_column='id_dim_prenda', blank=True, null=True)
    id_dim_confeccion = models.ForeignKey(DimensionConfeccion, models.DO_NOTHING, db_column='id_dim_confeccion', blank=True, null=True)
    id_dim_corte = models.ForeignKey(DimensionCorte, models.DO_NOTHING, db_column='id_dim_corte', blank=True, null=True)
    id_orden_trabajo = models.ForeignKey('OrdenTrabajo', models.DO_NOTHING, db_column='id_orden_trabajo')
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'orden_producción'


class OrdenTrabajo(models.Model):
    id_orden_trabajo = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    prioridad = models.IntegerField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    id_plan = models.ForeignKey('PlanProduccion', models.DO_NOTHING, db_column='id_plan')
    id_orden_pedido = models.ForeignKey(OrdenPedido, models.DO_NOTHING, db_column='id_orden_pedido')
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'orden_trabajo'


class ParteCorteDetalle(models.Model):
    id_dim_parte_prenda = models.OneToOneField(DimensionPartePrenda, models.DO_NOTHING, db_column='id_dim_parte_prenda', primary_key=True)  # The composite primary key (id_dim_parte_prenda, id_tipo_corte) found, that is not supported. The first column is selected.
    id_tipo_corte = models.ForeignKey('TipoCorte', models.DO_NOTHING, db_column='id_tipo_corte')
    medida = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'parte_corte_detalle'
        unique_together = (('id_dim_parte_prenda', 'id_tipo_corte'),)


class Pasillo(models.Model):
    id_pasillo = models.DecimalField(primary_key=True, max_digits=5, decimal_places=0)
    largo_pasillo = models.DecimalField(max_digits=4, decimal_places=2)
    ancho_pasillo = models.DecimalField(max_digits=3, decimal_places=2)
    id_zona = models.ForeignKey('Zona', models.DO_NOTHING, db_column='id_zona')

    class Meta:
        managed = False
        db_table = 'pasillo'


class PedidoDetalle(models.Model):
    id_orden_pedido = models.OneToOneField(OrdenPedido, models.DO_NOTHING, db_column='id_orden_pedido', primary_key=True)  # The composite primary key (id_orden_pedido, id_dim_prenda) found, that is not supported. The first column is selected.
    id_dim_prenda = models.ForeignKey(DimensionPrenda, models.DO_NOTHING, db_column='id_dim_prenda')

    class Meta:
        managed = False
        db_table = 'pedido_detalle'
        unique_together = (('id_orden_pedido', 'id_dim_prenda'),)


class PlanProduccion(models.Model):
    id_plan = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'plan_produccion'


class Prenda(models.Model):
    id_prenda = models.AutoField(primary_key=True)
    id_dim_prenda = models.ForeignKey(DimensionPrenda, models.DO_NOTHING, db_column='id_dim_prenda')
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado')
    id_caja = models.ForeignKey(CajaPrenda, models.DO_NOTHING, db_column='id_caja')

    class Meta:
        managed = False
        db_table = 'prenda'


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    ruc = models.DecimalField(unique=True, max_digits=11, decimal_places=0)
    denominacion_social = models.CharField(max_length=30)
    id_direccion = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='id_direccion')
    id_telefono = models.ForeignKey('Telefono', models.DO_NOTHING, db_column='id_telefono')
    id_correo = models.ForeignKey(Correo, models.DO_NOTHING, db_column='id_correo')

    class Meta:
        managed = False
        db_table = 'proveedor'


class RegistroLoteCaja(models.Model):
    id_lote = models.OneToOneField(Lote, models.DO_NOTHING, db_column='id_lote', primary_key=True)  # The composite primary key (id_lote, id_caja) found, that is not supported. The first column is selected.
    id_caja = models.ForeignKey(CajaLote, models.DO_NOTHING, db_column='id_caja')
    fecha_transicion = models.DateField()

    class Meta:
        managed = False
        db_table = 'registro_lote_caja'
        unique_together = (('id_lote', 'id_caja'),)


class RegistroTransformacionCaja(models.Model):
    id_actividad = models.OneToOneField(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad', primary_key=True)  # The composite primary key (id_actividad, id_caja) found, that is not supported. The first column is selected.
    id_caja = models.ForeignKey(CajaLote, models.DO_NOTHING, db_column='id_caja')

    class Meta:
        managed = False
        db_table = 'registro_transformacion_caja'
        unique_together = (('id_actividad', 'id_caja'),)


class RegistroUsoLote(models.Model):
    id_actividad = models.OneToOneField(ActividadDiaria, models.DO_NOTHING, db_column='id_actividad', primary_key=True)  # The composite primary key (id_actividad, id_lote) found, that is not supported. The first column is selected.
    id_lote = models.ForeignKey(Lote, models.DO_NOTHING, db_column='id_lote')
    cantidad_usada = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'registro_uso_lote'
        unique_together = (('id_actividad', 'id_lote'),)


class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'resultado'


class Talla(models.Model):
    id_talla = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'talla'


class Telefono(models.Model):
    id_telefono = models.AutoField(primary_key=True)
    numero = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'telefono'


class TipoCorte(models.Model):
    id_tipo_corte = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_corte'


class TipoLote(models.Model):
    id_tipo_lote = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'tipo_lote'


class TipoMateriaPrima(models.Model):
    id_tipo_materia_prima = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'tipo_materia_prima'


class TipoPartePrenda(models.Model):
    id_tipo_parte_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_parte_prenda'


class TipoPrenda(models.Model):
    id_tipo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_prenda'


class Zona(models.Model):
    id_zona = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0)
    nombre = models.CharField(unique=True, max_length=19)
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='id_area')

    class Meta:
        managed = False
        db_table = 'zona'
