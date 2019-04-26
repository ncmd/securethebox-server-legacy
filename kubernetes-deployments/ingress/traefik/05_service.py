import sys


def writeConfig(**kwargs):
    template = """
    kind: Service
    apiVersion: v1
    metadata:
      name: traefik-{clusterName}-ingress-controller
      annotations:
        external-dns.alpha.kubernetes.io/hostname: traefik.{clusterName}.securethebox.us
    spec:
      selector:
        app: traefik-{clusterName}-ingress-controller
      ports:
        - port: 80
          name: http
          targetPort: 8080
        - port: 443
          name: https
          targetPort: 8080
        - port: 8080
          name: admin
      type: LoadBalancer
              """

    with open('05-traefik-{clusterName}-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]))