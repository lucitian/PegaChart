from __main__ import app 
from flask import request, jsonify
from flask.helpers import send_file
from flask_cors import cross_origin
from db.db_blob import BlobDatabase
from functionalities.statistical_analysis import freq_dist
from functionalities.statistical_analysis import anderson_test
from functionalities.dataset_ops import describe_dataset
from scipy import stats
import pandas as pd
import urllib.request
import numpy as np

@app.route("/api/dataset/process", methods = ['POST'])
@cross_origin()
def dataset_details():
    try:
        file = None
        data = request.form
        try:
            file = request.files['file']
        except:
            file = BlobDatabase.get_dataset(data['filepath'])

        df = pd.read_csv(file, delimiter=data['delimiter'])
        
        res = describe_dataset(df)

        return res
    except Exception as e:
        return {
            'error': str(e),
            'code': 'DATASET_PROCESS_FAIL'
        }
    
@app.route("/api/dataset/get/<filename>/<cols>", methods=['GET'])
@cross_origin()
def get_dataset(filename,cols):
    try:
        url = BlobDatabase.get_dataset(filename)
        df = pd.read_csv(url)
        df = df.fillna('')

        if df.shape[0] > 50:
            df = df[:50]

        return {
            'code': 'DATASET_GET_SUCCESS',
            'data': df.to_dict(orient='records'),
            'filename': filename,
            'filesize': urllib.request.urlopen(url).length,
            'directory': filename
        }
    except Exception as e:
        return {
            'code': 'DATASET_GET_FAIL',
            'error': str(e)
        }

@app.route("/api/dataset/study/get/<filename>", methods=['GET'])
@cross_origin()
def get_study_dataset(filename):
    try:
        url = BlobDatabase.get_study_dataset(filename)
        df = pd.read_csv(url)
        df = df.fillna('')
        
        return {
            'code': 'STUDY_DATASET_GET_SUCCESS',
            'data': df.to_dict(orient='records'),
            'filename': filename,
            'filesize': urllib.request.urlopen(url).length,
            'directory': filename
        }
    except Exception as e:
        return {
            'code': 'STUDY_DATASET_GET_FAIL',
            'error': str(e)
        }