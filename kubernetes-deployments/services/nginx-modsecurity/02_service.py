import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: v1
    kind: Service
    metadata:
      name: {serviceName}-{userName}
    spec:
      selector:
        app: {serviceName}-{userName}
      ports:
      - name: http
        targetPort: 80
        port: 80
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/02_'+str(sys.argv[3])+'-'+str(sys.argv[2])+'-'+str(sys.argv[1])+'-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),serviceName=str(sys.argv[2]),clusterName=str(sys.argv[3]))