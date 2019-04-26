import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: v1
    kind: Service
    metadata:
      name: juice-shop-{userName}
    spec:
      selector:
        app: juice-shop-{userName}
      ports:
      - name: http
        targetPort: 3000
        port: 3000
              """

    with open('juice-shop-{userName}-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))