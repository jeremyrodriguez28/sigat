# SIGAT - Sistema de Gestión de Activos Tecnológicos

Proyecto académico para el curso **BISV-03 Modelos de Programación I**,
Universidad San Marcos.

Autor: Jeremy Johel Rodríguez Bogantes

## Descripción

SIGAT centraliza la administración de los activos tecnológicos (laptops,
monitores, equipos de red, etc.) de los clientes de una empresa de soporte
técnico outsourcing: registro de clientes y sedes, inventario de activos,
historial de mantenimientos, control de garantías, consultas y reportes.

Este primer avance implementa una interfaz web (Flask) con autenticación de
usuarios, sobre datos de prueba almacenados en memoria. En una siguiente
etapa se sustituirán por una base de datos.

## Demo en línea

🔗 (agregar aquí el link de Render una vez desplegado)

**Usuario de prueba:** `admin` &nbsp;&nbsp; **Contraseña:** `1234`

## Tecnologías

- Python 3 / Flask
- Jinja2 (plantillas HTML)
- CSS puro

## Cómo ejecutarlo localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/sigat.git
cd sigat

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Luego abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.

## Estructura del proyecto

```
sigat/
├── app.py                 # Rutas y lógica de la aplicación (Flask)
├── data.py                # Datos de prueba y funciones auxiliares
├── requirements.txt       # Dependencias
├── Procfile                # Comando de arranque para Render
├── templates/              # Vistas HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── clientes.html
│   ├── activos.html
│   ├── mantenimientos.html
│   ├── garantias.html
│   ├── consultas.html
│   ├── reportes.html
│   └── configuracion.html
└── static/
    └── css/
        └── estilo.css       # Estilos de la aplicación
```

## Usuarios de prueba

| Usuario   | Contraseña | Rol           |
|-----------|-----------|----------------|
| admin     | 1234      | Administrador  |
| mlopez    | 1234      | Técnico        |
| cramirez  | 1234      | Técnico        |

## Próximas etapas

- Sustituir las listas en memoria por una base de datos.
- Formularios de edición y eliminación de registros.
- Exportación de reportes a PDF/Excel.
- Roles y permisos diferenciados por tipo de usuario.
