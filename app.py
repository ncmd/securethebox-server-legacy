from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import subprocess

app = Flask(__name__)
api = Api(app)

# def executeShellCommandWithStdout(command):
#     print("Executing Shell Command!",command)
#     try:
#         output = check_output(command, stderr=STDOUT).decode()
#         print("Executed...")
#         abort(404, message=str(output))
#     except CalledProcessError as e:
#         output = e.output.decode()
#         print("Failed...")
#         abort(404, message=str(output))

def generateKubernetesServicesYaml(serviceName, userName, clusterName):
    print("Generating Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/01_deployment.py {userName} {serviceName} {clusterName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/02_service.py {userName} {serviceName} {clusterName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/03_ingress.py {userName} {serviceName} {clusterName}"],shell=True).wait()

def deleteKubernetesServicesYaml(serviceName, userName, clusterName):
    print("Deleting Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def manageKubernetesServicesPod(serviceName, userName, clusterName, action):
    print(action,"Services Pod",clusterName,serviceName,userName)
    subprocess.Popen([f"/app/vendor/google-cloud-sdk/bin/kubectl {action} -f /app/kubernetes-deployments/service/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"/app/vendor/google-cloud-sdk/bin/kubectl {action} -f /app/kubernetes-deployments/service/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"/app/vendor/google-cloud-sdk/bin/kubectl {action} -f /app/kubernetes-deployments/service/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def manageChallenge1(userName,clusterName, action):
    print(action,"Challenge 1",clusterName,userName)
    if action == 'apply':
        # 1. Generate Yaml Files
        generateKubernetesServicesYaml('nginx-modsecurity',userName,clusterName)
        generateKubernetesServicesYaml('juice-shop',userName,clusterName)
        generateKubernetesServicesYaml('splunk',userName,clusterName)
        # 2. Deploy Service pods
        manageKubernetesServicesPod('nginx-modsecurity', userName, clusterName, action)
        manageKubernetesServicesPod('juice-shop', userName, clusterName, action)
        manageKubernetesServicesPod('splunk', userName, clusterName, action)
    elif action == 'destroy':
        # 1. Destroy Service Pods
        manageKubernetesServicesPod('nginx-modsecurity', userName, clusterName, action)
        manageKubernetesServicesPod('juice-shop', userName, clusterName, action)
        manageKubernetesServicesPod('splunk', userName, clusterName, action)
        # 2. Delete Yaml Files
        deleteKubernetesServicesYaml('nginx-modsecurity',userName,clusterName)
        deleteKubernetesServicesYaml('juice-shop',userName,clusterName)
        deleteKubernetesServicesYaml('splunk',userName,clusterName)
        
# def manageKubernetesTraefik(action):
#         funcList = [
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/01_permissions.yml"]),
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/02_cluster-role.yml"]),
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/03_config.yml"]),
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/04_deployment.yml"]),
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/05_service.yml"]),
#             executeShellCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", action, "-f" ,"/app/kubernetes-deployments/ingress/traefik/06_ingress.yml"])
#             ]
#         return funcList

parser = reqparse.RequestParser()
parser.add_argument('action', choices=('apply','destroy'), help='{error_msg}')
parser.add_argument('userName', help='{error_msg}')
parser.add_argument('clusterName', help='{error_msg}')

# Kubernetes API
class Kubernetes(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/kubernetes/challenges/1
    PAYLOAD:    { action: deploy|destroy }
    '''
    def post(self, challenge_id):
        args = parser.parse_args()
        try:
            manageChallenge1(args['userName'],args['clusterName'],args['action'])
            return args, 201
        except:
            return args, 404

api.add_resource(Kubernetes, '/api/kubernetes/challenges/<challenge_id>')

if __name__ == '__main__':
    app.run(debug=True)
