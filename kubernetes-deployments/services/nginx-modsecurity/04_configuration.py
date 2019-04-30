import sys
from shutil import copyfile
import subprocess

def writeConfig(clusterName,serviceName,userName):
    # Copy Template file
    copyfile('./kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf', './kubernetes-deployments/services/nginx-modsecurity/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-nginx.conf')
    # Replace Line in file
    subprocess.Popen([f"sed '38s/nginx-userName/nginx-{userName}/' './kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx.conf"],shell=True).wait()
    # sed '38s/nginx-userName/nginx-oppa/' './kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf'  > ./kubernetes-deployments/services/nginx-modsecurity/04_us-west1-a-nginx-modsecurity-oppa-nginx.conf
    subprocess.Popen([f"sed '66s/serviceName-userName/{serviceName}-{userName}/' './kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx-2.conf"],shell=True).wait()
    # sed '66s/serviceName-userName/nginx-oppa/' './kubernetes-deployments/services/nginx-modsecurity/04_us-west1-a-juice-shop-oppa-nginx.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_us-west1-a-juice-shop-oppa-nginx-new.conf
    subprocess.Popen([f"sed '231s/userName/{userName}/' './kubernetes-deployments/services/nginx-modsecurity/template-modsecurity.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-modsecurity.conf"],shell=True).wait()

# usage:    
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))