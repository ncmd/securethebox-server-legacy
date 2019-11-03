# securethebox-server
# Requirements:
- python3.7.x
- npm 6.x
- nodejs 12.x

# How to make changes to this repo
- Refer to this repo https://github.com/ncmd/git-scripted

# Dev Setup
- Install nodejs tools
```
npm install -g cross-var
npm install -g commitizen
npm install -g npm-run-all
```

- Install Python Dependencies
```
pip3 install virtualenv
python3 -m venv 
. venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

# Updating App
- Merge origin master with fork master
```
npm run sync-fork-master
```
- Updating local fork master
```
npm run sync
```



# Kubernetes Cluster Setup
**Create Kubernetes cluster**
```
gcloud config set project "securethebox"
gcloud config set compute/region "us-west1"
gcloud config set compute/zone "us-west1-a"

gcloud beta container --project "securethebox" clusters create "us-west1-a" --zone "us-west1-a" --no-enable-basic-auth --cluster-version "1.12.7-gke.7" --machine-type "g1-small" --image-type "COS" --disk-type "pd-standard" --disk-size "30" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "1" --enable-cloud-logging --enable-cloud-monitoring --enable-ip-alias --network "projects/securethebox/global/networks/default" --subnetwork "projects/securethebox/regions/us-west1/subnetworks/default" --default-max-pods-per-node "8" --addons HorizontalPodAutoscaling,HttpLoadBalancing --enable-autoupgrade --enable-autorepair

gcloud container clusters get-credentials "us-west1-a"
```

# ExternalDNS Setup
**Create a DNS zone which will contain the managed DNS records.**
```
gcloud dns managed-zones create "us-west1-a-securethebox-us" \
    --dns-name "us-west1-a.securethebox.us." \
    --description "Automatically managed zone by kubernetes.io/external-dns"
```
**Make a note of the nameservers that were assigned to your new zone.**
```
gcloud dns record-sets list \
    --zone "us-west1-a-securethebox-us" \
    --name "us-west1-a.securethebox.us." \
    --type NS

kubectl create clusterrolebinding your-user-cluster-admin-binding --clusterrole=cluster-admin --user=cchong.vise@gmail.com
```
**Tell the parent zone where to find the DNS records for this zone by adding the corresponding NS records there. Assuming the parent zone is "gcp-zalan-do" and the domain is "gcp.zalan.do" and that it's also hosted at Google we would do the following.**
```
gcloud dns record-sets transaction start --zone "securethebox-us"
gcloud dns record-sets transaction add ns-cloud-d{1..4}.googledomains.com. \
    --name "us-west1-a.securethebox.us." --ttl 300 --type NS --zone "securethebox-us"
gcloud dns record-sets transaction execute --zone "securethebox-us"
```
**Deploy RBAC ExternalDNS**
```
kubectl apply -f rbac-external-dns.yml
```

# Heroku Deployment
## Deploying a Kubectl client to Heroku
```
cd /Users/charleschong/go/src/
heroku destroy stb-server --confirm stb-server
git clone https://github.com/ncmd/python-getting-started.git
cd python-getting-started/
heroku create stb-server
git push heroku master
heroku ps:scale web=1
heroku buildpacks:add https://github.com/ncmd/heroku-buildpack-google-cloud.git -a stb-server
heroku config:set GOOGLE_CREDENTIALS=$(base64 ~/.kube/private.json) PROJECT=securethebox INSTALL_KUBECTL=true ZONE=us-west1-a -a stb-server
touch t
git add .
git commit -m "T"
git push heroku master
echo y | heroku ps:exec -a stb-server /bin/echo "test"
export kubectl_config_server=$(kubectl config view --raw -o jsonpath='{.clusters[].cluster.server}')
export kubectl_config_user=$(kubectl config view --raw -o jsonpath='{.users[].name}')
export kubectl_config_cluster=$(kubectl config view --raw -o jsonpath='{.clusters[].name}')
export kubectl_config_certificate_authority=$(kubectl config view --raw -o jsonpath='{.clusters[].cluster.certificate-authority-data}')
heroku ps:exec -a stb-server /app/vendor/google-cloud-sdk/bin/kubectl config set-cluster gke_securethebox_us-west1-a_us-west1-a --server=$kubectl_config_server \
    heroku ps:exec -a stb-server /app/vendor/google-cloud-sdk/bin/kubectl config set-context gke_securethebox_us-west1-a_us-west1-a --user=$kubectl_config_user --cluster=$kubectl_config_cluster && \ 
    heroku ps:exec -a stb-server /app/vendor/google-cloud-sdk/bin/kubectl config set-cluster gke_securethebox_us-west1-a_us-west1-a --certificate-authority=$kubectl_config_certificate_authority && \
    heroku ps:exec -a stb-server /app/vendor/google-cloud-sdk/bin/gcloud container clusters get-credentials "us-west1-a" 
```

# Deploying Services
```
heroku ps:exec -a stb-server /app/vendor/google-cloud-sdk/bin/kubectl apply -f ./verify.yml
```

**Check DNS records created in CLOUD DNS**
```
gcloud dns record-sets list \
    --zone "us-west1-a-securethebox-us" \
    --name "traefik.us-west1-a.securethebox.us."
