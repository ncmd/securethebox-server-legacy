# thisstring = "    Container ID:   docker://2d827548bfb24abe67a588c1ff4d343f8a6732f67de7f88f9b86c32038ab9e79"

# print(thisstring.split("docker://",1)[1])
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
import time

# kubectl describe pod splunk-universal-forwarder-oppa-747d54cb-mkkc4

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
        if f'splunk-universal-forwarder-oppa' in str(i):
            print("FOUND POD_ID:",str(i))
            pod_id = str(i)
            findPod=False
    counter+=1

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
# Check file is copied
subprocess.Popen([f"docker exec -u root "+ncontainer_id+" cat /opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()

# 4. point Universal forwarder to splunk server
# This command should show a FATAL error, its supposed to happend in order for splunk to login
subprocess.Popen([f"docker exec -u root "+ncontainer_id+"  /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'"],shell=True).wait()
subprocess.Popen([f"docker exec -u root "+ncontainer_id+"  /opt/splunkforwarder/bin/splunk add forward-server splunk-oppa:9777"],shell=True).wait()

# 5. Restart splunk-universal-forwarder service
subprocess.Popen([f"docker exec -u root "+ncontainer_id+" /opt/splunkforwarder/bin/splunk restart"],shell=True).wait()