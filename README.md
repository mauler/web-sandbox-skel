# Sandbox Web Project

My personal skeleton project for testing purposes.

## Getting Started

This project is intended to run using **docker** together **docker-compose**.

The image *web* image inherits *python:3.6* most recebent image and install the python library requirements listed on requirements.txt file.

### Prerequisites

* docker
* docker-compose

### Installing

Go to the project root folder and start the service using:
```
docker-compose up
```

The project will be built and running on port "8055" you can access it on the url:

```
http://localhost:8055/
```

## Running the tests

The tests can be run using:

```
docker-compose run web python manage.py tests -k api
```

or if the "web" container is running you can re-use it using *exec* instead of *run*.

```
docker-compose exec web python manage.py tests -k api
```

## Deploy

### Heroku

Just push to heroku branch using

```
git push heroku master
```

### Docker

Rebuild the containers if requirements.txt is changed using:

```
docker-compose build --no-cache web
```

Restart the container and/or ensure is up and running

```
docker-compose restart
```
and/or
```
docker-compose up -d
```
