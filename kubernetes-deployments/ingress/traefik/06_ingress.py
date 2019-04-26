import sys


def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: traefik-{clusterName}-ingress-controller
      namespace: default
      annotations:
        kubernetes.io/ingress.class: traefik
        external-dns.alpha.kubernetes.io/target: traefik.{clusterName}.securethebox.us
    spec:
      tls:
      - hosts:
        - traefik.{clusterName}.securethebox.us
        secretName: traefik-ui-tls-cert
      rules:
        - host: traefik.{clusterName}.securethebox.us
          http:
            paths:
            - path: /
              backend:
                serviceName: traefik-{clusterName}-ingress-controller
                servicePort: admin
              """

    with open('06-traefik-{clusterName}-ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]))