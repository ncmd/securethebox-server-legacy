import sys
from shutil import copyfile
import subprocess

def writeConfig(clusterName,serviceName,userName):
    # Copy Template file
    copyfile('./kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf', './kubernetes-deployments/services/nginx-modsecurity/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-nginx.conf')
    # Replace Line in file
    subprocess.Popen([f"sed '38s/nginx-userName/nginx-{userName}/' './kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"sed '66s/serviceName-userName/{serviceName}-{userName}/' './kubernetes-deployments/services/nginx-modsecurity/template-nginx.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"sed '231s/userName/{userName}/' './kubernetes-deployments/services/nginx-modsecurity/template-modsecurity.conf' > ./kubernetes-deployments/services/nginx-modsecurity/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-modsecurity.conf"],shell=True).wait()

# usage:    
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))