# Command to build the Docker images
dev_build:
	docker build -t mysql-image .

# Command to bring up all containers using docker-compose
dev_up:
	docker compose up -d

# Command to stop and remove all containers
dev_down:
	docker compose down

# Command to show the status of running containers
dev_ps:
	docker ps