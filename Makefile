.PHONY: build dev

build:
	docker compose up --build

dev:
	fastapi dev src/main.py