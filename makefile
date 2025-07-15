all: up

copy_env:
	cat example.env .env

up: 
	docker-compose -f $(COMPOSE_FILE) up -d --build

down:
	docker-compose -f $(COMPOSE_FILE) down

build_torch_image:
	docker build -t torch_image -f ./deploy/Dockerfile.torch .

build_backend_image:
	docker build -t backend_image -f ./deploy/Dockerfile.backend .

build_frontend_image:
	docker build -t frontend_image -f ./deploy/Dockerfile.frontend .

build_llm_image:
	docker build -t llm_image -f ./deploy/Dockerfile.llm .

full_start:
	copy_env
	build_torch_image
	build_llm_image
	build_backend_image
	build_frontend_image
	docker-compose up -d
	
help:
	@echo "Доступные цели:"
	@echo "  all            - (По умолчанию) Запускает сервисы."
	@echo "  up             - Запускает сервисы (с пересборкой образов, если необходимо)."
	@echo "  down           - Останавливает сервисы."
	@echo "  copy_env       - Копирует example.env в .env"
	@echo "  full_start     - Копирует env и запускает сервисы."
	@echo "  build_*_image  - Собирает образ сервиса. Варианты *: torch, backend, frontend, llm"

.PHONY: all up down help
