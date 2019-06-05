from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
import time
import json
import requests
import os

'''
TODO:
- get status of pod
    - kubectl get pod --field-selector=status.phase=Succeeded

- Splunk port forwarding needs to work (it does, but needed portforwarding)
    - https://github.com/splunk/docker-splunk/tree/develop/test_scenarios/kubernetes
    - kubectl port-forward splunk-charles-c76dd785b-h866v 8000:8000

- Generating Answers
    - attacker_ip_address
    - perform sqli/xss

- Install Codebox to edit code
    - make it easier to edit code

-  Setup Each user has its own "namespace" in kubernetes
    - https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-organizing-with-namespaces

- Create Network Policies
    - https://kubernetes.io/docs/concepts/services-networking/network-policies/

- Automated checks to score user
    - Check if service is running

- Timer need to destroy environment after X time
    - After 2hrs

- Generate password for cloudcmd

1. pvc needs to be unique per user
2. pvc needs to be deleted 

1. add wireshark https://hub.docker.com/r/ffeldhaus/wireshark
2. need to fix time, timestamp for logs is wrong...

4. add attack server


kubectl delete po,svc,deployment --all
'''

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
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

def generateKubernetesPodsYaml(clusterName,serviceName,userName):
    print("Generating Pod Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/pods/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()

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

def manageKubernetesPods(clusterName, serviceName, userName, action):
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/pods/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()

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
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-3.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa


def deleteNginxConfig(clusterName,serviceName,userName):
    print("Deleting Nginx Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-modsecurity.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

# Install Nginx on Container/Pod
def setupWAF(clusterName, serviceName, userName):
    print("Checking if Service up with GET request")
    response = requests.request("GET", 'http://nginx-modsecurity-charles.us-west1-a.securethebox.us')
    print(response.text)

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
        if counter > 10:
            findPod=False
        print("Setup WAF counter:",counter)
        for i in pod_list:
            if f'nginx-modsecurity-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
        
    generateNginxConfig(clusterName,serviceName,userName)
    print("POD_ID:",pod_id)
    print("setupWAF - Sleeping 10 seconds for nginx service to load...")
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
        try:
            nginxReloadOut = check_output(nginxReloadCommand)
            print("Reload Output:",nginxReloadOut.decode("utf-8"))
            print("Deleting Nginx Conf File...")
            deleteNginxConfig(clusterName,"juice-shop",userName)
            print("COMPLETE!!!!")
        except:
            print("Error occured... on nginxReloadOut...")
            setupWAF(clusterName, serviceName, userName)    
        
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
        if counter > 10:
            findPod=False
        print(f"Setup {serviceName} counter:",counter)
        for i in pod_list:
            if f'{serviceName}-{userName}' in str(i):
                pod_id = str(i)
                findPod=False
                print("FOUND POD_ID:",pod_id)
        counter+=1
    return pod_id

def getPodStatus(podId):
    command = ["kubectl","get","pod",podId,"-o","json"]
    command_output = check_output(command)
    parsedJSON = json.loads(command_output)
    currentState = parsedJSON["status"]["containerStatuses"][0]["state"]
    # print(parsedJSON["status"]["containerStatuses"][0]["state"])
    for i in currentState:
        print("Key:",i)
        if i == "running":
            return True
        elif i != "running":
            return False

def getContainerId(podId):
    command = ["kubectl","describe","pod",podId]
    command_output = check_output(command).split()
    container_id = ''
    for i in command_output:
        # print(i)
        if 'docker://' in str(i):
            container_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
            print("FOUND CONTAINER_ID:",container_id)
    return container_id

def runSplunkScript():
    """

    """

def setupSplunkUserPreferences(container_id):
    # doc
    # /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf
    # tz = America/Los_Angeles
    # docker exec -it 0f0b570de296 /bin/sh
    # need to login as admin first
    print("Setting up Splunk User Preferences",container_id[:12])
    try:
        # subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk/check_login.py"],shell=True).wait()
        # mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/
        subprocess.Popen([f"docker exec -u root "+container_id+" mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/"],shell=True).wait()
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf "+container_id[:12]+":/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" cat /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunk/bin/splunk restart"],shell=True).wait()
    except:
        print("Trying again...")
        setupSplunkUserPreferences(container_id)

    # docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf 24d56f0c7156:/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf



def setupSplunkPortForwarding(userName):
    pod_id = getPodId("splunk",userName)
    subprocess.Popen([f"kubectl port-forward "+pod_id+" 8000:8000"],shell=True).wait()
    # kubectl port-forward splunk-charles-c76dd785b-f6z5l 8000:8000
    # os.spawnl(os.P_DETACH, "kubectl port-forward "+pod_id+" 8000:8000")
    # subprocess.Popen([f"kubectl port-forward "+pod_id+" 8089:8089"],shell=True).wait()

