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
        port: 8000
      - name: management
        targetPort: 8088
        port: 8088
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/02_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))