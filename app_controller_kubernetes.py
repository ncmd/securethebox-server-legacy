import subprocess


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

def createPersistentVolumes(action):
    print('Creating Persistent Volume and Claim')
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    # kubectl apply -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml
    # kubectl apply -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml

def manageKubernetesPods(clusterName, serviceName, userName, action):
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/pods/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()

def manageKubernetesServicesPod(clusterName, serviceName, userName, action):
    print(action,"Service Pod:",serviceName)
    if action == 'apply':
        print('Creating Persistent Volume and Claim')
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()