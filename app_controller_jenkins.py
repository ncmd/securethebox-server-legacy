import subprocess
import os
import requests
from lxml import html
import json
from subprocess import check_output
import urllib
import time
from app_controller_docker import dockerGetContainerId
from app_controller_kubernetes import kubernetesGetPodId
# from app_controller_gitlab import gitlabGeneratePersonalAccessToken

"""
1. deploy,service,ingress - done
2. install plugin/extension via cli/script
3. connect to gitlab
3. connect to kubernetes host
4. trigger from gitlab push
5. deploy to kubernetes
"""

# Installs Gitlab & Git Plugin
def jenkinsInstallPlugin(clusterName,userName):
    url = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/pluginManager/install"
    
    payload = "json=%7B%20%22GitLab%22%3A%20%7B%22default%22%3A%20true%7D%2C%22docker-build-step%22%3A%7B%22default%22%3Atrue%7D%2C%22Kubernetes%20Continuous%20Deploy%22%3A%20%7B%22default%22%3A%20true%7D%2C%22Git%22%3A%20%7B%22default%22%3A%20true%7D%7D&dynamicLoad=Install%20without%20restart&plugin.git.default=on&plugin.gitlab-plugin.default=on&plugin.kubernetes-cd.default=on&plugin.docker-build-step.default=on"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Host': "jenkins-"+userName+"."+clusterName+".securethebox.us",
        'accept-encoding': "gzip, deflate",
        'content-length': "202",
        'Connection': "keep-alive"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)

def jenkinsRestartServer(clusterName,userName):
    url = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/restart"
    response = requests.request("GET", url)
    print(response.status_code)

    url2 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/restart"
    payload2 = "json=%7B%7D&Submit=Yes"
    response2 = requests.request("POST",url2,data=payload2)
    print(response2.status_code)