def splunkSetupSplunkAddons(clusterName,serviceName,userName):
    print("Setting up splunk addons")
    pod_id = getPodId("splunk",userName)
    
    # 2. get container_id
    container_id = getContainerId(pod_id)
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/modsecurity-add-on-for-splunk.tgz "+container_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/suricata-add-on-for-splunk.tgz "+container_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    # Unpack tgz addon
    subprocess.Popen([f"docker exec -u root "+container_id+" tar xvzf /opt/splunk/etc/apps/modsecurity-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    subprocess.Popen([f"docker exec -u root "+container_id+" tar xvzf /opt/splunk/etc/apps/suricata-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    # Restart splunk service
    subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunk/bin/splunk restart"],shell=True).wait()

# # Setup Addons
#     splunkSetupSplunkAddons(clusterName,serviceName,userName)
#     # Setup User Preferences
#     setupSplunkUserPreferences(container_id)

def setupSplunkMaster(clusterName, userName):
    print("Setting up Splunk Master Setup")
    # 1. get splunk-universal-forwarder pod_id
    pod_id = getPodId("splunk",userName)
    
    # 2. get container_id
    container_id = getContainerId(pod_id)

    splunkSetupSplunkAddons(clusterName,"splunk",userName)

    setupSplunkUserPreferences(container_id)

    setupSplunkPortForwarding(userName)

   
    

def setupSplunkForwarderLogging(clusterName,serviceName,userName):
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

    # 1. get splunk-universal-forwarder pod_id
    pod_id = getPodId("splunk-universal-forwarder",userName)
    
    # 2. get container_id
    container_id = getContainerId(pod_id)
    
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-2.conf "+container_id+":/opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_us-west1-a-splunk-universal-forwarder-oppa-inputs.conf 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc:/opt/splunkforwarder/etc/system/local/inputs.conf
    # Check file is copied
    subprocess.Popen([f"docker exec -u root "+container_id+" cat /opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker exec -u root 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc cat /opt/splunkforwarder/etc/system/local/inputs.conf
    
    try:
        # 4. point Universal forwarder to splunk server
        # This command should show a FATAL error, its supposed to happend in order for splunk to login
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add forward-server splunk-"+userName+":9997"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/nginx-"+userName+".log"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/modsecurity-"+userName+".log"],shell=True).wait()

        # 5. Restart splunk-universal-forwarder service
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk restart"],shell=True).wait()
        
        # 6. Clean up inputs files on host
        deleteSplunkUniversalForwarderConfig(clusterName,"splunk-universal-forwarder",userName)
    except:
        print("Failed to setup Splunk Forwarder... retrying in 10 seconds")
        time.sleep(10)
        setupSplunkForwarderLogging(clusterName,serviceName,userName)

# Install Cloudcmd on Container/Pod
def setupCLOUDCMD(clusterName, serviceName, userName):
    print("setupCLOUDCMD!!!",clusterName,serviceName,userName)

    pod_id = getPodId(serviceName,userName)
    container_id = getContainerId(pod_id)

    if serviceName == 'nginx-modsecurity':
        subprocess.Popen([f"docker exec -u root "+container_id+" apk add nodejs nodejs-npm"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" forever start /usr/bin/cloudcmd --port 9000"],shell=True).wait()
    
    elif serviceName == 'juice-shop':
        subprocess.Popen([f"docker exec -u root "+container_id+" npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" forever start /usr/local/bin/cloudcmd --port 9000"],shell=True).wait()

def setupAttacker():
    subprocess.Popen([f"kubectl apply -f ./kubernetes-deployments/pods/kali-linux/01_pod.yml"],shell=True).wait()
    # subprocess.Popen([f"kubectl delete -f ./kubernetes-deployments/pods/kali-linux/01_pod.yml"],shell=True).wait()
    # generateKubernetesServicesYaml("us-west1-a", 'kali-linux','charles')
    # manageKubernetesServicesPod("us-west1-a",'kali-linux', 'charles', 'apply')
    # manageKubernetesServicesPod("us-west1-a",'kali-linux', 'charles', 'delete')
    # deleteKubernetesServicesYaml("us-west1-a",'kali-linux','charles')

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
        generateKubernetesPodsYaml(clusterName, 'kali-linux',userName)
        # 4. Deploy Service pods
        manageKubernetesServicesPod(clusterName,'nginx-modsecurity', userName, action)
        manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        manageKubernetesServicesPod(clusterName,'splunk', userName, action)
        manageKubernetesServicesPod(clusterName,'splunk-universal-forwarder',userName, action)
        manageKubernetesPods(clusterName,'kali-linux',userName, action)
        # manageKubernetesServicesPod(clusterName,'wireshark',userName, action)

        print("WAF setup")
        setupWAF(clusterName, 'juice-shop', userName)
        
        print("Splunk Universal Forwarder Setup")
        setupSplunkForwarderLogging(clusterName, 'splunk-universal-forwarder', userName)

        # Setup Cloudcmd
        print("Cloudcmd Setup")
        setupCLOUDCMD(clusterName, 'nginx-modsecurity', userName)
        # setupCLOUDCMD(clusterName, 'juice-shop', userName)

        # Setup Port Forwarding
        setupSplunkMaster(clusterName,userName)
        

    elif action == 'delete':
        # 1. Delete Ingress Pods
        manageKubernetesIngressPod(clusterName,'traefik', action)
        # 2. Generate Yaml Ingress Files
        deleteKubernetesIngressYaml(clusterName,'traefik')
        # 3. Delete Service Pods
        manageKubernetesServicesPod(clusterName, 'nginx-modsecurity',userName, action)
        manageKubernetesServicesPod(clusterName, 'juice-shop', userName, action)
        manageKubernetesServicesPod(clusterName, 'splunk', userName, action)
        manageKubernetesServicesPod(clusterName, 'splunk-universal-forwarder', userName, action)
        # 4. Delete Yaml Files
        deleteKubernetesServicesYaml(clusterName, 'nginx-modsecurity',userName)
        deleteKubernetesServicesYaml(clusterName, 'juice-shop',userName)
        deleteKubernetesServicesYaml(clusterName, 'splunk',userName)
        deleteKubernetesServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        # 5. Delete Persist Volumes
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True)
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True)
        # 6. Clean up the rest of environment (note this will close everything... do not do this in production)
        subprocess.Popen([f"kubectl delete po,svc,pv,pvc,deployment --all"],shell=True)

# Kubernetes API
class Kubernetes(Resource):
    '''
    REQUEST:    POST
    URI:        https://securethebox.us/api/kubernetes/challenges/1
    PAYLOAD:    { action: deploy | delete }
    '''
    def post(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            manageChallenge1(args['clusterName'],args['userName'],args['action'])
            return args, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return args, 404
    
    def get(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            # setupWAF(args['clusterName'],'juice-shop',args['userName'])
            # setupSplunkForwarderLogging(args['clusterName'],'splunk-universal-forwarder',args['userName'])
            # splunkSetupSplunkAddons(args['clusterName'],'splunk',args['userName'])
            # setupCLOUDCMD(args['clusterName'], 'nginx-modsecurity', args['userName'])
            # setupCLOUDCMD(args['clusterName'], 'juice-shop', args['userName'])
            # podId = getPodId(args['serviceName'],args['userName'])
            # podStatus = getPodStatus(podId)
            # setupSplunkPortForwarding(args['userName'])
            setupAttacker()

            return podStatus, 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"}
        except:
            return args, 404



# Check answer according to challengeNumber & questionNumber
def checkAnswer(challengeNumber, questionNumber):
    print("The answer is ....")

# Create a record for question for challengeNumber
def createQuestion(challengeNumber, questionNumber, answer):
    print('Created question and answer')
    """
    solutions/solution_id
    - challenge_1: { question1:'',answer1:''}
    """

# Takes in the submission for Challenge1
# def submissionChallenge1(challengeNumber, userName, solutionData):
def submissionChallenge1(solutions):
    print("SOLUTION:",solutions)
    for i in solutions:
        print(i,solutions[i])

# Kubernetes API
class Solutions(Resource):
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
    
kubernetes_parser = reqparse.RequestParser()
kubernetes_parser.add_argument('action', choices=('apply','delete'), help='{error_msg}')
kubernetes_parser.add_argument('userName', help='{error_msg}')
kubernetes_parser.add_argument('clusterName', choices=('us-west1-a'), help='{error_msg}')
kubernetes_parser.add_argument('serviceName', help='{error_msg}')

solutions_parser = reqparse.RequestParser()
solutions_parser.add_argument('solutionData', help='{error_msg}')

# API Paths
api.add_resource(Kubernetes, '/api/kubernetes/challenges/<challenge_id>')
api.add_resource(Solutions, '/api/solutions/challenges/<challenge_id>')

if __name__ == '__main__':
    app.run(debug=True)
