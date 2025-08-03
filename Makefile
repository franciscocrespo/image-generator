# Image Generator API - Makefile

.PHONY: help install dev prod test lint format type-check clean docker-* setup

# Variables
PYTHON_VERSION := 3.11
POETRY := poetry
DOCKER_IMAGE := image-generator
PORT := 8000

help: ## Mostrar esta ayuda
	@echo "Image Generator API - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configuración inicial del proyecto
	@echo "🚀 Configurando proyecto..."
	@if ! command -v poetry &> /dev/null; then \
		echo "❌ Poetry no encontrado. Instalando..."; \
		curl -sSL https://install.python-poetry.org | python3 -; \
	fi
	@if ! command -v pyenv &> /dev/null; then \
		echo "⚠️  pyenv no encontrado. Se recomienda instalarlo para gestión de versiones Python"; \
	else \
		echo "✅ Configurando Python $(PYTHON_VERSION)..."; \
		pyenv install $(PYTHON_VERSION) --skip-existing; \
		pyenv local $(PYTHON_VERSION); \
	fi
	@echo "📦 Instalando dependencias..."
	$(POETRY) install
	@echo "✅ ¡Proyecto configurado! Ahora configura tu OPENAI_API_KEY"

install: ## Instalar dependencias
	$(POETRY) install

dev: ## Ejecutar en modo desarrollo con hot reload
	@echo "🔥 Iniciando servidor de desarrollo..."
	$(POETRY) run uvicorn src.main:app --reload --host 0.0.0.0 --port $(PORT)

prod: ## Ejecutar en modo producción
	@echo "🚀 Iniciando servidor de producción..."
	$(POETRY) run gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$(PORT)

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	$(POETRY) run pytest -v

test-cov: ## Ejecutar tests con coverage
	@echo "🧪 Ejecutando tests con coverage..."
	$(POETRY) run pytest --cov=src --cov-report=html --cov-report=term

lint: ## Linting con flake8
	@echo "🔍 Ejecutando linting..."
	$(POETRY) run flake8 src/

format: ## Formatear código con black
	@echo "✨ Formateando código..."
	$(POETRY) run black src/

format-check: ## Verificar formato sin cambios
	@echo "✅ Verificando formato..."
	$(POETRY) run black src/ --check

type-check: ## Verificar tipos con mypy
	@echo "🔍 Verificando tipos..."
	$(POETRY) run mypy src/

quality: lint type-check format-check ## Ejecutar todas las verificaciones de calidad

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Docker commands
docker-build: ## Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	docker build -t $(DOCKER_IMAGE) .

docker-run: ## Ejecutar container Docker
	@echo "🐳 Ejecutando container..."
	docker run -p $(PORT):$(PORT) -e OPENAI_API_KEY="$(OPENAI_API_KEY)" $(DOCKER_IMAGE)

docker-dev: ## Ejecutar con docker-compose en modo desarrollo
	@echo "🐳 Iniciando con docker-compose..."
	docker-compose up --build

docker-prod: ## Ejecutar con docker-compose en modo producción
	@echo "🐳 Iniciando en modo producción..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

docker-stop: ## Detener containers
	docker-compose down

docker-logs: ## Ver logs de containers
	docker-compose logs -f

docker-clean: ## Limpiar imágenes y containers Docker
	@echo "🧹 Limpiando Docker..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Utility commands
deps-add: ## Agregar dependencia (uso: make deps-add PACKAGE=nombre)
	$(POETRY) add $(PACKAGE)

deps-add-dev: ## Agregar dependencia de desarrollo (uso: make deps-add-dev PACKAGE=nombre)
	$(POETRY) add --group dev $(PACKAGE)

deps-update: ## Actualizar todas las dependencias
	$(POETRY) update

shell: ## Activar shell de Poetry
	$(POETRY) shell

health: ## Verificar health check de la API
	@echo "🏥 Verificando health check..."
	@curl -f http://localhost:$(PORT)/health || echo "❌ API no disponible"

docs: ## Abrir documentación de la API
	@echo "📖 Abriendo documentación..."
	@open http://localhost:$(PORT)/docs || echo "Visita: http://localhost:$(PORT)/docs"
