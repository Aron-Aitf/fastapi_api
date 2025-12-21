build:
	docker compose up --build

dev:
	source /home/aron/main/python/venv/fastapi/bin/activate
	fastapi dev src/main.py

clean_logs:
	rm -r logs