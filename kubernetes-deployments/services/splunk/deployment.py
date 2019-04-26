import sys

def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: splunk-{userName}
      labels:
        app: splunk-{userName}
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: splunk-{userName}
      template:
        metadata:
          labels:
            app: splunk-{userName}
        spec:
          containers:
          - name: splunk-{userName}
            image: splunk/splunk:latest
            env:
              - name: SPLUNK_START_ARGS
                value: --accept-license
              - name: SPLUNK_USER
                value: root
              - name: SPLUNK_PASSWORD
                value: changeme
              """

    with open('splunk-{userName}-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))