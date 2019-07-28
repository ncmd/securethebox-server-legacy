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
from app_controllers.challenges.challenges import (
    challengesManageChallenge1
)

kubernetes_parser = reqparse.RequestParser()
kubernetes_parser.add_argument('action', choices=('apply','delete'), help='{error_msg}')
kubernetes_parser.add_argument('userName', help='{error_msg}')
kubernetes_parser.add_argument('clusterName', choices=('us-west1-a'), help='{error_msg}')
kubernetes_parser.add_argument('serviceName', help='{error_msg}')

# Kubernetes API
class apiKubernetes(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/kubernetes/challenges/1
    PAYLOAD:    { action: deploy | delete }
    '''
    def post(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            challengesManageChallenge1(args['clusterName'],args['userName'],args['action'])
            return args, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return args, 404
    
    def get(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            return args, 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"}
        except:
            return args, 404
