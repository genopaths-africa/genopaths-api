```
# python virtual env 
source venv/bin/activate 

# install dependencies
pip install -r requirements.txt

# run tests
python -m pytest -s

# run dev server
python run.py

# accessing db 
docker-compose -f docker-compose-dev.yml exec genopaths_db psql -U genopaths -h localhost -d genopaths

```