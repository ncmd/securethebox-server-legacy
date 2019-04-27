from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
import time

'''
Need to fix 04_configuration.py
Not parsing to write to file
python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa
'''


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

def generateKubernetesIngressYaml(clusterName,serviceName):
    print("Generating Yaml",clusterName,serviceName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/01_permissions.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/02_cluster-role.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/03_config.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/04_deployment.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/05_service.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/06_ingress.py {clusterName} {serviceName}"],shell=True).wait()

def generateKubernetesServicesYaml(clusterName, serviceName, userName):
    print("Generating Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/02_service.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/03_ingress.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def deleteKubernetesIngressYaml(clusterName, serviceName):
    print(f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def deleteKubernetesServicesYaml(clusterName,serviceName, userName):
    print(f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def manageKubernetesIngressPod(clusterName,serviceName, action):
    print(f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def manageKubernetesServicesPod(clusterName, serviceName, userName, action):
    print(action,"Services Pod",clusterName,serviceName,userName)
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def generateNginxConfig(clusterName,serviceName,userName):
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/04_configuration.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

# Install Nginx on Container/Pod
def setupWAF(clusterName, serviceName, userName):
    print("setupWAF!!!",serviceName,userName)
    time.sleep(20)
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    for i in pod_list:
        if f'{serviceName}-{userName}' in str(i):
            print(str(i))
            pod_id = str(i)
    print([f"kubectl cp ./kubernetes-deployments/services/{serviceName}/nginx.conf default/"+pod_id+":/etc/nginx/nginx.conf"])
    generateNginxConfig(clusterName,serviceName,userName)
    subprocess.Popen([f"kubectl cp ./kubernetes-deployments/services/{serviceName}/04_{clusterName}-{serviceName}-{userName}-nginx.conf default/"+pod_id+":/etc/nginx/nginx.conf"],shell=True).wait()
    subprocess.Popen([f"kubectl exec -it "+pod_id+" -- nginx -s reload"],shell=True).wait()
    # kubectl exec -it nginx-modsecurity-oppa-6b7f54ff8-fszg6 -- /bin/sh
    # kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/nginx.conf default/nginx-modsecurity-oppa-6b7f54ff8-fszg6:/etc/nginx/nginx.conf

# Install Cloudcmd on Container/Pod
def setupCLOUDCMD(clusterName, serviceName, userName):
    print("setupCLOUDCMD!!!",clusterName,serviceName,userName)
    time.sleep(20)
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    for i in pod_list:
        if f'{serviceName}-{userName}' in str(i):
            print(str(i))
            pod_id = str(i)

    if serviceName == 'nginx-modsecurity':
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- apk add nodejs nodejs-npm"],shell=True).wait()
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- forever start /usr/bin/cloudcmd --port 6000"],shell=True).wait()
    elif serviceName == 'juice-shop':
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- forever start /usr/local/bin/cloudcmd --port 7000"],shell=True).wait()





def manageChallenge1(clusterName, userName, action):
    print(action,"Challenge 1",clusterName,userName)
    if action == 'apply':
        # 1. Generate Yaml Ingress Files
        generateKubernetesIngressYaml(clusterName, 'traefik')
        # 2. Deploy Ingress Pods
        manageKubernetesIngressPod(clusterName, 'traefik', action)
        time.sleep(20)
        # # 3. Generate Yaml Service Files
        generateKubernetesServicesYaml(clusterName, 'nginx-modsecurity',userName)
        generateKubernetesServicesYaml(clusterName, 'juice-shop',userName)
        generateKubernetesServicesYaml(clusterName, 'splunk',userName)
        # # 4. Deploy Service pods
        manageKubernetesServicesPod(clusterName,'nginx-modsecurity', userName, action)
        setupWAF(clusterName, 'nginx-modsecurity', userName)
        setupCLOUDCMD(clusterName, 'nginx-modsecurity', userName)

        manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        setupCLOUDCMD(clusterName, 'juice-shop', userName)
        manageKubernetesServicesPod(clusterName,'splunk', userName, action)

    elif action == 'delete':
        # 1. Delete Ingress Pods
        manageKubernetesIngressPod(clusterName,'traefik', action)
        # 2. Generate Yaml Ingress Files
        deleteKubernetesIngressYaml(clusterName,'traefik')
        # 3. Delete Service Pods
        manageKubernetesServicesPod(clusterName, 'nginx-modsecurity',userName, action)
        manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        manageKubernetesServicesPod(clusterName, 'splunk', userName, action)
        # 4. Delete Yaml Files
        deleteKubernetesServicesYaml(clusterName,'nginx-modsecurity',userName)
        deleteKubernetesServicesYaml(clusterName,'juice-shop',userName)
        deleteKubernetesServicesYaml(clusterName,'splunk',userName)

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
parser.add_argument('action', choices=('apply','delete'), help='{error_msg}')
parser.add_argument('userName', help='{error_msg}')
parser.add_argument('clusterName', choices=('us-west1-a'), help='{error_msg}')
parser.add_argument('serviceName', help='{error_msg}')

# Kubernetes API
class Kubernetes(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/kubernetes/challenges/1
    PAYLOAD:    { action: deploy|Delete }
    '''
    def post(self, challenge_id):
        args = parser.parse_args()
        try:
            manageChallenge1(args['clusterName'],args['userName'],args['action'])
            return args, 201
        except:
            return args, 404
    
    def get(self, challenge_id):
        args = parser.parse_args()
        try:
            setupWAF(args['clusterName'],args['serviceName'],args['userName'])
            return args, 201
        except:
            return args, 404

api.add_resource(Kubernetes, '/api/kubernetes/challenges/<challenge_id>')

if __name__ == '__main__':
    app.run(debug=True)
