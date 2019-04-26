import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: splunk-{userName}
      annotations:
        kubernetes.io/ingress.class: traefik
        traefik.frontend.passHostHeader: "false"
        traefik.frontend.priority: "1"
    spec:
      rules:
      - host: splunk-{userName}.{clusterName}.securethebox.us
        http:
          paths:
          - path: /
            backend:
              userName: splunk-{userName}
              servicePort: 8000
              """

    with open('splunk-{userName}-ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),clusterName=str(sys.argv[2]))