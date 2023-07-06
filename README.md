# SnappFood Delay Report Service
A web base service that handle delay report request at SnappFood company!


## Integrated Tools
- Python +v3.11
- Postgresql +v14
- Redis +v7
- Celery
- ELK v8.8.1
- RabbitMQ v3.12
- UWSGI
- Nginx
- Docker & Docker Compose
- Poetry (dependency management)
- Pre commit

## Run

### SFDR Web App
To run service itself, execute the following command at teh root of the project (be sure u have installed both docker and `docker compose`):
```shell
docker compose up
```
### ELK
This is an unnecessary tools to monitor log and ... . After running `SFDR` service you can run RLK by running following command:
```shell
cd ELK  # enter ELK directory!
docker compose up setup  # Just once to setup pre-hooks, for the next time you can ignore this part.
docker compose up
```

## Test
To run tests execute following command the root of the project:
```shell
docker compose up db
```
