import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: v1
    kind: Service
    metadata:
      name: nginx-modsecurity-{userName}
    spec:
      selector:
        app: nginx-modsecurity-{userName}
      ports:
      - name: http
        targetPort: 80
        port: 80
              """

    with open('nginx-modsecurity-{userName}-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))