```
**Check domain is resolvable**
```
dig +short @ns-cloud-d1.googledomains.com. traefik.us-west1-a.securethebox.us.
```

# Monitoring & Troubleshooting
**Check Heroku Kubectl Server Status**
```
heroku logs -a stb-server --tail
```

**Deploy with Cloudcmd**
```
heroku config:set CLOUDCMD_AUTH=false CLOUDCMD_COLUMNS=name-size-date-owner-mode CLOUDCMD_CONFIG_AUTH=false CLOUDCMD_CONFIG_DIALOG=false CLOUDCMD_CONFIRM_COPY=true CLOUDCMD_CONFIRM_MOVE=true CLOUDCMD_CONSOLE=true CLOUDCMD_CONTACT=true CLOUDCMD_EDITOR=edward CLOUDCMD_EXPORT=false CLOUDCMD_EXPORT_TOKEN=root CLOUDCMD_IMPORT=false CLOUDCMD_IMPORT_LISTEN=false CLOUDCMD_IMPORT_TOKEN=root CLOUDCMD_IMPORT_URL=http://localhost:8000 CLOUDCMD_KEYS_PANEL=true CLOUDCMD_ONE_FILE_PANEL=false CLOUDCMD_OPEN=false CLOUDCMD_PASSWORD=toor CLOUDCMD_SHOW_FILE_NAME=false CLOUDCMD_SYNC_CONSOLE_PATH=false CLOUDCMD_TERMINAL=true CLOUDCMD_TERMINAL_PATH=gritty CLOUDCMD_USERNAME=root CLOUDCMD_VIM=false NPM_CONFIG_PRODUCTION=false -a stb-server 
```

# Deleting Kubernetes

**Cleanup**
```
gcloud config set project "securethebox"
gcloud config set compute/region "us-west1"
gcloud config set compute/zone "us-west1-a"
echo y | gcloud container clusters delete "us-west1-a"
```

# Managing Local DNS with dnsmasq for Local Traefik Kubernetes
https://medium.com/localz-engineering/kubernetes-traefik-locally-with-a-wildcard-certificate-e15219e5255d

```
brew install nss mkcert
sudo brew services start dnsmasq
sudo killall -HUP mDNSResponder
mkcert '*.securethebox.us'
mkcert '*.us-west1-a.securethebox.us'
mkcert -install
kubectl -n default create secret tls traefik-tls-cert --key=_wildcard.securethebox.us-key.pem --cert=_wildcard.securethebox.us.pem
kubectl -n default create secret tls traefik-tls-cert --key=_wildcard.us-west1-a.securethebox.us-key.pem --cert=_wildcard.us-west1-a.securethebox.us.pem
kubectl -n default delete secret traefik-tls-cert

sudo vi /usr/local/etc/dnsmasq.conf
address=/us-west1-a.securethebox.us/127.0.0.1


sudo vi /etc/resolver/dev
dig securethebox.us @127.0.0.1
```

**Traefik Setup**
- https://www.digitalocean.com/community/tutorials/how-to-use-traefik-as-a-reverse-proxy-for-docker-containers-on-ubuntu-18-04
```
docker network create challenge1
touch acme.json
chmod 600 acme.json
docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $PWD/traefik.toml:/traefik.toml \
  -v $PWD/acme.json:/acme.json \
  -p 80:80 \
  -p 443:443 \
  -l traefik.frontend.rule=Host:monitor.securethebox.us \
  -l traefik.port=8080 \
  --network challenge1 \
  --name traefik \
  traefik:1.7.10-alpine
```

**Getting shell of docker container:**
```
docker exec -it c71a87c88a1e /bin/bash
docker exec -it 677912a06309 /bin/sh
```

**Installing and Starting Cloudcmd on Alpine:**
```
docker exec -u root -it dcdd24377a97 npm install -g cloudcmd && cloudcmd --port 7000 --no-open
docker exec -u root -it dcdd24377a97 which cloudcmd
/usr/local/bin/cloudcmd
docker exec -u root -it dcdd24377a97 npm install -g forever
docker exec -u root -it dcdd24377a97 forever start /usr/local/bin/cloudcmd
```

**Open a new port 8080:8080 on Container container_id_01**
```
docker stop container_id_01
docker commit container_id_01 container_id_02
docker run -p 8080:8080 -td container_id_02
```

**Getting Network information of container:**
```
docker inspect container_id_here | grep IPAddressdocker
```

**Proxying port 8080 of host to port 80 on container**
```
docker run --name container_name -d -p 8080:80 container_image_name
```

**Setup Nginx Conf and Cloudcmd for nginx-modsecurity**
```
docker-compose up -d
docker cp ./nginx.conf securethebox-challenge_nginx-modsecurity_1:/etc/nginx/nginx.conf
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 cat /etc/nginx/nginx.conf
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 nginx -s reload
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 apk add nodejs nodejs-npm
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 npm install -g cloudcmd
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 npm install -g forever
docker exec -u root -it securethebox-challenge_nginx-modsecurity_1 forever start /usr/bin/cloudcmd --port 7000
docker exec -it securethebox-challenge_nginx-modsecurity_1 /bin/sh
```

**Install and Start Cloudcmd for juice-shop**
```
docker exec -u root -it securethebox-challenge_juice-shop_1 npm install -g cloudcmd
docker exec -u root -it securethebox-challenge_juice-shop_1 npm install -g forever
docker exec -u root -it securethebox-challenge_juice-shop_1 forever start /usr/local/bin/cloudcmd --port 7000
docker exec -it securethebox-challenge_juice-shop_1 /bin/sh
```

**juicebox setup**
```
docker run --rm -p 3000:3000 bkimminich/juice-shop
```

**nginx config**
```
server {
    listen       80;
    server_name  localhost;
    modsecurity on;
    location / {
        rewrite ^/juice-shop(.*) /$1 break;
        proxy_pass http://juice-shop:3000;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

## Tiller and Helm commands
```
helm list --host="localhost:44134"

helm delete quarrelsome-umbrellabird --purge --host="localhost:44134"
```