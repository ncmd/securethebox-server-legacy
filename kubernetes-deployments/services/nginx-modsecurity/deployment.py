import sys


def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: nginx-modsecurity-{userName}
      labels:
        app: nginx-modsecurity-{userName}
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: nginx-modsecurity-{userName}
      template:
        metadata:
          labels:
            app: nginx-modsecurity-{userName}
        spec:
          containers:
          - name: nginx-modsecurity-{userName}
            image: "ncmd/nginx-modsecurity:latest"
              """

    with open('nginx-modsecurity-{userName}-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))