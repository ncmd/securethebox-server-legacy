'''
TODO:
- NEED TO SPLIT UP CHALLENGES
- deployment files resource tuning

- get status of pod
    - kubectl get pod --field-selector=status.phase=Succeeded

- Splunk port forwarding needs to work (it does, but needed portforwarding)
    - https://github.com/splunk/docker-splunk/tree/develop/test_scenarios/kubernetes
    - kubectl port-forward splunk-charles-c76dd785b-h866v 8000:8000
    kubectl port-forward dokku-charles-55bbfd6578-tvrhp 8000:80
    kubectl port-forward hashicorp-vault-charles-66d99fc8cc-rqb5w 8200:8200

- Generating Answers
    - attacker_ip_address
    - perform sqli/xss

- Install Codebox to edit code (Perhaps use gitpod browser extension)
    - make it easier to edit code

-  Setup Each user has its own "namespace" in kubernetes
    - https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-organizing-with-namespaces

- Create Network Policies (for own namespace to prevent docker.socket mount)
    - https://kubernetes.io/docs/concepts/services-networking/network-policies/

- Automated checks to score user (somewhat working)
    - Check if service is running

- Timer need to FREEZE (not destroy) environment after X time
    - After 2hrs

- Generate password for cloudcmd

- pvc needs to be unique per user. pvc needs to be deleted after challenge end

- add wireshark https://hub.docker.com/r/ffeldhaus/wireshark

- need to fix time, timestamp for logs is wrong...

- add attack server (Kali linux pod running script)

- need to add a detection answer to detect attacker activity
'''