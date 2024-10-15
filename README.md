# Theatre API Service 


> Django REST project 
This is a Django REST Framework (DRF) powered API for managing theatre services, such as plays, performances, tickets and related entities.


## Run service on your machine

1. Clone repository  
```shell
git clone https://github.com/Ivan-Shakhman/Theatre-API-Service
cd Theatre-API-Service
```
2. Then, create and activate .venv environment  
```shell
python -m venv env
venv\Scripts\activate
```

3. Install requirements.txt by the command below  


```shell
pip install -r requirements.txt
```

4. You need to migrate
```shell
python manage.py migrate
```
5. (Optional) Also you can load fixture data
```shell
python manage.py loaddata data.json
```
email: admin@gmail.com

password: 1qazcde3

6. And finally, create superuser and run server

```shell
python manage.py createsuperuser
python manage.py runserver # http://127.0.0.1:8000/
```

## Run with Docker

1. Clone repository  
```shell
git clone https://github.com/Ivan-Shakhman/Theatre-API-Service
cd airport-service
```
2. Create .env file and set up environment variables
```shell
DATABASE_ENGINE=postgresql
POSTGRES_PASSWORD=theatre
POSTGRES_USER=theatre
POSTGRES_DB=theatre
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=true
DATABASE_URL=postgresql://theatre:theatre:5432/theatre
```

3. Build and run docker containers 


```shell
docker-compose -f docker-compose.yaml up --build
```

## Usage
* Manage reservation and add tickets for performances (simple user) and manage (create, update etc.) performances, play end other (admin) 
* For more detail use http://localhost:8000/api/doc/swagger/ to see all endpoints

## Features
* JWT Authentication
* Admin panel /admin/
* Swagger documentation
* Managing reservations and tickets
* Creating genres, actors, plays, performances, tickets, reservations 
* Filtering and plays and performances.
* Redis usage for caching
