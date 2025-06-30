# Compatibility Dating App

Una aplicación de citas inteligente que calcula la compatibilidad entre usuarios basada en sus respuestas a preguntas personalizadas. Construida con FastAPI y Vue.js.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Algoritmo de Compatibilidad](#algoritmo-de-compatibilidad)
- [Autenticación](#autenticación)
- [Base de Datos](#base-de-datos)


## Características

### Para Usuarios
- **Registro y autenticación segura** con JWT
- **Sistema de preguntas personalizadas** por categorías
- **Cálculo de compatibilidad inteligente** basado en respuestas
- **Mejores matches** ordenados por porcentaje de compatibilidad
- **Perfil personal** con información básica
- **Historial de compatibilidades** calculadas

### Para Administradores
- **Panel de administración completo**
- **Gestión de usuarios** (CRUD completo)
- **Creación y gestión de preguntas** con diferentes tipos
- **Sistema de opciones** para preguntas múltiples
- **Cálculo masivo de compatibilidades**
- **Reportes y estadísticas** del sistema

## Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLite** - Base de datos ligera
- **JWT** - Autenticación segura
- **Bcrypt** - Hash de contraseñas
- **Pydantic** - Validación de datos
- **CORS** - Soporte para frontend

### Frontend
- **Vue.js** - Framework JavaScript progresivo
- **JavaScript/TypeScript** - Lenguaje principal del frontend

### Herramientas de Desarrollo
- **Uvicorn** - Servidor ASGI
- **Python 3.8+** - Lenguaje del backend

## Estructura del Proyecto

```
compatibility-app/
├── 📁 CORE/
│   ├── 📁 app/
│   │   └── 📁 __pycache__/
│   ├── 📁 repositories/
│   │   └── 📄 usuario_repository.py
│   ├── 📁 routers/
│   │   ├── 📄 admin.py
│   │   ├── 📄 auth_routes.py
│   │   └── 📄 usuarios.py
│   ├── 📁 services/
│   │   ├── 📁 factories/
│   │   │   └── 📄 token_factory.py
│   │   ├── 📄 compatibilidad.py
│   │   └── 📄 estrategias.py
│   ├── 📄 auth.py
│   ├── 📄 database.py
│   ├── 📄 main.py
│   └── 📄 models.py
├── 📁 vue-project/
│   └── [Archivos del frontend Vue.js]
├── 📄 compatibility_app.db
├── 📄 README.md
├── 📄 requirements.txt
└── 📄 run.py
```

## Instalación

### Prerequisitos
- Python 3.8 o superior
- Node.js y npm (para el frontend)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/compatibility-app.git
cd compatibility-app
```

2. **Configurar el entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias del backend**
```bash
pip install -r requirements.txt
```

4. **Instalar dependencias del frontend**
```bash
cd vue-project
npm install
cd ..
```

5. **Inicializar la base de datos**
```bash
python run.py
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./compatibility_app.db
```

### Configuración de la Base de Datos

La aplicación utiliza SQLite por defecto. Al ejecutar por primera vez, se creará automáticamente:
- Base de datos: `compatibility_app.db`
- Administrador por defecto:
  - **Email:** `admin@admin.com`
  - **Contraseña:** `admin123`

## Uso

### Iniciar el Backend
```bash
python run.py
# O usando uvicorn directamente:
uvicorn CORE.main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar el Frontend
```bash
cd vue-project
npm run dev
```

### Acceder a la Aplicación
- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:5173
- **Documentación API:** http://localhost:8000/docs

## API Endpoints

### Autenticación
```http
POST /register          # Registrar usuario
POST /login             # Login usuario
POST /admin/login       # Login administrador
```

### Usuarios
```http
GET  /preguntas                    # Obtener preguntas disponibles
POST /respuestas                   # Crear respuesta de usuario
GET  /mis-respuestas/{id_usuario}  # Obtener respuestas del usuario
```

### Compatibilidad
```http
POST /calcular-compatibilidad/{otro_usuario_id}  # Calcular compatibilidad
GET  /mis-compatibilidades                       # Obtener mis compatibilidades
GET  /mejores-matches                            # Obtener mejores matches
```

### Administración
```http
# Usuarios
GET    /admin/usuarios           # Listar usuarios
POST   /admin/usuarios           # Crear usuario
GET    /admin/usuarios/{id}      # Obtener usuario
PUT    /admin/usuarios/{id}      # Actualizar usuario
DELETE /admin/usuarios/{id}      # Eliminar usuario

# Preguntas
POST /admin/preguntas           # Crear pregunta
GET  /admin/preguntas           # Listar preguntas

# Opciones
POST /admin/opciones            # Crear opción
GET  /admin/opciones/{pregunta_id}  # Obtener opciones

# Compatibilidades
POST /admin/calcular-compatibilidad-masiva  # Calcular todas las compatibilidades
GET  /admin/compatibilidades                # Obtener todas las compatibilidades
```

## Algoritmo de Compatibilidad

El sistema calcula la compatibilidad basándose en diferentes tipos de preguntas:

### Tipos de Preguntas

1. **Binarias** (`si/no`)
   - Coincidencia exacta: 100% o 0%

2. **Múltiples** (opciones múltiples)
   - Usa el índice de Jaccard: `intersección / unión`

3. **Escala** (1-5)
   - Fórmula: `1 - (diferencia_absoluta / rango_máximo)`

4. **Texto** (respuesta libre)
   - Comparación exacta de texto

### Cálculo Final

```
Compatibilidad = (Σ(coincidencia_i × peso_i) / Σ(peso_i)) × 100
```

Donde:
- `coincidencia_i` es el porcentaje de coincidencia para la pregunta i
- `peso_i` es el peso asignado a la pregunta i

## Autenticación

### Sistema de Tokens JWT
- **Expiración:** 30 minutos por defecto
- **Algoritmo:** HS256
- **Tipos de usuario:** `user` y `admin`

### Flujo de Autenticación
1. Usuario/Admin envía credenciales
2. Sistema valida y genera JWT
3. Token se incluye en header `Authorization: Bearer <token>`
4. Sistema valida token en cada request protegido

## Base de Datos

### Esquema Principal

```sql
-- Usuarios
usuarios (
    id_usuario, nombre, email, contraseña_hash,
    fecha_nacimiento, genero, ubicacion, created_at
)

-- Administradores
administradores (
    id_admin, nombre, email, contraseña_hash, created_at
)

-- Preguntas
preguntas (
    id_pregunta, texto, tipo, categoria, peso, created_at
)

-- Opciones (para preguntas múltiples)
opciones (
    id_opcion, id_pregunta, texto_opcion
)

-- Respuestas de usuarios
respuestas_usuario (
    id_respuesta, id_usuario, id_pregunta, respuesta, created_at
)

-- Resultados de compatibilidad
resultados_compatibilidad (
    id_resultado, id_usuario_origen, id_usuario_comparado,
    porcentaje_compatibilidad, created_at
)
```

## Ejemplos de Uso

### Registrar un Usuario
```bash
curl -X POST "http://localhost:8000/register" \
-H "Content-Type: application/json" \
-d '{
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "contraseña": "password123",
  "fecha_nacimiento": "1990-01-01",
  "genero": "masculino",
  "ubicacion": "Madrid, España"
}'
```

### Crear una Pregunta (Admin)
```bash
curl -X POST "http://localhost:8000/admin/preguntas" \
-H "Authorization: Bearer <admin_token>" \
-H "Content-Type: application/json" \
-d '{
  "texto": "¿Cuál es tu tipo de música favorita?",
  "tipo": "multiple",
  "categoria": "intereses",
  "peso": 1.5
}'
```

### Calcular Compatibilidad
```bash
curl -X POST "http://localhost:8000/calcular-compatibilidad/2" \
-H "Authorization: Bearer <user_token>"
```

## Testing

### Ejecutar Tests
```bash
# Backend
python -m pytest tests/

# Frontend
cd vue-project
npm run test
```

### Datos de Prueba
- **Admin:** `admin@admin.com` / `admin123`
- **Usuario de prueba:** Crear vía `/register`

## Despliegue

### Producción con Render

Este proyecto está desplegado usando **Render**, una plataforma de hosting moderna y fácil de usar.

#### Configuración en Render

**Backend (Web Service):**
```bash
# Build Command
pip install -r requirements.txt

# Start Command
uvicorn CORE.main:app --host 0.0.0.0 --port $PORT
```

**Frontend (Static Site):**
```bash
# Build Command
cd vue-project && npm install && npm run build

# Publish Directory
vue-project/dist
```

#### Variables de Entorno en Render
En el dashboard de Render, configura estas variables:

```env
SECRET_KEY=clave_produccion_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PYTHON_VERSION=3.9.0
PORT=8000
```

#### Pasos para Desplegar

1. **Conectar repositorio** en Render
2. **Crear Web Service** para el backend:
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn CORE.main:app --host 0.0.0.0 --port $PORT`
   
3. **Crear Static Site** para el frontend:
   - Build Command: `cd vue-project && npm install && npm run build`
   - Publish Directory: `vue-project/dist`

4. **Configurar variables de entorno** en el dashboard

#### URLs de Producción
- **API Backend:** `https://tu-app-backend.onrender.com`
- **Frontend:** `https://tu-app-frontend.onrender.com`
- **API Docs:** `https://tu-app-backend.onrender.com/docs`

### Docker (Alternativo)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "CORE.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

