# Citrus Homelab

POCO Citrus (Redmi 9) transformado em servidor homelab, acessível via Tailscale.

## Especificações

| Item | Valor |
|------|-------|
| Dispositivo | POCO Citrus (Redmi 9) |
| Android | 10 (MIUI, bootloader bloqueado, sem root) |
| Arquitetura | aarch64 (ARM64) |

## Portas e Serviços

| Porta | Serviço | Bind | Acesso |
|-------|---------|------|--------|
| 8022 | SSH | 0.0.0.0 | Somente chave ED25519 |
| 8080 | Nginx (dashboard + proxy) | 0.0.0.0 | Auth básica obrigatória |
| 8081 | FileBrowser | 127.0.0.1 | Proxy via nginx com auth |
| 8082 | Camera API | 127.0.0.1 | Proxy via nginx com auth |
| 41737 | LensCast (câmera MJPEG) | veja nota | Proxy via nginx com auth |
| 8384 | Syncthing GUI | 127.0.0.1 | SSH tunnel |

> **LensCast**: É um app Android que binda em `0.0.0.0`. Sem root, não é possível
> bloquear com iptables. A câmera fica acessível na rede WiFi local sem auth.
> Use a interface web do LensCast para ativar autenticação nativa se disponível.
> A versão instalada é buildada localmente a partir do código-fonte auditado.

## Segurança

- **Nginx auth básica** — protege dashboard, câmera, arquivos e LensCast
- **SSH sem senha** — somente autenticação por chave pública ED25519
- **FileBrowser bind 127.0.0.1** — inacessível diretamente
- **Syncthing bind 127.0.0.1** — acesso somente via SSH tunnel
- **Camera API bind 127.0.0.1** — controla LensCast via HTTP, proxy com auth
- **LensCast build local** — código-fonte auditado, sem telemetry/ads

## Aplicativos

| App | Função | Origem |
|-----|--------|--------|
| Termux | Terminal Linux | F-Droid |
| Termux:API | Acesso a hardware | F-Droid |
| Termux:Boot | Auto-início no boot | F-Droid |
| Tailscale | VPN mesh | APK direto |
| LensCast | Câmera IP MJPEG/RTSP | Build local (GitHub) |
| Syncthing | Sincronização de arquivos | F-Droid |
| FileBrowser | Gerenciador de arquivos web | GitHub releases |

## Estrutura de Arquivos no Celular

```
~/.termux/boot/start.sh           → Auto-início (chama start-all.sh)
~/start-all.sh                     → Inicia todos os serviços
~/www/index.html                   → Dashboard web
~/www/.htpasswd                    → Senhas do nginx
~/filebrowser                       → Binary do FileBrowser
~/filebrowser.db                    → Banco de dados do FileBrowser
~/camera-api.py                     → API de controle da câmera
$PREFIX/etc/nginx/nginx.conf        → Proxy reverso + auth
$PREFIX/etc/ssh/sshd_config         → SSH config (sem senha)
~/.ssh/authorized_keys              → Chaves públicas SSH
```

## Estrutura do Repositório

```
citrus-homelab/
├── README.md                        → Esta documentação
├── .gitignore                       → Ignora secrets
├── security/
│   ├── nginx.conf                   → Nginx com auth + proxy reverso
│   └── htpasswd                     → (gitignored) senhas criptografadas
├── apps/
│   ├── index.html                   → Dashboard com controle de câmera
│   ├── start-all.sh                 → Script de boot (5 serviços)
│   ├── boot-start.sh                → Script do Termux:Boot
│   └── camera-api.py                → API HTTP de controle da câmera
└── notes/
    ├── ports-and-access.md           → Mapa de portas e acesso
    ├── credentials.md                → (gitignored) credenciais reais
    └── credentials.template.md       → Template de credenciais
```