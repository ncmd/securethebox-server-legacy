def writeConfig(**kwargs):
    template = """
    apiVersion: v1
    kind: Service
    metadata:
      name: {serviceName}
    spec:
      selector:
        app: {serviceName}
      ports:
      - name: {portName}
        targetPort: {portTargetPort}
        port: {portPort}
              """

    with open('service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
writeConfig(serviceName="serviceName",portName="http",portTargetPort=80,portPort=80)