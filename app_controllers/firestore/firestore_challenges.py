import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from challenge_models import Challenge
import datetime

# Use a service account
cred = credentials.Certificate('../../secrets/firestore-stb-prod.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# def challenge_apps(app_list):
#     for app in app_list:
#         if app == ""

def challenge_1(username):
    this_challenge = Challenge("Learning the Environment","Simulated business environment supporting security for an Application")
    this_challenge.category = "infrastructure"
    this_challenge.duration = 45
    this_challenge.difficulty = 3
    this_challenge.grading_criteria = ["vocal","ctf","definitions","video"]
    this_challenge.overview = "Gauging a cadidate's skill on infrastructure security"
    this_challenge.apps = ["juice-shop","splunk","nginx-modsecurity","gitlab",
                           "jenkins"]

    # JUICE-SHOP
    juice_shop_index = 0
    this_challenge.add_resource("juice-shop","Main Application and most Valueable service. Keep this service up at all times apply your knowledge of security.","http://juice-shop-username.us-west1-a.securethebox.us/","http://juice-shop-username-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(juice_shop_index,"admin@someemail.com","admin123")
    this_challenge.add_resource_reference(juice_shop_index,"Juice-Shop Source Code Repository",'https://github.com/bkimminich/juice-shop')
    this_challenge.add_resource_reference(juice_shop_index,"About Juice-Shop","https://www.owasp.org/index.php/OWASP_Juice_Shop_Project")
    this_challenge.add_resource_reference(juice_shop_index,"Node-Vault node library","https://github.com/kr1sp1n/node-vault")
    this_challenge.add_resource_reference(juice_shop_index,"Csurf CSRF token node library","https://github.com/expressjs/csurf")
    this_challenge.add_resource_reference(juice_shop_index,"Content Security Policy (CSP) Cheatsheet","https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Content_Security_Policy_Cheat_Sheet.md")
    this_challenge.add_resource_tip(juice_shop_index,"Frontend/Client = Angular.js")
    this_challenge.add_resource_tip(juice_shop_index,"Backend/Server = Node.js+Express")
    this_challenge.add_resource_tip(juice_shop_index,"Authentication = SQL+JWT")
    this_challenge.add_resource_tip(juice_shop_index,"Change default passwords")
    this_challenge.add_resource_tip(juice_shop_index,"Patch code in gitlab repository to fix vulnerabilities")
    this_challenge.add_resource_tip(juice_shop_index,"Use Node-Vault library to request for secrets")
    this_challenge.add_resource_tip(juice_shop_index,"Use CSurf middleware to add csrf token to requests")
    this_challenge.add_resource_tip(juice_shop_index,"Change default passwords")

    # SPLUNK
    splunk_index = 1
    this_challenge.add_resource("splunk","Security Incident Event Management","http://splunk-username.us-west1-a.securethebox.us/","http://splunk-username-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(splunk_index,"admin","Changeme")
    this_challenge.add_resource_reference(splunk_index,"Splunk Cheat Sheet","https://lzone.de/cheat-sheet/Splunk")
    this_challenge.add_resource_reference(splunk_index,"About Juice-Shop","https://www.owasp.org/index.php/OWASP_Juice_Shop_Project")
    this_challenge.add_resource_tip(splunk_index,"source=\"/var/log/challenge1/nginx-username.log\"")
    this_challenge.add_resource_tip(splunk_index,"source=\"/var/log/challenge1/modsecurity-username.log\"")
    this_challenge.add_resource_tip(splunk_index,"Set time frame of search to REAL-TIME 1 hour window.")
    this_challenge.add_resource_tip(splunk_index,"Adjust to Verbose Mode search.")
    this_challenge.add_resource_tip(splunk_index,"Consider the fields: status, http_method, uri_path, uri_query, http_user_agent, and http_referrer.")

    # NGINX-MODSECURITY
    nginx_modsecurity_index = 2
    this_challenge.add_resource("nginx-modsecurity","Load Balancer + Web Application Firewall","http://nginx-modsecurity-username.us-west1-a.securethebox.us/","http://nginx-modsecurity-username-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(nginx_modsecurity_index,"none","none")
    this_challenge.add_resource_reference(nginx_modsecurity_index,"OWASP Core Rule Set","https://modsecurity.org/crs/")
    this_challenge.add_resource_tip(nginx_modsecurity_index,"source=\"/var/log/challenge1/nginx-username.log\"")
    this_challenge.add_resource_tip(nginx_modsecurity_index,"source=\"/var/log/challenge1/modsecurity-username.log\"")
    this_challenge.add_resource_tip(nginx_modsecurity_index,"To enable Modsecurity edit the /etc/nginx/nginx.conf file")
    this_challenge.add_resource_tip(nginx_modsecurity_index,"To modify Modsecurity edit /etc/nginx/modsec/modsecurity.conf file")
    this_challenge.add_resource_tip(nginx_modsecurity_index,"Reload nginx after changes with the command \"nginx -s reload\"")

    # GITLAB
    gitlab_index = 3
    this_challenge.add_resource("gitlab","Source Code Respository","http://gitlab-username.us-west1-a.securethebox.us/","http://gitlab-username-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(gitlab_index,"root","Changeme")
    this_challenge.add_resource_reference(gitlab_index,"Gitlab Git Cheatsheet","https://about.gitlab.com/images/press/git-cheat-sheet.pdf")
    this_challenge.add_resource_reference(gitlab_index,"Github Security Best Practices Cheat Sheet","https://snyk.io/blog/ten-git-hub-security-best-practices/")
    this_challenge.add_resource_tip(gitlab_index,"You can edit code directly from the Repository")
    this_challenge.add_resource_tip(gitlab_index,"Use Node-Vault to get Secrets")
    this_challenge.add_resource_tip(gitlab_index,"Create policies for read/write")

    # JENKINS
    jenkins_index = 4
    this_challenge.add_resource("jenkins","Continuous Integration & Continuous Deployment Server","http://jenkins-username.us-west1-a.securethebox.us/","http://jenkins-username-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(jenkins_index,"none","none")
    this_challenge.add_resource_reference(jenkins_index,"Jenkins Cheatsheet","https://www.edureka.co/blog/cheatsheets/jenkins-cheat-sheet/")
    this_challenge.add_resource_tip(jenkins_index,"When a changes happens in github project, jenkins run \"git pull\" command on juice-shop docker container to update changes to app")
    this_challenge.add_resource_tip(jenkins_index,"Edit the \"deploy-to-kubernetes\" job")
    this_challenge.add_resource_tip(jenkins_index,"Run \"Setup Security\" to add authentication")
    this_challenge.add_resource_tip(jenkins_index,"You do not need to \"build\" a docker image or \"deploy\", you just need to make changes in gitlab repository")

    # # HASHICORP VAULT
    # hashicorp_vault_index = 5

    # # HASHICORP CONSUL
    # hashicorp_consul_index = 6

    # QUESTIONS
    this_challenge.add_question("ctf", "")






    this_challenge.print_challenge()


if __name__ == "__main__":
    
    challenge_1("charles")



"""
challenges -> id ->
    challenge_id
    challenge_title
    challenge_description
    challenge_overview
    challenge_published |
        - MM/DD/YYYY
    challenge_last_update |
        - MM/DD/YYYY
    challenge_difficulty |
        - Level 1 - 5
    challenge_tags: [] 
    challenge_category |
        - web applications
        - secrets management
        - git repository
        - ids/ips
        - tls/ssl, pki
        - operating system internals
        - code review
        - pentesting
        - infrastructure
        - cryptography
        - vpn
        - identity access management
        - incident response
        - forensics
        - business
        - leadership
    challenge_duration |
        - 10 minutes - 2 hours
    challenge_grading_criteria
        - must pass | 
            - coding
            - verbal
            - video
            - ctf
            - etc...
    challenge_enabled_apps
        - kali
        - gitlab
        - splunk
        - juice-shop
    challenge_scenario_topology
        - json format
    challenge_resources |
        url |
            - kali-username.us-west1-a.securethebox.com
        shell |
            - kali-shell-username.us-west1-a.securethebox.com
        credentials |
            - username
            - password
        references |
            - url1
        tips | 
            - tip1
    challenge_video_questions |
        - id
        - question_description
        - helper_attachments
        - helper_urls
        - helper_images
    challenge_vocal_questions
    challenge_coding_questions
    challenge_typed_questions
    challenge_ctf_questions
    challenge_video_submission
    challenge_vocal_submission
    challenge_coding_submission
    challenge_typed_submission
    challenge_ctf_submission


"""