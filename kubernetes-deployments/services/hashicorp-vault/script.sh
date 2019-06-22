#!/usr/bin/env bash
set -e
set -o pipefail

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_SKIP_VERIFY=true

vault login root

vault policy write app-readonly -<<EOF
path "database/creds/readonly" {
  capabilities = ["read"]
}
EOF

vault auth enable userpass
for u in sally bobby chris devin; do
  vault write auth/userpass/users/$u password=password policies=app-readonly
done

vault kv put secret/foo a=b
vault kv get secret/foo

