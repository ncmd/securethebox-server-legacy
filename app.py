from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import time
import json
import requests
import os

from app_routes.kubernetes import ( 
    apiKubernetes 
)
from app_routes.solutions import (
    apiSolutions
)

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# API Paths
api.add_resource(apiKubernetes, '/api/kubernetes/challenges/<challenge_id>')
api.add_resource(apiSolutions, '/api/solutions/challenges/<challenge_id>')

if __name__ == '__main__':
    app.run(debug=True)
