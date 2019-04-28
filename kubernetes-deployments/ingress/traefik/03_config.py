import sys


def writeConfig(**kwargs):
    templateo = """
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: default
data:
  traefik.toml: |
    defaultEntryPoints = ["http"]
    [entryPoints]
      [entryPoints.http]
      address = ":80"
    [kubernetes]
    """
    template = """
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: default
data:
  traefik.toml: |
    defaultEntryPoints = ["http", "https"]
    [entryPoints]
      [entryPoints.http]
      address = ":80"
      #   [entryPoints.http.redirect]
      #     entryPoint = "https"
      # [entryPoints.https]
      # address = ":443"
      #   [entryPoints.https.tls]
    [kubernetes]
              """

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/03_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-config.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))