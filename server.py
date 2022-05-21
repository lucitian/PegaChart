from flask import Flask, request
from flask_cors import CORS
from secret import SECRET_KEY
import os

# app initialization
app = Flask(__name__)
cors = CORS(app)

# app configurations
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = SECRET_KEY

# connect routes to app
from routes import user_routes, research_routes, auth_routes, dataset_routes

# run the app
if __name__ == "__main__":
    app.run(debug=True, threaded=True)