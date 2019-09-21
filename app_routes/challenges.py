import subprocess
from subprocess import check_output
import requests
import json
from flask_restful import reqparse,Resource

apps_parser = reqparse.RequestParser()
apps_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')

# Challenges API
class apiChallenges(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/challenges
    PAYLOAD:    
    '''
    def post(self):
        args = apps_parser.parse_args()
        try:
            return args, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return args, 404

    # Get Apps list
    def get(self):
        args = apps_parser.parse_args()
        try:
            return args, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return 404
