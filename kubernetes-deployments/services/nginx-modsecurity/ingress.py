import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: nginx-modsecurity-{userName}
      annotations:
        kubernetes.io/ingress.class: traefik
        traefik.frontend.passHostHeader: "false"
        traefik.frontend.priority: "1"
    spec:
      rules:
      - host: nginx-modsecurity-{userName}.{clusterName}.securethebox.us
        http:
          paths:
          - path: /
            backend:
              serviceName: nginx-modsecurity-{userName}
              servicePort: 80
              """

    with open('nginx-modsecurity-{userName}-ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),clusterName=str(sys.argv[2]))