import subprocess
from subprocess import check_output
import requests
import json
from flask_restful import reqparse,Resource

from app_controllers.infrastructure.kubernetes import (
    kubernetesGetPodId
)
from app_controllers.infrastructure.docker import (
    dockerGetContainerId
)


solutions_parser = reqparse.RequestParser()
solutions_parser.add_argument('solutionData', help='{error_msg}')

# Takes in the submission for Challenge1
# def submissionChallenge1(challengeNumber, userName, solutionData):
def submissionChallenge1(solutions):
    print("SOLUTION:",solutions)
    for i in solutions:
        print(i,solutions[i])

# Solutions API
class apiSolutions(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/kubernetes/challenges/1
    PAYLOAD:    { action: deploy | delete }
    '''
    def post(self, challenge_id):
        # args = solutions_parser.parse_args()
        try:
            json_data = request.get_json(force=True)
            submissionChallenge1(json_data)
            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404