import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: v1
    kind: Service
    metadata:
      name: splunk-{userName}
    spec:
      selector:
        app: splunk-{userName}
      ports:
      - name: http
        targetPort: 8000
        port: 8000
      - name: management
        targetPort: 8088
        port: 8088
              """

    with open('splunk-{userName}-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))