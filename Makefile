include .env

run:
	-docker compose up

down:
	-docker compose down

init:
	mkdir $(PROJECT_DIR)
	docker compose -f compose-init.yaml up
	docker compose -f compose-init.yaml down
