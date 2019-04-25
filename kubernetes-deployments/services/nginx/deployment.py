def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: {serviceName}
      labels:
        app: {serviceName}
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: {serviceName}
      template:
        metadata:
          labels:
            app: {serviceName}
        spec:
          containers:
          - name: {serviceName}
            image: "{imageName}"
              """

    with open('deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
writeConfig(serviceName="serviceName",imageName="imageName")