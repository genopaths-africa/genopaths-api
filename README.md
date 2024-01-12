# genopaths-api
GenoPaths API  - REST API Server for GenoPaths Platform

## Setup 
1. Create virtualenv : python -m virtualenv venv && source venv/bin/activate
2. Install dependencies: pip install -r requirements.txt

## Accessing migration commands 

```
flask db --help #migration help

# initialize the migration repositotry. This is already done
flask init

# Create a new migration 
flask db migrate #autogenrate revision file 
flask db revision -m "create some table"
flask db upgrade #apply migrations
flask db downgrade # undo previous migration

```

## Using docker in dev 

```
docker-compose -f docker-compose-dev.yml

#dconnect to postgresql
docker-compose -f docker-compose-dev.yml exec genopaths_db psql -U genopaths  -h localhost -d genopaths
```

## Access database 
```
docker-compose -f docker-compose-dev.yml exec genopaths_db psql -U genopaths -h localhost -d genopaths
```

## Running tests

```
python -m pytest -s
```

# Seeding data 

```
flask seed run
``` 