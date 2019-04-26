import sys


def writeConfig(**kwargs):
    template = """
    kind: Deployment
    apiVersion: extensions/v1beta1
    metadata:
      name: juice-shop-{userName}
      labels:
        app: juice-shop-{userName}
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: juice-shop-{userName}
      template:
        metadata:
          labels:
            app: juice-shop-{userName}
        spec:
          containers:
          - name: juice-shop-{userName}
            image: "ncmd/juice-shop:latest"
              """

    with open('juice-shop-{userName}-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(userName=str(sys.argv[1]))