import argparse
import os
import logging
import sys 
import csv 
import json
import re 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import rasterio
import pandas as pd 

logging = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='validate-transform')
parser.add_argument("-o","--outputdir", help="provide output directory", default=os.getcwd())
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-c","--config", help="provide configuration", required=True, type=str)
requiredNamed.add_argument("-d","--data", help="provide configuration", required=True, type=str)

args = parser.parse_args()
datafile = args.data 
configfile = args.config
config_object = json.load(open(configfile))
output_dir = args.outputdir

logging.info('Running validate-transform.py')  

##TODO: validate json format 

def drop(record, field, expr=None):
    """
    Drop a field from the record if the expression evaluates to True.
    """
    if field in record:
        del record[field]
    return record

def uppercase(record, field):
    if field in record:
        record[field] = record[field].upper()
    return record

def lowercase(record, field):
    if field in record:
        record[field] = record[field].lower()
    return record

def mask(record, field, mark='*'):
    if field in record:
        record[field] = '***'
    return record

def drop_if(record, field, value):
    if field in record and record[field] == value:
        del record[field]
    return record

def risk(lat, lon):
    """
    Compute the location risk score based on the population density tiff file.
    """
    try:

        #@todo: check if the file exists
        dat = rasterio.open(r"uga_ppp_2020_constrained.tif")
        # read all the data from the first band
        z = dat.read()[0]
        idx = dat.index(lon, lat, precision=1E-6)    
        # return dat.xy(*idx), z[idx]
        return z[idx]
    except:
        return -1

def concat(record, newfield, *kargs, sep=','):
    for arg in kargs:
        if arg in record:
            record[newfield] = sep.join([record[newfield], record[arg]])
    return record

def validate(record, config):

    #get the validation rules
    validate_fields = config['validate']['fields']

    ##get fields with validation rules
    # validation_list = list(validate_fields.keys())
    for key in validate_fields.keys():
        val = record[key]
        if(re.match(r'LIKE\(\)', validate_fields[key])):
            re.match(r'LIKE\(\)', [key])
        if(re.match(r'DROP', validate_fields[key])):
            record = drop(record, key)

    return record 

def transform(record, config):
    validate_config = config['transform']

    return record

def lookup_district(latitude, longitude):
    #point = Point(0.5, 0.5)
    #polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    #polygon.contains(point)
    return 'DISTRICT NAME'

pd = pd.read_csv(datafile)

#risk 
transformers = config_object['transform']
for tr in transformers:
    if '$risk' in tr: #risk(lat, log)
        lat_field, lon_field = tr['$risk']
        pd['risk'] = pd.apply(lambda x: risk(x[lon_field], x[lat_field]), axis=1)
        print(f'lat: {lat_field}, log: {lat_field}')

    if '$drop' in tr: #drop([field1, field2, ...])
        fields = tr['$drop']
        pd = pd.drop(tr['$drop'], axis=1)

    if '$mask' in tr: #mask([field1, field2, ...], '****')
        fields, mask = tr['$mask']
        # pd[fields] = pd[fields].mask(pd[fields].notnull(), mark)
        pd[fields] = pd.apply(lambda x: mask, axis=1)

    if '$dropif' in tr: #dropif([field], condition)
        print(tr['$dropif'])
        fields, condition = tr['$dropif']
        if '$gt' in condition: 
            pd = pd[pd[fields] > condition['$gt']]
        if '$lt' in condition: 
            pd = pd[pd[fields] < condition['$lt']]
        if '$eq' in condition: 
            pd = pd[pd[fields] == condition['$eq']]


output_file = os.path.join(output_dir, datafile)
pd.to_csv(output_file, index=False)

print(pd)
