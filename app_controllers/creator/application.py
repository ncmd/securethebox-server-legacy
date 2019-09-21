import yaml


class Application():
    def __init__(self):
        self.applicationList = []

    def loadApplications(self, applicationList):
        self.applicationList = applicationList

    def addApplication(self,applicationName):
        self.applicationList.append(applicationName)
        
    def getApplicationList(self):
        return self.applicationList

def generateDeploymentYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/deployment.yaml','r+') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)

def generateIngressYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/ingress.yaml','w') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)

def generateServiceYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/service.yaml','w') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)
