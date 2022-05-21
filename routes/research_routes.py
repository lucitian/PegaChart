from __main__ import app
from random import randint
from flask import request
from flask_cors import cross_origin
from db.db_blob import BlobDatabase
from objects.study import Study
from objects.user import User
from objects.research import Research
from os.path import dirname, realpath
from functionalities.statistical_analysis import *
from functionalities.machine_learning import *
from functionalities.interpretation import interpret
from functionalities.dataset_ops import describe_dataset
from sklearn.model_selection import train_test_split
import pandas as pd
import warnings
import io

warnings.filterwarnings('ignore')

@app.route("/api/research/<id>")
@cross_origin()
def fetch_research(id):
    try:
        research = Research(id)

        if not research.is_registered:
            return {
                'error': 'Research does not exist.',
                'code': 'RESEARCH_NOT_EXIST'
            }
        
        data = research.get_research()
        data['research_url'] = BlobDatabase.get_dataset(data['dataset'])

        authors = []

        for author in data['authors']:
            u = User(author['user']).get_user()['username']
            authors.append({
                'user': author['user'],
                'username': u,
                'type': author['type']
            })
        
        data['authors'] = authors
        
        return {
            'data' : data,
            'code': "RESEARCH_GET_SUCCESS",
        }
    except Exception as e:
        return {
            'code': "RESEARCH_GET_FAIL",
            'message': str(e)
        }

@app.route("/api/researches", methods=["POST"])
@cross_origin()
def fetch_researches():
    try:
        data = request.get_json()

        user = User(data['_id'])
        
        researches = user.research_papers
        
        return {
            'code': 'RESEARCHES_GET_SUCCESS',
            'researches': researches
        }
        
    except Exception as e:
        return {
            'code': 'RESEARCHES_GET_FAIL',
            'error': str(e)
        }
    

@app.route("/api/research/new", methods=["POST"])
@cross_origin()
def add_research():
    try:
        data = request.form

        uuid = randint(10000000, 99999999)

        file = request.files['dataset']
        file_name = f"{uuid}_{file.filename}"

        BlobDatabase.upload_dataset(file_name, file)

        df = pd.read_csv(BlobDatabase.get_dataset(file_name), delimiter=data['delimiter'])
        details = describe_dataset(df)

        res = Research.register_research(
            research_name = data['research_name'],
            research_description = data['research_description'],
            dataset = file_name,
            dataset_details = details,
            delimiter = data['delimiter'],
            author = data['author'],
            created_at = data['created_at']
        )

        if not res['status']:
            return {
                'message': res['message'],
                'code': 'RESEARCH_SAVE_UNEXPECTED_FAILURE',
                'type': 'error'
            }
        
        return {
            'message': 'Research saved successfully.',
            'code': 'RESEARCH_SAVE_SUCCESS',
            'type': 'success',
            'uuid': res['_id']
        }
    except Exception as e:
        return {
            'error': str(e),
            'code': 'RESEARCH_SAVE_INTERNAL_FAILURE',
            'type': 'error'
        }

