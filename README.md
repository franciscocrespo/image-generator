# Image Generator API

API Backend para generación y edición de imágenes con IA utilizando OpenAI.

## Características

- **Generación de imágenes**: Crear imágenes desde texto usando DALL-E
- **Edición de imágenes**: Inpainting y outpainting con IA
- **Eliminación de fondo**: Remover fondos de imágenes automáticamente
- **Arquitectura hexagonal**: Diseño limpio y mantenible
- **FastAPI**: API moderna con documentación automática
- **Async/await**: Operaciones asíncronas para mejor rendimiento

## Requisitos

- Python 3.11+
- Poetry
- OpenAI API Key

## Instalación

1. Instalar dependencias:
```bash
poetry install
```

2. Configurar variables de entorno:
```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

3. Ejecutar la aplicación:
```bash
poetry run uvicorn src.main:app --reload
```

## Endpoints

### Generación de Imágenes
```http
POST /api/v1/images/generate
Content-Type: application/json

{
  "prompt": "A beautiful sunset over the ocean",
  "size": "1024x1024",
  "quality": "standard",
  "n": 1
}
```

### Edición de Imágenes
```http
POST /api/v1/images/edit
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "prompt": "Add a rainbow in the sky",
  "mask_url": "https://example.com/mask.jpg",
  "size": "1024x1024",
  "n": 1
}
```

### Eliminación de Fondo
```http
POST /api/v1/images/remove-background
Content-Type: application/json

"https://example.com/image.jpg"
```

## Documentación

Una vez ejecutada la aplicación, la documentación interactiva estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker

Construir imagen:
```bash
docker build -t image-generator .
```

Ejecutar container:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY="tu-api-key" image-generator
```
