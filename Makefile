.PHONY: up down seed init test logs-api logs-worker validate-graph

up:
	docker compose up -d --build

down:
	docker compose down

init:
	docker compose exec api python scripts/init_arangodb.py

seed:
	docker compose exec api python scripts/seed_data.py

test:
	docker compose exec api pytest -q

logs-api:
	docker compose logs -f api

logs-worker:
	docker compose logs -f worker

validate-graph:
	python3 scripts/validate_dependencies.py
