# Docker Flask Celery Redis

A basic [Docker Compose](https://docs.docker.com/compose/) template for orchestrating a [Flask](http://flask.pocoo.org/) application & a [Celery](http://www.celeryproject.org/) queue with [Redis](https://redis.io/)

### Installation

```bash
git clone https://github.com/mattkohl/docker-flask-celery-redis
```

### Local
```shell
pip install -r requirements.txt
python -m entrypoint.py
```

### Build & Launch

```bash
docker-compose up -d --build
```

This will expose the Flask application's endpoints on port `5001` as well as a [Flower](https://github.com/mher/flower) server for monitoring workers on port `5555`

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

To shut down:

```bash
docker-compose down
```

To change the endpoints, update the code in [api/app.py](api/src/app.py)

Task changes should happen in [queue/tasks.py](main.py) 

---

adapted from [https://github.com/itsrifat/flask-celery-docker-scale](https://github.com/itsrifat/flask-celery-docker-scale)

## Troubleshooting
Problems when loading keycloak (mixed content):
https://keycloak.discourse.group/t/keycloak-in-docker-behind-reverse-proxy/1195/13

[Securing Node.js Express REST APIs with Keycloak](https://medium.com/devops-dudes/securing-node-js-express-rest-apis-with-keycloak-a4946083be51)