import sys


def writeConfig(**kwargs):
    templateo = """
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: traefik-ingress-controller
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: traefik-ingress-controller
    spec:
      serviceAccountName: traefik-ingress-controller
      terminationGracePeriodSeconds: 60
      volumes:
        - name: config
          configMap:
            name: traefik-config
      containers:
      - name: traefik
        image: "traefik:1.6"
        volumeMounts:
          - mountPath: "/etc/traefik/config"
            name: config
        args:
        - --configfile=/etc/traefik/config/traefik.toml
        - --api
        - --kubernetes
        - --logLevel=DEBUG
    """
    template = """
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: {serviceName}-{clusterName}-ingress-controller
    spec:
      serviceAccountName: {serviceName}-{clusterName}-ingress-controller
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

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]))