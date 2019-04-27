import sys

def writeConfig(**kwargs):
    template = """
user nginx nginx;
worker_processes  1;
load_module modules/ngx_http_modsecurity_module.so;
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server_names_hash_max_size 6144;
    server_names_hash_bucket_size 128;
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/modsec_includes.conf;
    server {
        listen       80;
        server_name  localhost;
        location / {
            rewrite ^/juice-shop(.*) /$1 break;
            proxy_pass   http://{serviceName}-{userName};
        }
        include /etc/nginx/insert.d/*.conf;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
include /etc/nginx/conf.d/*.conf;
}
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-nginx.conf', 'w') as yfile:
        yfile.write(template.format(**kwargs))

# usage:
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))