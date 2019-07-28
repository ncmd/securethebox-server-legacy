import unittest
import setup
import os
"""
start = time.time()
        # # 1. Generate Yaml Ingress Files
        # generateKubernetesIngressYaml(clusterName, 'traefik')
        # # 2. Deploy Ingress Pods
        # manageKubernetesIngressPod(clusterName, 'traefik', action)
        # # 3. Generate Yaml Service Files
        # time.sleep(10)
        # # SETUP GITLAB
        # generateKubernetesServicesYaml(clusterName, 'gitlab',userName)
        # manageKubernetesServicesPod(clusterName,'gitlab',userName, action)
        # generateKubernetesServicesYaml(clusterName, 'jenkins',userName)
        # manageKubernetesServicesPod(clusterName,'jenkins',userName, action)
        # print("Sleeping 100 seconds")
        # time.sleep(100)
        # print("Finished sleeping ...")
        # reset_token,session_cookie = gitlabGetResetPasswordToken(clusterName,userName)
        # gitlabPostResetPassword(reset_token,session_cookie,clusterName,userName)
        # gitlabCreateProject(clusterName, userName)
        # gitlabMakeProjectPublic(clusterName, userName)
        # gitlabProjectAllowOutbound(clusterName, userName)
        # gitlabProjectAddWebhook(clusterName, userName)
        # # SETUP APP SERVER
        # os.chdir('..')
        # os.chdir('..')
        # print("---------------------------CWD:",os.getcwd())
        # generateKubernetesServicesYaml(clusterName, 'juice-shop',userName)
        # manageKubernetesServicesPod(clusterName,'juice-shop', userName, action)
        # # wait for app to fully deploy
        # # time.sleep(120)
        # # SETUP JENKINS
        # jenkinsInstallPlugin("us-west1-a",userName)
        # print("Plugin Installed")
        # time.sleep(30)
        # api_token = gitlabCreatePersonalAccessToken()
        # print("API TOKEN:",api_token)
        # jenkinsConnectGitlab(api_token,"us-west1-a",userName)
        # time.sleep(30)
        # jenkinsRestartServer("us-west1-a",userName)
        # print("DONE")
        # time.sleep(30)
        # jenkinsCreateSSHKeypair('jenkins',userName)
        # jenkinsCreateJob('jenkins',userName)
        # public_key = jenkinsGetSSHPublicKey('jenkins',userName)
        # gitlabProjectAddDeployKey(public_key,clusterName,userName)
        # end = time.time()
        # print("EVERYTHING SHOULD BE DONE! Time elapsed:",end - start)
        
        


        generateKubernetesServicesYaml(clusterName, 'nginx-modsecurity',userName)
        
        # generateKubernetesServicesYaml(clusterName, 'splunk',userName)
        # generateKubernetesServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        
        # # generateKubernetesPodsYaml(clusterName, 'kali-linux',userName)
        # # 4. Deploy Service pods
        # manageKubernetesServicesPod(clusterName,'nginx-modsecurity', userName, action)
        
        # manageKubernetesServicesPod(clusterName,'splunk', userName, action)
        # manageKubernetesServicesPod(clusterName,'splunk-universal-forwarder',userName, action)
        
        # # manageKubernetesPods(clusterName,'kali-linux',userName, action)
        # # manageKubernetesServicesPod(clusterName,'wireshark',userName, action)

        # print("WAF setup")
        # setupWAF(clusterName, 'juice-shop', userName)
        
        # print("Splunk Universal Forwarder Setup")
        # setupSplunkForwarderLogging(clusterName, 'splunk-universal-forwarder', userName)

        # # Setup Cloudcmd
        # print("Cloudcmd Setup")
        # setupCLOUDCMD(clusterName, 'nginx-modsecurity', userName)
        # setupCLOUDCMD(clusterName, 'juice-shop', userName)

        # # Setup Attacker
        # setupAttacker(clusterName,'kali-linux',userName)

        # Setup Port Forwarding
        # setupSplunkMaster(clusterName,userName)
        
"""
class TestStringMethods(unittest.TestCase):
    def test_kubernetes_(self):
	    self.assertEqual(setup.accept_xcode_license(), True)
    def test_install_golang(self):
        self.assertEqual(setup.install_golang(), True)
    def test_install_update_ruby(self):
        self.assertEqual(setup.install_update_ruby(), True)
    def test_install_homebrew(self):
        self.assertEqual(setup.install_homebrew(), True)
    def test_install_node_yarn(self):
        self.assertEqual(setup.install_node_yarn(), True)
    def test_install_node_global_tools(self):
        self.assertEqual(setup.install_node_global_tools(), True)
    def test_install_github_desktop(self):
        self.assertEqual(setup.install_github_desktop(), True)
    def test_install_sublime_text(self):
        self.assertEqual(setup.install_sublime_text(), True)
    def test_install_postman(self):
        self.assertEqual(setup.install_postman(), True)
    def test_install_fastlane(self):
        self.assertEqual(setup.install_fastlane('test@gmail.com'), True)
    def test_install_travis_cli(self):
        self.assertEqual(setup.install_travis_cli(), True)

if __name__ == '__main__':
    unittest.main()