@app.route("/api/research/study/new", methods=["POST"])
@cross_origin()
def add_study():
    try:
        data = request.get_json()

        uuid = randint(10000000, 99999999)

        compute_res = None
        regression_configuration = None
        graphing = None
        
        research = Research(data['research_id'])
        
        df = pd.read_csv(BlobDatabase.get_dataset(research.get_research()['dataset']), delimiter=research.get_research()['delimiter'])

        columns = data['columns']
        options = data['options']

        interprets = []
        changes = []
        null_deleted = 0 
        null_replaced = 0
        outlier_deleted = 0
        outlier_replaced = 0
        for col in columns:
            for option in options:
                if option['column'] == col:
                    if option['null_option']['method'] == 'delete':
                        init_rows = int(df.shape[0])
                        df.dropna(subset=[col], inplace=True)
                        null_deleted = init_rows - int(df.shape[0])
                    elif option['null_option']['method'] == 'replace':
                        init_na = df[col].isna().sum()
                        if option['null_option']['replace_by'] == 'mean':
                            df[col].fillna(df[col].mean(), inplace=True)
                        elif option['null_option']['replace_by'] == 'median':
                            df[col].fillna(df[col].median(), inplace=True)
                        elif option['null_option']['replace_by'] == 'mode':
                            df[col].fillna(df[col].mode(), inplace=True)
                        null_replaced = int(init_na - df[col].isna().sum())
                    elif option['null_option']['method'] == 'nothing':
                        pass
                    if df[col].isnull().values.any():
                        return {
                            'code': 'STUDY_ADD_FAIL',
                            'error': f'Statisfy detected null values on the variable {col} which may be detrimental to the computation process. Please clean your dataset first.'
                        }
                    
                    low = df[col].quantile(0.10)
                    hi = df[col].quantile(0.90)

                    if option['outlier_option']['method'] == 'delete':
                        index = df[col][(df[col] < low) | (df[col] > hi)].index 
                        init_rows = int(df.shape[0])
                        df.drop(index, inplace=True)
                        outlier_deleted = init_rows - int(df.shape[0]) 
                    elif option['outlier_option']['method'] == 'replace':
                        init_outliers = len(df[col][(df[col] < low) | (df[col] > hi)])
                        if option['outlier_option']['method'] == 'mean':
                            df[col].where(df[col] < low, df[col].mean(), inplace=True)
                            df[col].where(df[col] > hi, df[col].mean(), inplace=True)
                        elif option['outlier_option']['method'] == 'median':
                            df[col].where(df[col] < low, df[col].median(), inplace=True)
                            df[col].where(df[col] > hi, df[col].median(), inplace=True)
                        elif option['outlier_option']['method'] == 'mode':
                            df[col].where(df[col] < low, df[col].mode(), inplace=True)
                            df[col].where(df[col] > hi, df[col].mode(), inplace=True)
                        outlier_replaced = init_outliers - (init_outliers - len(df[col][(df[col] < low) | (df[col] > hi)]))
                    elif option['null_option']['method'] == 'nothing':
                        pass

            changes.append(
                {
                    'column': col,
                    'null_deleted': null_deleted,
                    'null_replaced': null_replaced,
                    'outlier_deleted': outlier_deleted,
                    'outlier_replaced': outlier_replaced
                }
            )
            null_deleted = 0 
            null_replaced = 0
            outlier_deleted = 0
            outlier_replaced = 0

        if data['test_type'] == 'Pearson R Correlation Test':
            if len(columns) != 2:
                return {
                    'code': 'STUDY_ADD_FAIL',
                    'error': 'Pearson R only accepts two variables. Please make sure to only select two columns to analyze.'
                }
            
            compute_res = pearsonr(df[columns[0]], df[columns[1]])
        elif data['test_type'] == 'Linear Regression':
            if int(data['iterations']) > 10000:
                return {
                    'code': 'STUDY_ADD_FAIL',
                    'error': 'The number of iterations is too big for the server to handle. Please reduce the number of iterations and try again.',
                }
            new_cols = columns.copy()
            new_cols.remove(data['label'])
            
            X = df[new_cols]
            y = df[data['label']]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(data['testSize'])/100, random_state=99)

            #train = pd.concat([X_train, y_train], axis=1).to_csv((f"LINREG_TRAIN_{uuid}_{Research(data['research_id']).get_research()['dataset']}"))
            #test = pd.concat([y_train, y_test], axis=1).to_csv((f"LINREG_TEST_{uuid}_{Research(data['research_id']).get_research()['dataset']}"))

            model = LinearRegression()
            model.fit_data(X_train, y_train)
            model.gradient_descent(iterations = int(data['iterations']), learning_rate=float(data['learningRate']))

            reactified_cost_history = []
            reactified_gradient_history = []

            for _  in range(len(model.cost_history)):
                reactified_cost_history.append({
                    'x': _+1, 
                    'y': model.cost_history[_][0]
                })

                reactified_gradient_history.append({
                    'x': float(model.theta_history[_][0][0]),
                    'y': abs(float(model.gradient_history[_][0][0]))
                })

            pred = model.predict(X_test)

            compute_res = (('R Squared', model.r_squared(y_test, pred)), 
                ('R Squared (%)', model.r_squared(y_test, pred)*100), 
                ('Mean Absolute Percentage Error', model.mape(y_test, pred))
            )

            regression_configuration = {
                'test_size': data['testSize'],
                'iterations': data['iterations'],
                'learning_rate': data['learningRate']
            }

            graphing = {
                'cost_history': reactified_cost_history,
                'gradient_history': reactified_gradient_history
            }
        elif data['test_type'] == 'Spearman Rho Rank Correlation Test':
            if len(columns) != 2:
                return {
                    'code': 'STUDY_ADD_FAIL',
                    'error': 'Spearman Rho only accepts two variables. Please make sure to only select two columns to analyze.'
                }
            
            compute_res = spearmanrho(df[columns[0]], df[columns[1]])

        res = Study.new_study(
            _id = uuid,
            study_name = data['study_name'],
            research_id = data['research_id'],
            created_by = data['created_by'],
            test_type = data['test_type'],
            study_dataset = f"{uuid}_{Research(data['research_id']).get_research()['dataset']}",
            created_at = data['created_at'],
            columns = data['columns'],
            study_description = data['study_description'],
            interpretations = interpret(data['test_type'], compute_res),
            variables = compute_res,
            options = data['options'],
            changes = changes,
            regression_configuration = regression_configuration,
            graphing = graphing
        )

        if not res['status']:
            return {
                'code': 'STUDY_ADD_FAIL',
                'error': f"An error occurred while calculating. Error message: {res['message']}",
            }

        df = df[[col for col in columns]]
        blob = io.StringIO(df.to_csv(index=False))
        BlobDatabase.upload_study_dataset(f"{uuid}_{Research(data['research_id']).get_research()['dataset']}", blob.read())

        return {
            'code': 'STUDY_ADD_SUCCESS',
            'message': 'Study is successfully registered and computed.',
        }

    except TypeError as e:
        return {
            'code': 'STUDY_ADD_FAIL',
            'error': f"An error occurred while calculating. Error message: {str(e)}",
        }
        
    except Exception as e:
        return {
            'code': 'STUDY_ADD_FAIL',
            'error': str(e),
        }

