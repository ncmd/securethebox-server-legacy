def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: {serviceName}
      annotations:
        kubernetes.io/ingress.class: traefik
        traefik.frontend.passHostHeader: "false"
        traefik.frontend.priority: "1"
    spec:
      rules:
      - host: {serviceName}.{clusterName}.securethebox.us
        http:
          paths:
          - path: /
            backend:
              serviceName: {serviceName}
              servicePort: {servicePort}
              """

    with open('ingress.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
writeConfig(serviceName="serviceName",servicePort=80,clusterName="clusterName")