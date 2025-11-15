.PHONY: build dev

build:
	docker compose up --build

dev:
	docker compose down
	sudo rm -rf data
	fastapi dev src/main.py