@app.route("/api/research/delete", methods=["POST"])
@cross_origin()
def delete_research():
    try:
        data = request.get_json()

        research = Research(data['_id'])
        r_obj = research.get_research()

        studies = research.studies

        for study in studies:
            s = Study(study['_id'])
            BlobDatabase.delete_study_dataset(s.get_study()['study_dataset'])
            s.delete_study()
        
        BlobDatabase.delete_dataset(r_obj['dataset'])

        research_name = r_obj['research_name']

        research.delete_research()

        return {
            'deleted_research': research_name,
            'code': 'RESEARCH_DELETE_SUCCESS',
            'message': f'Research {research_name} has been deleted successfully.'
        }
    except Exception as e:
        return {
            'code': 'RESEARCH_DELETE_FAILED',
            'message': str(e)
        }

@app.route("/api/research/study/fetch", methods=["POST"])
@cross_origin()
def get_studies():
    try:
        data = request.form 

        research = Research(data['research_id'])

        return {
            'code': 'STUDY_GET_SUCCESS',
            'data': research.studies,
        }
    except Exception as e:
        return {
            'code': 'STUDY_GET_FAIL',
            'message': str(e),
        }

@app.route("/api/research/study/delete", methods=["POST"])
@cross_origin()
def delete_study():
    try:
        data = request.get_json()

        study = Study(data['_id']).get_study()
        name = study['study_name']

        BlobDatabase.delete_study_dataset(study['study_dataset'])
        Study(data['_id']).delete_study()

        return {
            'code': 'STUDY_DELETE_SUCCESS',
            'message': f'Study {name} successfully deleted.'
        }
    except Exception as e:
        return {
            'code': 'STUDY_DELETE_FAIL',
            'message': str(e)
        }
