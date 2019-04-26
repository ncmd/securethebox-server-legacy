import sys


def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: {serviceName}-{userName}
      labels:
        app: {serviceName}-{userName}
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: {serviceName}-{userName}
      template:
        metadata:
          labels:
            app: {serviceName}-{userName}
        spec:
          containers:
          - name: {serviceName}-{userName}
            image: "ncmd/juice-shop:latest"
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[3])+'-'+str(sys.argv[2])+'-'+str(sys.argv[1])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),serviceName=str(sys.argv[2]),clusterName=str(sys.argv[3]))