1. python3
```shell
python3 -m venv venv
source venv/bin/activate
```
2. create `.env` file
```shell
cat > .env << __ENV
JWT_SECRET_KEY=testsecretkey
ENGINE=postgres
POSTGRES_HOST=192.168.10.1
POSTGRES_PORT=5433
POSTGRES_DB=profile
POSTGRES_USER=profile
POSTGRES_PASSWORD=profilesecret
__ENV
```   
3. export variables from `.env` file
```shell
export $(cat .env | xargs)
```   
4. modules
```shell
pip install aiohttp aiohttp-jinja2 aiohttp-swagger \
    aiopg sqlalchemy marshmallow aiohttp_jwt \
    aiohttp_apispec pytest pytest-cov pytest-aiohttp
```
5. run
```shell
python3 app.py
```
6. tests
```shell
pytest -v --cov=. --cov-report=term-missing
```

# Build and run docker

1. install docker
2. build image
```shell
docker build -f Dockerfile -t profile-test ./
```
3. setup `.env` file (p.2)
4. create docker instance of postgres 
```shell
docker run -d -p 5433:5432 --name profile-postgres --env-file .env postgres:13.2-alpine
```
5. run docker image as daemon
```shell
docker run --rm -d -p 8080:8080 --env-file .env profile-api
```
6. attach to db container and create schema
```shell
```


# useful links
    * [API](http://localhost:8080/api/v1/doc)
    