# 3.
def jenkinsConnectGitlab(api_token,clusterName,userName):
    # 1. Add Gitlab Credentials
    url1 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/descriptor/com.cloudbees.plugins.credentials.CredentialsSelectHelper/resolver/com.cloudbees.plugins.credentials.CredentialsSelectHelper$SystemContextResolver/provider/com.cloudbees.plugins.credentials.SystemCredentialsProvider$ProviderImpl/context/jenkins/addCredentials"
    headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # encoded_api_token = str(urllib.parse.quote(api_token))
    payload1 = "_.domain=_&_.scope=GLOBAL&_.username=&_.password=&_.id=&_.description=&stapler-class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&_.scope=GLOBAL&_.apiToken="+api_token+"&_.id=gitlab-token&_.description=&stapler-class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&%24class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&stapler-class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&%24class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&stapler-class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&json=%7B%22domain%22%3A+%22_%22%2C+%22%22%3A+%221%22%2C+%22credentials%22%3A+%7B%22scope%22%3A+%22GLOBAL%22%2C+%22apiToken%22%3A+%22"+api_token+"%22%2C+%22%24redact%22%3A+%22apiToken%22%2C+%22id%22%3A+%22gitlab-"+userName+"-root-token-id%22%2C+%22description%22%3A+%22%22%2C+%22stapler-class%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl%22%2C+%22%24class%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl%22%7D%7D"
    response1 = requests.request("POST",url1, data=payload1, headers=headers1)
    print("RESPONSE 2:",response1.status_code)

    #2. Test Connection
    url2 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/descriptorByName/com.dabsquared.gitlabjenkins.connection.GitLabConnectionConfig/testConnection"
    headers2 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload2 = "apiTokenId=gitlab-"+userName+"-root-token-id&clientBuilderId=autodetect&url=http%3A%2F%2Fgitlab-"+userName+"&ignoreCertificateErrors=false"
    response2 = requests.request("POST",url2, data=payload2, headers=headers2)
    # Response should be Success
    print("RESPONSE 2:",response2.text)

    # 3. Apply
    url3 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/configSubmit"
    headers3 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload3 = "system_message=&_.numExecutors=2&_.labelString=&master.mode=NORMAL&_.quietPeriod=5&_.scmCheckoutRetryCount=0&namingStrategy=0&stapler-class=jenkins.model.ProjectNamingStrategy%24DefaultProjectNamingStrategy&%24class=jenkins.model.ProjectNamingStrategy%24DefaultProjectNamingStrategy&stapler-class=jenkins.model.ProjectNamingStrategy%24PatternProjectNamingStrategy&%24class=jenkins.model.ProjectNamingStrategy%24PatternProjectNamingStrategy&_.namePattern=.*&_.description=&durabilityHint=null&_.usageStatisticsCollected=on&_.useAuthenticatedEndpoint=on&_.name=gitlab-"+userName+"-root-connection&id=com.dabsquared.gitlabjenkins.connection.GitLabConnection%40b025587&_.url=http%3A%2F%2Fgitlab-"+userName+"&_.apiTokenId=gitlab-"+userName+"-root-token-id&_.clientBuilderId=autodetect&_.connectionTimeout=10&_.readTimeout=10&_.appInsightsEnabled=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&_.url=http%3A%2F%2Fjenkins-"+userName+"."+clusterName+".securethebox.us%2F&_.adminAddress=address+not+configured+yet+%3Cnobody%40nowhere%3E&_.globalConfigName=&_.globalConfigEmail=&_.shell=&_.dockerUrl=&_.dockerVersion=&_.dockerCertPath=&_.smtpServer=&_.defaultSuffix=&_.smtpAuthUserName=&_.smtpAuthPasswordSecret=&_.smtpPort=&_.replyToAddress=&_.charset=UTF-8&sendTestMailTo=&core%3Aapply=&json=%7B%22system_message%22%3A+%22%22%2C+%22jenkins-model-MasterBuildConfiguration%22%3A+%7B%22numExecutors%22%3A+%222%22%2C+%22labelString%22%3A+%22%22%2C+%22mode%22%3A+%22NORMAL%22%7D%2C+%22jenkins-model-GlobalQuietPeriodConfiguration%22%3A+%7B%22quietPeriod%22%3A+%225%22%7D%2C+%22jenkins-model-GlobalSCMRetryCountConfiguration%22%3A+%7B%22scmCheckoutRetryCount%22%3A+%220%22%7D%2C+%22jenkins-model-GlobalProjectNamingStrategyConfiguration%22%3A+%7B%7D%2C+%22jenkins-model-GlobalNodePropertiesConfiguration%22%3A+%7B%22globalNodeProperties%22%3A+%7B%7D%7D%2C+%22org-jenkinsci-plugins-workflow-flow-GlobalDefaultFlowDurabilityLevel%22%3A+%7B%22durabilityHint%22%3A+%22null%22%7D%2C+%22hudson-model-UsageStatistics%22%3A+%7B%22usageStatisticsCollected%22%3A+%7B%7D%7D%2C+%22com-dabsquared-gitlabjenkins-connection-GitLabConnectionConfig%22%3A+%7B%22useAuthenticatedEndpoint%22%3A+true%2C+%22connections%22%3A+%7B%22name%22%3A+%22gitlab-"+userName+"-root-connection%22%2C+%22id%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabConnection%40b025587%22%2C+%22url%22%3A+%22http%3A%2F%2Fgitlab-"+userName+"%22%2C+%22apiTokenId%22%3A+%22gitlab-"+userName+"-root-token-id%22%2C+%22clientBuilderId%22%3A+%22autodetect%22%2C+%22ignoreCertificateErrors%22%3A+false%2C+%22connectionTimeout%22%3A+%2210%22%2C+%22readTimeout%22%3A+%2210%22%7D%7D%2C+%22app-insights-plugin-configuration%22%3A+%7B%22appInsightsEnabled%22%3A+true%7D%2C+%22jenkins-management-AdministrativeMonitorsConfiguration%22%3A+%7B%22administrativeMonitor%22%3A+%5B%22hudson.PluginManager%24PluginCycleDependenciesMonitor%22%2C+%22hudson.PluginManager%24PluginUpdateMonitor%22%2C+%22hudson.PluginWrapper%24PluginWrapperAdministrativeMonitor%22%2C+%22hudsonHomeIsFull%22%2C+%22hudson.diagnosis.NullIdDescriptorMonitor%22%2C+%22OldData%22%2C+%22hudson.diagnosis.ReverseProxySetupMonitor%22%2C+%22hudson.diagnosis.TooManyJobsButNoView%22%2C+%22hudson.model.UpdateCenter%24CoreUpdateMonitor%22%2C+%22hudson.node_monitors.MonitorMarkedNodeOffline%22%2C+%22hudson.triggers.SCMTrigger%24AdministrativeMonitorImpl%22%2C+%22jenkins.diagnosis.HsErrPidList%22%2C+%22jenkins.diagnostics.CompletedInitializationMonitor%22%2C+%22jenkins.diagnostics.RootUrlNotSetMonitor%22%2C+%22jenkins.diagnostics.SecurityIsOffMonitor%22%2C+%22jenkins.diagnostics.URICheckEncodingMonitor%22%2C+%22jenkins.model.DownloadSettings%24Warning%22%2C+%22jenkins.model.Jenkins%24EnforceSlaveAgentPortAdministrativeMonitor%22%2C+%22jenkins.security.QueueItemAuthenticatorMonitor%22%2C+%22jenkins.security.RekeySecretAdminMonitor%22%2C+%22jenkins.security.UpdateSiteWarningsMonitor%22%2C+%22jenkins.security.apitoken.ApiTokenPropertyDisabledDefaultAdministrativeMonitor%22%2C+%22jenkins.security.apitoken.ApiTokenPropertyEnabledNewLegacyAdministrativeMonitor%22%2C+%22legacyApiToken%22%2C+%22jenkins.security.csrf.CSRFAdministrativeMonitor%22%2C+%22slaveToMasterAccessControl%22%2C+%22jenkins.security.s2m.MasterKillSwitchWarning%22%2C+%22jenkins.slaves.DeprecatedAgentProtocolMonitor%22%5D%7D%2C+%22jenkins-model-JenkinsLocationConfiguration%22%3A+%7B%22url%22%3A+%22http%3A%2F%2Fjenkins-"+userName+"."+clusterName+".securethebox.us%2F%22%2C+%22adminAddress%22%3A+%22address+not+configured+yet+%3Cnobody%40nowhere%3E%22%7D%2C+%22hudson-plugins-git-GitSCM%22%3A+%7B%22globalConfigName%22%3A+%22%22%2C+%22globalConfigEmail%22%3A+%22%22%2C+%22createAccountBasedOnEmail%22%3A+false%7D%2C+%22hudson-tasks-Shell%22%3A+%7B%22shell%22%3A+%22%22%7D%2C+%22org-jenkinsci-plugins-dockerbuildstep-DockerBuilder%22%3A+%7B%22dockerUrl%22%3A+%22%22%2C+%22dockerVersion%22%3A+%22%22%2C+%22dockerCertPath%22%3A+%22%22%7D%2C+%22hudson-tasks-Mailer%22%3A+%7B%22smtpServer%22%3A+%22%22%2C+%22defaultSuffix%22%3A+%22%22%2C+%22useSsl%22%3A+false%2C+%22smtpPort%22%3A+%22%22%2C+%22replyToAddress%22%3A+%22%22%2C+%22charset%22%3A+%22UTF-8%22%7D%2C+%22core%3Aapply%22%3A+%22%22%7D&Submit=Save"
    # Response should be saved
    response3 = requests.request("POST",url3, data=payload3, headers=headers3)
    print("RESPONSE 3:",response3.text)

    # generate ssh keypair with no password (within container)
