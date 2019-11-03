"""
This file should take care of downloading/installing/uninstalling repos

Relies on PyHelm https://github.com/flaper87/pyhelm

Clones repos in securethebox organization
https://github.com/securethebox

securethebox org repos should contain all the helm charts 

required a tiller service to connect to which should be listening on port 44134

"""
from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller
import yaml 
import subprocess
import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pprint

class HelmChart:
    def __init__(self):
        self.chart_name = ""
        self.source_type = ""
        self.source_location = ""
        self.tiller_host = ""
        self.kubernetes_namespace = ""
        self.release_name = ""
        self.releaseNamespaceDict = {}
        self.chartReleaseNameDict = {}
        self.chart = ""
        self.values_yaml = ""

    # internal chart name
    def setName(self, name):
        self.chart_name = name

    # git, dir
    def setType(self,type):
        self.source_type = type
    
    # Github URL
    def setLocation(self, location):
        self.source_location = location

    # tiller host
    def setHost(self, host):
        self.tiller_host = host  

    # kubernetes namespace
    def setNamespace(self, namespace):
        self.kubernetes_namespace = namespace

    # load helm chart
    def loadChart(self):
        chart = ChartBuilder(
            {"name": self.chart_name, 
             "source": {
                 "type": self.source_type, 
                 "location": self.source_location
                 }
            })
        self.setChart(chart.get_helm_chart())
        
    def setChart(self, chart):
        self.chart = chart
        
    def getChartValuesYaml(self):
        # length_lines = len(str(self.chart).split('\n'))
        chart_lines = str(self.chart).splitlines()
        for index, value in enumerate(chart_lines):
            if "values {" in value:
                # REMEMBER TO REPLACE \n WITH \\n when we convert it back to RAW
                raw_yaml = chart_lines[index+1].split("raw: ",1)[1][1:][:-1].replace('\\n','\n')
                load_yaml = str(raw_yaml)
                return load_yaml

    # update the values section within chart
    def setChartValuesYaml(self,new_values):
        # Find line need to replace
        chart_lines = str(self.chart).splitlines()
        for index, value in enumerate(chart_lines):
            if "values {" in value:
                # REMEMBER TO REPLACE \n WITH \\n when we convert it back to RAW
                prev_values = chart_lines[index+1]
                chart_lines[index+1] = chart_lines[index+1].replace(prev_values, new_values.replace('\n','\\n'))
        self.chart = '\n'.join(chart_lines)
        print(self.chart)

    # Save chart to Firebase/Firestore

    # install helm chart
    def installChart(self):
        tiller = Tiller(self.tiller_host)
        tiller.install_release(
            self.chart, 
            dry_run=False, 
            namespace=self.kubernetes_namespace)

    # matches all deployed helm charts to repective namespace
    def loadReleasesForNamespaceDict(self):
        tiller = Tiller(self.tiller_host)
        releaseData = tiller.list_releases(namespace=self.kubernetes_namespace)
        for x in releaseData:
            length_lines = len(str(x).split('\n'))
            find_namespace = re.findall('"([^"]*)"',str(str(x).splitlines()[length_lines-2]).partition('\n')[0])
            namespace = find_namespace[0]
            find_name = re.findall('"([^"]*)"',str(x).partition('\n')[0])
            release_name = find_name[0]
            self.releaseNamespaceDict[release_name] = namespace

    # match releases to chart
    def listCharts(self):
        tiller = Tiller(self.tiller_host)
        chartData = tiller.list_charts()
        for x in chartData:
            find_release_name = re.findall("'(.*?)'",str(str(x).splitlines()[0]).partition('\n')[0])
            release_name = find_release_name[0]
            find_chart_name = re.findall('"([^"]*)"',str(str(x).splitlines()[1]).partition('\n')[0])
            chart_name = find_chart_name[0]
            self.chartReleaseNameDict[release_name] = chart_name

    def deleteAllReleasesForNamespace(self, namespace):
        for key in self.releaseNamespaceDict:
            if self.releaseNamespaceDict[key] == namespace:
                self.uninstallRelease(key)

    def uninstallRelease(self, release_name):
        tiller = Tiller(self.tiller_host)
        tiller.uninstall_release(release=release_name, disable_hooks=False, purge=True)

    def deleteChart(self):
        subprocess.Popen([f"helm delete {self.release_name} --purge --host=\"{self.tiller_host}:44134\""],shell=True).wait()
    
    def getChart(self):
        return self.chart

if __name__ == "__main__":
    hc = HelmChart()
    hc.setName("defectdojo")
    hc.setType("git")
    hc.setHost("localhost")
    # Ideally each user should have their own namespace
    hc.setNamespace("default")
    hc.setLocation("https://github.com/securethebox/defectdojo.git")
    hc.loadChart()
    hc.getChartValuesYaml()
    hc.setChartValuesYaml("  raw: \"🔥🔥🔥🔥🔥🔥🔥🔥🔥\"")
    # hc.listCharts()
    # hc.loadReleasesForNamespaceDict()
    # hc.deleteAllReleasesForNamespace("default")
