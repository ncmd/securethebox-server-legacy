import subprocess
from subprocess import check_output
import requests
import json
from flask_restful import reqparse,Resource
import yaml

from app_controllers.creator.application import (
    Application,
    generateDeploymentYaml,
    generateIngressYaml,
    generateServiceYaml,
)


app = Application()
app.loadApplications(['nginx','haproxy', 'juice-shop', 'suricata', 'wazuh', 'elk', 'splunk'])

apps_parser = reqparse.RequestParser()
apps_parser.add_argument('yamlData', help='{error_msg}')
# apps_parser.add_argument('yamlDataDeployment', help='{error_msg}')
# apps_parser.add_argument('yamlDataIngress', help='{error_msg}')
# apps_parser.add_argument('yamlDataService', help='{error_msg}')

# Apps API
class apiApplications(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/apps
    PAYLOAD:    { yamlData:  }
    '''
    def post(self, app_id):
        args = apps_parser.parse_args()
        try:
            yd = args['yamlData']
            jyd = json.loads(yd)
            # jyd = json.loads(yd)
            print(jyd)
            # yData = yaml.safe_load(yd)
            # yaml.dump(yData, f, default_flow_style=False)
            # print(yData)
            # generateDeploymentYaml(yData)
            # generateIngressYaml(args['yamlDataIngress'])
            # generateServiceYaml(args['yamlDataService'])
            return args, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return args, 404

    # Get Apps list
    def get(self):
        try:
            return app.getApplicationList(), 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return 404
