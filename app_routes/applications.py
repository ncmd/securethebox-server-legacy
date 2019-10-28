import subprocess
from subprocess import check_output
import requests
import json
from flask_restful import reqparse, Resource
import yaml

from app_controllers.creator.application import (
    Application,
    generateDeploymentYaml,
    generateIngressYaml,
    generateServiceYaml,
)
from app_controllers.applications.helm_chart import (
    HelmChart
)

app = Application()
app.loadApplications(
    [
        {'name': 'kubernetes', 'label': 'Kubernetes', 'category': 'infrastructure','category_label': 'Infrastructure'},
        {'name': 'virtual_machine', 'label': 'Virtual Machine', 'category': 'infrastructure','category_label': 'Infrastructure'},
        {'name': 'nginx', 'label': 'Nginx', 'category': 'load_balancer','category_label': 'Load Balancer'},
        {'name': 'haproxy', 'label': 'HAProxy', 'category': 'load_balancer','category_label': 'Load Balancer'},
        {'name': 'juice-shop', 'label': 'Juice Shop', 'category': 'application','category_label': 'Applications'},
        {'name': 'suricata', 'label': 'Suricata', 'category': 'ids','category_label': 'IDS'},
        {'name': 'wazuh', 'label': 'Wazuh', 'category': 'endpoint_security','category_label': 'Endpoint Security'},
        {'name': 'elk', 'label': 'ELK', 'category': 'siem','category_label': 'SIEM'},
        {'name': 'splunk', 'label': 'Splunk', 'category': 'siem','category_label': 'SIEM'}, 
    ])

apps_parser = reqparse.RequestParser()
apps_parser.add_argument('yamlData', help='{error_msg}')

# Apps API
class apiApplicationsQueryHelmChart(Resource):
     def post(self):
        args = apps_parser.parse_args()
        yd = args['yamlData']
        yData = yaml.safe_load(yd)
        hc = HelmChart()
        hc.setName(yData['name'])
        hc.setType("git")
        hc.setHost("localhost")
        # Ideally each user should have their own namespace
        hc.setNamespace("default")
        hc.setLocation(yData['url'])
        hc.loadChart()
        responsedata = hc.getChartValuesYaml()
        try:
            return responsedata, 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return args, 404

class apiApplicationsGetCategories(Resource):
     def get(self):
        args = apps_parser.parse_args()
        try:
            return app.getCategories(), 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"}
        except:
            return args, 404

# Save Helm Chart should add to the list of Applications
class apiApplicationsSaveHelmChart(Resource):
     def post(self):
        args = apps_parser.parse_args()
        yd = args['yamlData']
        yData = yaml.safe_load(yd)
        hc = HelmChart()
        hc.setName(yData['name'])
        hc.setType("git")
        hc.setHost("localhost")
        # Ideally each user should have their own namespace
        hc.setNamespace("default")
        hc.setLocation(yData['url'])
        hc.loadChart()
        hc.setChartValuesYaml("  raw: \""+yData['chart']+"\"")

        app.addApplication(
            {
                'name': yData['name'],
                'label': yData['name'].capitalize(),
                'category': 'infrastructure',
                'category_label': 'Infrastructure'
            }
        )
        try:
            return "chart was added", 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return args, 404

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
            return args, 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return args, 404

    # Get Apps list
    def get(self):
        try:
            return app.getApplicationList(), 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return 404
