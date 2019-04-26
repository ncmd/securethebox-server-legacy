import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: juice-shop-{userName}
      annotations:
        kubernetes.io/ingress.class: traefik
        traefik.frontend.passHostHeader: "false"
        traefik.frontend.priority: "1"
    spec:
      rules:
      - host: juice-shop-{userName}.{clusterName}.securethebox.us
        http:
          paths:
          - path: /
            backend:
              serviceName: juice-shop-{userName}
              servicePort: 3000
              """

    with open('juice-shop-{userName}-ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]),clusterName=str(sys.argv[2]))