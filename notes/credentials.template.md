# Credenciais e Chaves — Citrus Homelab

Copie este arquivo para `credentials.md` e preencha com seus valores.

## SSH
- **Chave privada**: `~/.ssh/citrus` (no PC)
- **Conexao**: `ssh -i ~/.ssh/citrus -p 8022 <usuario>@<tailscale-ip>`
- **Senha desativada**: PasswordAuthentication no

## HTTP Basic Auth (Nginx)
- **Usuario**: <defina>
- **Senha**: <defina>
- **Gerar htpasswd**: `openssl passwd -5 <senha>`
- **Arquivo htpasswd**: `~/www/.htpasswd` (no celular)

## FileBrowser
- **Usuario**: <defina>
- **Senha**: <defina>
- **Porta**: 127.0.0.1:8081

## Syncthing
- **Acesso GUI**: 127.0.0.1:8384
- **Tunel SSH**: `ssh -i ~/.ssh/citrus -p 8022 -L 8384:127.0.0.1:8384 <usuario>@<tailscale-ip>`

## Tailscale
- **IP**: <seu-ip-tailscale>
- **WiFi**: <seu-ip-wifi>