.PHONY: all build run down lint

PREFIX=docker compose --env-file .env -f deployments/docker-compose.yml

all: build run

build:
	${PREFIX} build

run:
	${PREFIX} up -d

down:
	${PREFIX} down --volumes

rebuild: down all

logs:
	${PREFIX} logs ${AT}

ps:
	${PREFIX} ps -a

lint:
	autopep8 --in-place -r .
