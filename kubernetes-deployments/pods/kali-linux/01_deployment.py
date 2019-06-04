import sys

def writeConfig(**kwargs):
    template = """
kind: Pod
apiVersion: v1
metadata:
  name: {serviceName}-{userName}
spec:
  containers:
    - name: {serviceName}-{userName}
      image: kalilinux/kali-linux-docker
      command: ["/bin/sh", "-c"]
      args:
      - echo starting;
        apt-get update && apt-get install metasploit-framework python3-pip -y;
        pip3 install --user pymetasploit3;
        msfrpcd -P securethebox -S;
        service postgresql start;
        msfdb init;
        echo done;
        while true ; do continue ; done ;
  restartPolicy: Never
              """

    with open('./kubernetes-deployments/pods/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))