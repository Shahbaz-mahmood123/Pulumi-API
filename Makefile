# Makefile for Docker Compose App

# Variables
COMPOSE_FILE := compose.yaml

# Targets
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run              : Start the Docker containers"
	@echo "  down            : Stop and remove the Docker containers"
	@echo "  build           : Build the Docker images"
	@echo "  logs            : View logs of running containers"
	@echo "  exec            : Execute a command in a running container (e.g., make exec service_name command=<command>)"
	@echo "  test            : Run tests (if applicable)"
	@echo "  clean           : Remove all generated files and containers"

.PHONY: run
run:
	docker-compose -f $(COMPOSE_FILE) up -d

.PHONY: down
down:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: build
build:
	docker-compose -f $(COMPOSE_FILE) build

.PHONY: logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

.PHONY: exec
exec:
	docker-compose -f $(COMPOSE_FILE) exec $(service_name) $(command)

.PHONY: test
test:
	# Add your test commands here

.PHONY: clean
clean: down
	# Add any cleanup commands here

