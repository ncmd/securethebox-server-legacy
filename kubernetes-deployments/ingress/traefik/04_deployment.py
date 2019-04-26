import sys


def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: traefik-{clusterName}-ingress-controller
    spec:
      replicas: 1
      template:
        metadata:
          labels:
            app: traefik-{clusterName}-ingress-controller
        spec:
          serviceAccountName: traefik-ingress-controller
          terminationGracePeriodSeconds: 60
          volumes:
            - name: config
              configMap:
                name: traefik-config
          containers:
          - name: traefik
            image: "traefik:1.7.10-alpine"
            volumeMounts:
              - mountPath: "/etc/traefik/config"
                name: config
            args:
            - --configfile=/etc/traefik/config/traefik.toml
            - --api
            - --kubernetes
            - --logLevel=DEBUG
              """

    with open('04-traefik-{clusterName}-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]))