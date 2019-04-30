from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
import time

'''
1. /opt/splunkforwarder/etc/system/local/inputs.conf
not getting updated...

2. need to fix time, timestamp is wrong...

1. Splunk needs to work (it does, but needed portforwarding)
- https://github.com/splunk/docker-splunk/tree/develop/test_scenarios/kubernetes
- kubectl port-forward splunk-oppa-7f7b975c4-m52x9 8000:8000

4. Splunk enable receiving (9997 is already enabled for receiving)
- https://docs.splunk.com/Documentation/Forwarder/7.2.6/Forwarder/Enableareceiver
kubectl exec -it splunk-oppa-7f7b975c4-l6wpx -- /bin/bash
/opt/splunk/bin/splunk add monitor /var/log/challenge1/nginx-oppa.log
/opt/splunk/bin/splunk add monitor /var/log/challenge1/modsecurity-oppa.log
/opt/splunk/bin/splunk enable listen 9777 -auth admin:Changeme
/opt/splunk/bin/splunk restart
/opt/splunk/etc/system/local/inputs.conf
[default]
host = splunk-oppa-7f7b975c4-m52x9
[splunktcp://9997]
disabled = 0


/opt/splunk/bin/splunk set web-port 80

4. Splunk Universal Forwarder setup to parse Persistent Volume /var/logs/challenge1
- https://docs.splunk.com/Documentation/Forwarder/7.2.6/Forwarder/HowtoforwarddatatoSplunkEnterprise
- https://pansplunk.readthedocs.io/en/latest/universal_forwarder.html
kubectl exec -it splunk-universal-forwarder-oppa-747d54cb-mkkc4 -- /bin/bash

/opt/splunkforwarder/bin/splunk
- kubectl exec -it splunk-universal-forwarder-oppa-747d54cb-db9ws -- /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'
- kubectl exec -it splunk-universal-forwarder-oppa-747d54cb-db9ws -- /opt/splunkforwarder/bin/splunk add forward-server splunk-oppa:9777
/opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/nginx-oppa.log
/opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/modsecurity-oppa.log

/opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1

edit /opt/splunkforwarder/etc/system/local/inputs.conf
[monitor:///var/log/challenge1/nginx-oppa.log]
sourcetype = nginx

[monitor:///var/log/challenge1/modsecurity-oppa.log]
sourcetype = modsecurity

kubectl delete po,svc,deployment --all
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
    print("Generating Ingress Yaml",clusterName,serviceName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/01_permissions.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/02_cluster-role.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/03_config.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/04_deployment.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/05_service.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/06_ingress.py {clusterName} {serviceName}"],shell=True).wait()

def generateKubernetesServicesYaml(clusterName, serviceName, userName):
    print("Generating Service Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/02_service.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/03_ingress.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def deleteKubernetesIngressYaml(clusterName, serviceName):
    print("Deleting Ingress Yaml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def deleteKubernetesServicesYaml(clusterName,serviceName, userName):
    print("Deleting Service Yaml")
    # print(f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def manageKubernetesIngressPod(clusterName,serviceName, action):
    print(action,"Ingress Pod:",serviceName)
    # print(f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def manageKubernetesServicesPod(clusterName, serviceName, userName, action):
    print(action,"Service Pod:",serviceName)
    if action == 'apply':
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    # time.sleep(10)
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def generateNginxConfig(clusterName,serviceName,userName):
    print("Generating Nginx Config")
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

def generateSplunkUniversalForwarderConfig(clusterName,serviceName,userName):
    print("Generating Splunk Config")
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk-universal-forwarder/04_configuration.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def deleteSplunkUniversalForwarderConfig(clusterName,serviceName,userName):
    print("Deleting Splunk Universal Forwarder Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa


def deleteNginxConfig(clusterName,serviceName,userName):
    print("Deleting Nginx Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{serviceName}-{userName}-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{serviceName}-{userName}-nginx-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{serviceName}-{userName}-modsecurity.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

# Install Nginx on Container/Pod
def setupWAF(clusterName, serviceName, userName):
    print("Setup WAF for:",serviceName,userName)
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        print("Setup WAF counter:",counter)
        for i in pod_list:
            if f'nginx-modsecurity-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
        
    generateNginxConfig(clusterName,serviceName,userName)
    print("POD_ID:",pod_id)
    print("Sleeping 10 seconds for splunk service to load...")
    time.sleep(10)
    try:
        print("Copying nginx file to Pod")
        subprocess.Popen([f"kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx-2.conf default/"+pod_id+":/etc/nginx/nginx.conf"],shell=True).wait()
        subprocess.Popen([f"kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-modsecurity.conf default/"+pod_id+":/etc/nginx/modsec/modsecurity.conf"],shell=True).wait()
        print("Confirming nginx.conf and modsecurity.conf file copied...")
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- cat /etc/nginx/nginx.conf | grep "+serviceName+""],shell=True).wait()
        print("Reloading Nginx service")
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- nginx -s reload"],shell=True).wait()
        print("Checking output of reloading Nginx:")
        nginxReloadCommand = ["kubectl","exec","-it",pod_id,"--", "nginx", "-s", "reload"]
        nginxReloadOut = check_output(nginxReloadCommand)
        print("Reload Output:",nginxReloadOut.decode("utf-8"))
        print("Deleting Nginx Conf File...")
        deleteNginxConfig(clusterName,"juice-shop",userName)
    except: 
        print("Error occured... retrying setupWAF...")
        setupWAF(clusterName, serviceName, userName)    
    # kubectl exec -it splunk-oppa-75fff68596-jbq46 -- /bin/sh
    # kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/nginx.conf default/nginx-modsecurity-oppa-6b7f54ff8-fszg6:/etc/nginx/nginx.conf

def getPodId(serviceName, userName):
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        print(f"Setup {serviceName} counter:",counter)
        for i in pod_list:
            if f'{serviceName}-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
    return pod_id

def getContainerId(podId):
    command = ["kubectl","describe","pod",podId]
    command_output = check_output(command).split()
    container_id = ''
    for i in command_output:
        # print(i)
        if 'docker://' in str(i):
            # print(i.decode("utf-8").replace('\'',''))
            container_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
    return container_id

def splunkSetupSplunkAddons(clusterName,serviceName,userName):
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        print("Setup Splunk counter:",counter)
        for i in pod_list:
            if f'splunk-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
        # time.sleep(1)
    
    # 2. get container_id
    ncommand = ["kubectl","describe","pod",pod_id]
    nout = check_output(ncommand).split()
    ncontainer_id = ''
    for i in nout:
        # print(i)
        if 'docker://' in str(i):
            # print(i.decode("utf-8").replace('\'',''))
            ncontainer_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/modsecurity-add-on-for-splunk.tgz "+ncontainer_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    # Unpack tgz addon
    subprocess.Popen([f"docker exec -u root "+ncontainer_id+" tar xvzf /opt/splunk/etc/apps/modsecurity-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    # Restart splunk service
    subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunk/bin/splunk restart"],shell=True).wait()

def setupSplunkLogging(clusterName,serviceName,userName):
    """
    0. enable splunk receving
    1. get splunk-universal-forwarder pod_id
    2. get container_id
    3. Run copy inputs over to container
    4. Add Splunk server to forward logs
    5. Restart splunk-universal-forwarder service

    kubectl describe pod splunk-universal-forwarder-oppa-747d54cb-wtlzg
    docker exec -u root 4c35ca0d76dccc84e93896d7c953da8bb119c08fbd4af50dc7842682198a41ef whoami
    """

    generateSplunkUniversalForwarderConfig(clusterName,serviceName,userName)
    print("Sleeping 30 Seconds for splunk to get ready")
    time.sleep(30)

    # 0. splunk enable listen 9997 -auth admin:Changeme

    # 1. get splunk-universal-forwarder pod_id
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        print("Setup Splunk counter:",counter)
        for i in pod_list:
            if f'splunk-universal-forwarder-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
        # time.sleep(1)
    
    # 2. get container_id
    ncommand = ["kubectl","describe","pod",pod_id]
    nout = check_output(ncommand).split()
    ncontainer_id = ''
    for i in nout:
        # print(i)
        if 'docker://' in str(i):
            # print(i.decode("utf-8").replace('\'',''))
            ncontainer_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs.conf "+ncontainer_id+":/opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_us-west1-a-splunk-universal-forwarder-oppa-inputs.conf 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc:/opt/splunkforwarder/etc/system/local/inputs.conf
    # Check file is copied
    subprocess.Popen([f"docker exec -u root "+ncontainer_id+" cat /opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker exec -u root 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc cat /opt/splunkforwarder/etc/system/local/inputs.conf
    
    try:
        # 4. point Universal forwarder to splunk server
        # This command should show a FATAL error, its supposed to happend in order for splunk to login
        subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk add forward-server splunk-"+userName+":9997"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/nginx-"+userName+".log"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/modsecurity-"+userName+".log"],shell=True).wait()

        # 5. Restart splunk-universal-forwarder service
        subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk restart"],shell=True).wait()
        
        # 6. Clean up inputs files on host
        deleteSplunkUniversalForwarderConfig(clusterName,"splunk-universal-forwarder",userName)
    except:
        print("Failed to setup Splunk Forwarder... retrying in 10 seconds")
        time.sleep(10)
        setupSplunkLogging(clusterName,serviceName,userName)

# Install Cloudcmd on Container/Pod
def setupCLOUDCMD(clusterName, serviceName, userName):
    print("setupCLOUDCMD!!!",clusterName,serviceName,userName)
    # time.sleep(5)
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        print(counter)
        for i in pod_list:
            if f'{serviceName}-{userName}' in str(i):
                print(str(i))
                pod_id = str(i)
                findPod=False
        counter+=1

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
        # 3. Generate Yaml Service Files
        time.sleep(10)
        generateKubernetesServicesYaml(clusterName, 'nginx-modsecurity',userName)
        generateKubernetesServicesYaml(clusterName, 'juice-shop',userName)
        generateKubernetesServicesYaml(clusterName, 'splunk',userName)
        generateKubernetesServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        # 4. Deploy Service pods
        manageKubernetesServicesPod(clusterName,'nginx-modsecurity', userName, action)
        manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        manageKubernetesServicesPod(clusterName,'splunk', userName, action)
        manageKubernetesServicesPod(clusterName,'splunk-universal-forwarder',userName, action)

        # print("WAF setup")
        setupWAF(clusterName, 'juice-shop', userName)
        # setupCLOUDCMD(clusterName, 'nginx-modsecurity', userName)
        # setupCLOUDCMD(clusterName, 'juice-shop', userName)

        print("Splunk Universal Forwarder Setup")
        setupSplunkLogging(clusterName, 'splunk-universal-forwarder', userName)

    elif action == 'delete':
        # 1. Delete Ingress Pods
        manageKubernetesIngressPod(clusterName,'traefik', action)
        # 2. Generate Yaml Ingress Files
        deleteKubernetesIngressYaml(clusterName,'traefik')
        # 3. Delete Service Pods
        manageKubernetesServicesPod(clusterName, 'nginx-modsecurity',userName, action)
        manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        manageKubernetesServicesPod(clusterName, 'splunk', userName, action)
        manageKubernetesServicesPod(clusterName, 'splunk-universal-forwarder', userName, action)
        # 4. Delete Yaml Files
        deleteKubernetesServicesYaml(clusterName,'nginx-modsecurity',userName)
        deleteKubernetesServicesYaml(clusterName,'juice-shop',userName)
        deleteKubernetesServicesYaml(clusterName,'splunk',userName)
        deleteKubernetesServicesYaml(clusterName,'splunk-universal-forwarder',userName)
        # 5. Delete Persist Volumes
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True)
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True)

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
    PAYLOAD:    { action: deploy | delete }
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
            # setupWAF(args['clusterName'],'juice-shop',args['userName'])
            # setupSplunkLogging(args['clusterName'],'splunk-universal-forwarder',args['userName'])
            splunkSetupSplunkAddons(args['clusterName'],'splunk',args['userName'])
            return args, 201
        except:
            return args, 404


# API Paths
api.add_resource(Kubernetes, '/api/kubernetes/challenges/<challenge_id>')

if __name__ == '__main__':
    app.run(debug=True)
