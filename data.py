# ============================================
# SIGAT - Sistema de Gestión de Activos Tecnológicos
# data.py
# Datos de prueba (en una etapa futura se sustituirán por una base de datos)
# ============================================

import hashlib


def hash_password(texto_plano):
    """Convierte una contraseña de texto plano en un hash SHA-256."""
    return hashlib.sha256(texto_plano.encode()).hexdigest()


# --------------------------------------------
# Usuarios (las contraseñas se guardan como hash, nunca en texto plano)
# --------------------------------------------
usuarios = [
    {"id": 1, "nombre": "Administrador", "username": "admin",
     "password": hash_password("1234"), "rol": "Administrador"},
    {"id": 2, "nombre": "María López", "username": "mlopez",
     "password": hash_password("1234"), "rol": "Técnico"},
    {"id": 3, "nombre": "Carlos Ramírez", "username": "cramirez",
     "password": hash_password("1234"), "rol": "Técnico"},
]

# --------------------------------------------
# Clientes
# --------------------------------------------
clientes = [
    {"id": 1, "nombre": "Grupo Empresarial SA", "contacto": "Ana Pérez",
     "telefono": "2222-1111", "correo": "contacto@grupoempresarial.com"},
    {"id": 2, "nombre": "Consultoría Global", "contacto": "Luis Vargas",
     "telefono": "2222-2222", "correo": "contacto@consultoriaglobal.com"},
    {"id": 3, "nombre": "Innovación Tecnológica", "contacto": "Laura Sánchez",
     "telefono": "2222-3333", "correo": "contacto@innovacion.com"},
]

# --------------------------------------------
# Sedes
# --------------------------------------------
sedes = [
    {"id": 1, "cliente_id": 1, "nombre": "San José", "direccion": "San José Centro"},
    {"id": 2, "cliente_id": 2, "nombre": "Alajuela", "direccion": "Alajuela Centro"},
    {"id": 3, "cliente_id": 3, "nombre": "Heredia", "direccion": "Heredia Centro"},
]

# --------------------------------------------
# Activos
# --------------------------------------------
activos = [
    {"id": 1, "serie": "SN-0012458", "placa": "ACT-0001", "cliente_id": 1, "sede_id": 1,
     "usuario": "María López", "categoria": "Laptop", "marca": "Dell", "modelo": "Inspiron 15",
     "fecha_adquisicion": "2024-01-15", "estado": "Operativo", "garantia": "2025-08-12"},
    {"id": 2, "serie": "SN-0012459", "placa": "ACT-0002", "cliente_id": 2, "sede_id": 2,
     "usuario": "Carlos Ramírez", "categoria": "Laptop", "marca": "HP", "modelo": "EliteBook",
     "fecha_adquisicion": "2024-02-10", "estado": "Operativo", "garantia": "2025-11-05"},
    {"id": 3, "serie": "SN-0012460", "placa": "ACT-0003", "cliente_id": 3, "sede_id": 3,
     "usuario": "Ana Torres", "categoria": "Laptop", "marca": "Lenovo", "modelo": "ThinkPad",
     "fecha_adquisicion": "2024-03-20", "estado": "En mantenimiento", "garantia": "2025-07-20"},
    {"id": 4, "serie": "SN-0012461", "placa": "ACT-0004", "cliente_id": 1, "sede_id": 1,
     "usuario": "Pedro Gómez", "categoria": "Laptop", "marca": "Acer", "modelo": "Aspire 5",
     "fecha_adquisicion": "2024-04-01", "estado": "Operativo", "garantia": "2025-09-18"},
    {"id": 5, "serie": "SN-0012462", "placa": "ACT-0005", "cliente_id": 2, "sede_id": 2,
     "usuario": "Luis Fernández", "categoria": "Monitor", "marca": "Dell", "modelo": "P2422H",
     "fecha_adquisicion": "2023-05-01", "estado": "Fuera de servicio", "garantia": "2025-01-10"},
]

# --------------------------------------------
# Mantenimientos
# --------------------------------------------
mantenimientos = [
    {"id": 1, "activo_id": 3, "tipo": "Preventivo", "fecha": "2025-07-15",
     "tecnico": "Administrador", "descripcion": "Limpieza interna y revisión general",
     "observaciones": "Equipo en observación."},
    {"id": 2, "activo_id": 1, "tipo": "Correctivo", "fecha": "2025-06-20",
     "tecnico": "María López", "descripcion": "Actualización de controladores",
     "observaciones": "Equipo operativo."},
]


# --------------------------------------------
# Funciones auxiliares (usadas por app.py para no repetir lógica)
# --------------------------------------------

def buscar_cliente(cliente_id):
    return next((c for c in clientes if c["id"] == cliente_id), None)


def buscar_sede(sede_id):
    return next((s for s in sedes if s["id"] == sede_id), None)


def buscar_activo(activo_id):
    return next((a for a in activos if a["id"] == activo_id), None)


def nombre_cliente(cliente_id):
    c = buscar_cliente(cliente_id)
    return c["nombre"] if c else "N/D"


def nombre_sede(sede_id):
    s = buscar_sede(sede_id)
    return s["nombre"] if s else "N/D"


def activos_de_cliente(cliente_id):
    return [a for a in activos if a["cliente_id"] == cliente_id]


def eliminar_cliente(cliente_id):
    """Elimina un cliente solo si no tiene activos asociados.
    Devuelve (True, None) si se eliminó, o (False, mensaje) si no se pudo."""
    if activos_de_cliente(cliente_id):
        return False, "No se puede eliminar: el cliente tiene activos registrados a su nombre."
    global clientes, sedes
    clientes = [c for c in clientes if c["id"] != cliente_id]
    sedes = [s for s in sedes if s["cliente_id"] != cliente_id]
    return True, None


def eliminar_activo(activo_id):
    global activos, mantenimientos
    activos = [a for a in activos if a["id"] != activo_id]
    mantenimientos = [m for m in mantenimientos if m["activo_id"] != activo_id]
