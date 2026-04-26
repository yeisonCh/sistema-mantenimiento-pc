# app/services/__init__.py

from .persona import (
    service_obtener_personas,
    service_obtener_persona_por_id,
    service_crear_persona,
    service_actualizar_persona,
    service_eliminar_persona
)

from .tipo_activo import (
    service_obtener_tipos_activo,
    service_obtener_tipo_activo_por_id,
    service_crear_tipo_activo,
    service_actualizar_tipo_activo,
    service_eliminar_tipo_activo
)

from .empresa import (
    service_obtener_empresas,
    service_obtener_empresa_por_id,
    service_crear_empresa,
    service_actualizar_empresa,
    service_eliminar_empresa
)

from .activo import ( 
    service_obtener_activos,
    service_obtener_activo_por_id,
    service_obtener_activos_por_tipo,
    service_obtener_activos_por_empresa,
    service_obtener_activos_por_estado,
    service_crear_activo,
    service_actualizar_activo,
    service_eliminar_activo
)