# Image Generator API

🎨 **API Backend para generación y edición de imágenes con IA utilizando OpenAI DALL-E**

Esta API proporciona endpoints para generar, editar y procesar imágenes usando inteligencia artificial, implementada con una arquitectura hexagonal limpia y mantenible.

## 🚀 Características

- **🎭 Generación de imágenes**: Crear imágenes desde texto usando DALL-E 3
- **✏️ Edición de imágenes**: Inpainting y outpainting con IA
- **🗑️ Eliminación de fondo**: Remover fondos de imágenes automáticamente
- **🏗️ Arquitectura hexagonal**: Diseño limpio con separación de responsabilidades
- **⚡ FastAPI**: API moderna con documentación automática OpenAPI/Swagger
- **🔄 Async/await**: Operaciones asíncronas para mejor rendimiento
- **🐳 Docker**: Containerización con multi-stage build
- **📝 Type Safety**: Type hints completos con validación Pydantic

## 🏛️ Arquitectura

El proyecto sigue el patrón de **Arquitectura Hexagonal** (Ports & Adapters):

```
src/
├── domain/              # 🎯 Lógica de negocio
│   └── models.py        # Modelos de dominio (Pydantic)
├── ports/               # 🔌 Interfaces (Puertos)
│   └── image_service.py # Contrato del servicio de imágenes
├── adapters/            # 🔧 Implementaciones (Adaptadores)
│   ├── openai_service.py    # Adaptador OpenAI DALL-E
│   └── api_controllers.py   # Controladores FastAPI
├── config.py            # ⚙️ Configuración de la aplicación
└── main.py              # 🚪 Punto de entrada FastAPI
```

### Componentes Principales

#### 🎯 **Domain Layer**
- **`models.py`**: Define los modelos de datos usando Pydantic
  - `ImageGenerationRequest`: Parámetros para generar imágenes
  - `ImageEditRequest`: Parámetros para editar imágenes
  - `ImageResponse`: Respuesta con URL de imagen generada
  - `ImageOperationResult`: Resultado de operaciones con manejo de errores

#### 🔌 **Ports Layer**
- **`image_service.py`**: Define la interfaz `ImageServicePort` con métodos abstractos
  - `generate_image()`: Contrato para generación
  - `edit_image()`: Contrato para edición
  - `remove_background()`: Contrato para eliminación de fondo

#### 🔧 **Adapters Layer**
- **`openai_service.py`**: Implementación concreta usando OpenAI API
  - Integra con DALL-E 3 para generación
  - Maneja edición con máscaras para inpainting
  - Procesa eliminación de fondo con prompts específicos
- **`api_controllers.py`**: Controladores REST con FastAPI
  - Define endpoints HTTP
  - Maneja validación de entrada
  - Gestiona respuestas de error

## 📋 Requisitos

- **Python**: 3.11 o superior
- **Poetry**: Para gestión de dependencias
- **OpenAI API Key**: Cuenta activa en OpenAI con créditos
- **Docker** (opcional): Para containerización

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd image-generator
```

### 2. Instalar Poetry (si no está instalado)
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 3. Configurar Python con pyenv (recomendado)
```bash
# Instalar Python 3.11 si no está disponible
pyenv install 3.11
pyenv local 3.11
```

### 4. Instalar dependencias
```bash
poetry install
```

### 5. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu API key
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env

# O exportar directamente
export OPENAI_API_KEY="tu-api-key-aqui"
```

> 💡 **Obtener API Key**: Visita [OpenAI Platform](https://platform.openai.com/api-keys)

## 🚀 Ejecución

### Desarrollo Local
```bash
# Activar entorno virtual y ejecutar
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# O activar shell y ejecutar
poetry shell
uvicorn src.main:app --reload
```

### Producción
```bash
# Con Uvicorn
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Con Gunicorn (recomendado para producción)
poetry run gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```bash
# Construir imagen
docker build -t image-generator .

# Ejecutar container
docker run -p 8000:8000 -e OPENAI_API_KEY="tu-api-key" image-generator

# Con docker-compose (crear docker-compose.yml)
docker-compose up -d
```

## 📖 Documentación API

Una vez ejecutada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## 🛡️ Endpoints

### 🎨 Generación de Imágenes
```http
POST /api/v1/images/generate
Content-Type: application/json

{
  "prompt": "A majestic dragon flying over a medieval castle at sunset",
  "size": "1024x1024",     // "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
  "quality": "hd",         // "standard" o "hd"
  "n": 1                   // Número de imágenes (1-10)
}
```

**Respuesta:**
```json
{
  "success": true,
  "images": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
      "revised_prompt": "A majestic dragon with iridescent scales..."
    }
  ],
  "error_message": null
}
```

### ✏️ Edición de Imágenes (Inpainting)
```http
POST /api/v1/images/edit
Content-Type: application/json

{
  "image_url": "https://example.com/original-image.jpg",
  "prompt": "Add a rainbow in the sky",
  "mask_url": "https://example.com/mask.png",  // Opcional: área a editar
  "size": "1024x1024",
  "n": 1
}
```

> 📝 **Nota**: La imagen debe ser PNG válida, menor a 4MB, y cuadrada.

### 🗑️ Eliminación de Fondo
```http
POST /api/v1/images/remove-background
Content-Type: application/json

"https://example.com/image-with-background.jpg"
```

## 🧪 Testing

```bash
# Ejecutar tests
poetry run pytest

# Con coverage
poetry run pytest --cov=src

# Linting
poetry run flake8 src/
poetry run black src/ --check
poetry run mypy src/
```

## 🔧 Desarrollo

### Estructura de Carpetas
```
image-generator/
├── 📁 src/                  # Código fuente
├── 📁 tests/                # Tests unitarios e integración
├── 📄 pyproject.toml        # Configuración Poetry + herramientas
├── 📄 Dockerfile            # Containerización
├── 📄 .python-version       # Versión Python para pyenv
├── 📄 .env.example          # Variables de entorno ejemplo
└── 📄 README.md             # Esta documentación
```

### Comandos Útiles
```bash
# Formatear código
poetry run black src/

# Linting
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Agregar dependencia
poetry add package-name

# Agregar dependencia de desarrollo
poetry add --group dev package-name
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Troubleshooting

### Errores Comunes

**❌ "OPENAI_API_KEY environment variable is required"**
```bash
# Verificar que la variable esté configurada
echo $OPENAI_API_KEY

# Configurar si está vacía
export OPENAI_API_KEY="tu-api-key"
```

**❌ "Poetry command not found"**
```bash
# Reinstalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Agregar al PATH
export PATH="$HOME/.local/bin:$PATH"
```

**❌ "Python version not supported"**
```bash
# Instalar Python 3.11 con pyenv
pyenv install 3.11
pyenv local 3.11
```

---

**🔗 Enlaces Útiles:**
- [OpenAI API Documentation](https://platform.openai.com/docs/guides/image-generation)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