def jenkinsCreateSSHKeypair(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)
    subprocess.Popen([f"docker exec -i "+container_id+"  bash -c \"ssh-keygen -f /id_rsa -t rsa -N '' -y\""],shell=True).wait()

def jenkinsGetSSHPublicKey(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)
    public = check_output(["docker", "exec","-i",container_id,"bash","-c","cat id_rsa.pub"])
    ssh_public_key = public.decode("utf-8")
    print("PUBLIC KEY:",ssh_public_key)
    return ssh_public_key

def jenkinsGetSSHPrivateKey(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    print("POD ID:",pod_id)
    container_id = dockerGetContainerId(pod_id)
    print("CONTAINER ID:",container_id)
    private = check_output(["docker", "exec","-i",container_id,"bash","-c","cat id_rsa"])
    ssh_private_key = private.decode("utf-8")
    print("PRIVATE KEY:",ssh_private_key)
    return ssh_private_key


    # add private key to jenkins
    # ssh-keygen -f id_rsa -t rsa -N ''
    # cat /root/.ssh/id_rsa
    # cat /root/.ssh/id_rsa.pub
    # id = jenkins-charles-root-private-key

    # create job
    # name: deploy-to-kubernetes
    
    # source code management in jenkins (must make repo public and add public key first):
    # Repository URL: http://gitlab-"+userName+"/root/juice-shop-"+userName

    # Run docker command in container to update changes
    # docker exec -i 557ccefcc2ca  bash -c "cd juice-shop-charles ; git pull"

def main():
    # jenkinsInstallPlugin('"+clusterName+"','"+userName+"')
    # time.sleep(30)
    # api_token = gitlabGeneratePersonalAccessToken()
    # print("API TOKEN:",api_token)
    # jenkinsConnectGitlab(api_token,"us-west1-a","charles")
    # time.sleep(30)
    # jenkinsRestartServer('"+clusterName+"','"+userName+"')
    jenkinsGetSSHPublicKey('jenkins','charles')

if __name__ == "__main__":
    main()