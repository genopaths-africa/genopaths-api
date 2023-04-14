# genopaths-api
GenoPaths API  - REST API Server for GenoPaths Platform

## Setup 
1. Create virtualenv : python -m virtualenv venv && source venv/bin/activate
2. Install dependencies: python -r requirements.txt

## Accessing migration commands 

```
flask db --help #migration help

# initialize the migration repositotry. This is already done
flask init

# Create a new migration 
flask db migrate #autogenrate revision file 
flask db revision -m "create some table"
flask db upgrate #apply migrations
flask db downgrade # undo previous migration

```