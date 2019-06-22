import subprocess
from subprocess import check_output

"""
Start this script

"""
def deployVault():
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-vault/_01_config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-vault/_02_service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-vault/_03_deployment.yml"],shell=True).wait()

# kubectl delete -f ./kubernetes-deployments/services/hashicorp-vault/_03_deployment.yml
if __name__ == "__main__":
    deployVault()