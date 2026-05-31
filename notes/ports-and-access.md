# Mapa de Portas e Acesso — Citrus Homelab

## Portas

| Porta | Protocolo | Serviço | Bind | Acesso Externo |
|-------|-----------|---------|------|----------------|
| 8022 | TCP | SSH | 0.0.0.0 | Somente chave pública, sem senha |
| 8080 | TCP | Nginx dashboard | 0.0.0.0 | Auth básica obrigatória |
| 8081 | TCP | FileBrowser | 127.0.0.1 | Nenhum (proxy via nginx) |
| 8082 | TCP | Camera API | 127.0.0.1 | Nenhum (proxy via nginx) |
| 41737 | TCP | LensCast MJPEG | 0.0.0.0* | Proxy via nginx com auth |
| 8384 | TCP | Syncthing GUI | 127.0.0.1 | Nenhum (SSH tunnel) |

*Nota: LensCast é um app Android que binda em 0.0.0.0. Sem root, não é possível
bloquear acesso direto com iptables. A porta fica acessível na rede WiFi local.
A segurança é garantida pelo nginx com auth para acesso via dashboard.
A versão instalada é buildada localmente a partir do código-fonte auditado.

## Caminhos Nginx (tudo protegido com auth básica)

| Caminho | Proxy para | Auth |
|---------|-----------|------|
| / | Dashboard (arquivo local) | Sim |
| /cam/ | LensCast MJPEG (127.0.0.1:41737/mjpeg) | Sim |
| /lenscast/ | LensCast Web UI (127.0.0.1:41737/) | Sim |
| /files/ | FileBrowser (127.0.0.1:8081) | Sim |
| /api/camera?action=start/stop/toggle | LensCast HTTP API | Sim |
| /api/status | Verifica se câmera está online | Sim |

## Autenticação

| Serviço | Metodo | Detalhes |
|---------|--------|---------|
| Dashboard/Nginx | HTTP Basic Auth | usuario: admin (senha em credentials.md) |
| SSH | Chave publica ED25519 | ~/.ssh/citrus no PC |
| FileBrowser | Login proprio | usuario: admin (senha em credentials.md) |
| LensCast | HTTP Basic Auth (via nginx) | mesmo do dashboard |
| Camera API | HTTP Basic Auth (via nginx) | mesmo do dashboard |
| Syncthing | API/GUI token | acessivel somente em 127.0.0.1:8384 |

## Camera API (porta 8082)

endpoint: `/api/camera?action=start|stop|toggle`
- `start` — envia `{"streaming": true}` para LensCast `/api/control`
- `stop` — envia `{"streaming": false}` para LensCast `/api/control`
- `toggle` — envia `{"streaming": "toggle"}` para LensCast `/api/control`
- `/api/status` — verifica se a porta 41737 está aberta (camera online/offline)