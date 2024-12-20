help: ##@Help Show this help
	cat Makefile

test: ## test
	pytest

env:
	cp .env.example .env

migrate:  ##@Database Do all migrations in database
	cd app && alembic upgrade head

open_db:
	docker exec -it db psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

test:
	python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
