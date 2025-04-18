PROJECT_NAME = automatic_speech_recognition

# Имя файла docker-compose
COMPOSE_FILE = docker-compose.yml

# Цель по умолчанию
all: up

# Запуск сервисов
up: 
	docker-compose -f $(COMPOSE_FILE) up -d --build

# Остановка сервисов
down:
	docker-compose -f $(COMPOSE_FILE) down

# Перезапуск сервисов
restart: down up

# Проверка статуса сервисов
ps:
	docker-compose -f $(COMPOSE_FILE) ps

# Удаление неиспользуемых образов и томов (очистка)
clean: down
	docker system prune -a --volumes --force

# Все вместе
full: up down clean

# Помощь
help:
	@echo "Доступные цели:"
	@echo "  up      - Запуск сервисов"
	@echo "  down    - Остановка сервисов"
	@echo "  restart - Перезапуск сервисов"
	@echo "  clean   - Удаление неиспользуемых образов и томов"
	@echo "  full    - Запуск, остановка и очистка проекта"

.PHONY: all up down restart clean full help
