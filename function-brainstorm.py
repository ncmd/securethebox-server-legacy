
'''

Simulation on defending against common web application attacks

Track user actions to score them with checklist to track performance

'''



def deploy_challenge(action,username, challenge_id):
	'''
	create yml file based on arguments
	
	deploy challenge servers
	
	get urls for servers
	username-service_name.us-west1-a.securethebox.us

	traefik should direct traffic to appropriate servers
	ie. waf should be linked to app

	kubernetes storage should have all the logs in one place
	splunk should be able to load this storage for parsing/indexing
	'''
	print('a')

	
def track_challenge_progress(uesrname,challenge_id):
	'''
	user knows how to use linux bash
	user know how to create a functioning script
	user knows how to work with json/csv/syslog data
	user able to implement authentication
	user knows how to make prepared statements for sql queries
	user able to identify network interfaces
	user able to identify running processes
	user knows how to kill running processes
	user identified vulnerable function
	user kno
	'''

	print('a')

def generateServiceYaml(serviceName, userName, clusterName):
    if serviceName == "nginx-modsecurity":
        funcListDeploy = [
        print(["python", f"/app/kubernetes-deployments/services/{serviceName}/01_deployment.py", "-f" , userName]),
        print(["python", f"/app/kubernetes-deployments/services/{serviceName}/02_service.py", "-f" , userName]),
        print(["python", f"/app/kubernetes-deployments/services/{serviceName}/03_ingress.py", "-f" , userName, clusterName])
        ]
        print(funcListDeploy)
        # executeCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", "apply", "-f" ,"/app/kubernetes-deployments/service/{serviceName}/{serviceName}-{userName}-deployment.yml"]),
        # executeCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", "apply", "-f" ,"/app/kubernetes-deployments/service/{serviceName}/{serviceName}-{userName}-service.yml"]),
        # executeCommandWithStdout(["/app/vendor/google-cloud-sdk/bin/kubectl", "apply", "-f" ,"/app/kubernetes-deployments/service/{serviceName}/{serviceName}-{userName}-ingress.yml"]),
    elif serviceName == "juice-shop":
        print("juice-shop")
    elif serviceName == "splunk":
        print("splunk")

if __name__ == "__main__":
	generateServiceYaml("nginx-modsecurity", "oppa", "us-west1-a")