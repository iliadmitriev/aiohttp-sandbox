1. python3
```shell
python3 -m venv venv
source venv/bin/activate
```
2. create `.env` file
```shell
cat > .env << __ENV
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
pip install aiohttp aiohttp-jinja2 aiohttp-swagger aiopg sqlalchemy marshmallow
```
5. run
```shell
python3 app.py
```
6. links
    * [API](http://localhost:8080/api/v1/doc)
    