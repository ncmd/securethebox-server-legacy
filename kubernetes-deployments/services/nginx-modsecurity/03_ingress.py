import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: {serviceName}-{userName}
      annotations:
        kubernetes.io/ingress.class: traefik
        traefik.frontend.passHostHeader: "false"
        traefik.frontend.priority: "1"
    spec:
      rules:
      - host: {serviceName}-{userName}.{clusterName}.securethebox.us
        http:
          paths:
          - path: /
            backend:
              serviceName: {serviceName}-{userName}
              servicePort: 80
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/03_'+str(sys.argv[3])+'-'+str(sys.argv[2])+'-'+str(sys.argv[1])+'-ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),serviceName=str(sys.argv[2]),clusterName=str(sys.argv[3]))