# Atividade 3 - SO 2026.2

## Integrantes
- Augusto Cesar

## Ambiente e Infraestrutura
- **Ambiente:** Máquina Virtual rodando Ubuntu 24.04 LTS.
- **Kernel:** Linux (x86_64)
- **Docker:** Versão 29.1.3
- **Cgroup:** v2
- **Imagem Utilizada:** `python:3.12-slim`
- **Digest:** `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`

## Como Reproduzir
1. Baixar a imagem: `docker pull python:3.12-slim`
2. Executar os experimentos.
3. Os resultados brutos estarão em `resultados/resultados.csv`.

## Estrutura de Arquivos
- `grafico_tempo.png`: Comparação do tempo médio de execução (C1 vs C2).
- `grafico_throttling.png`: Prova visual do estrangulamento do Kernel (nr_throttled).
- `evidencias/namespaces.txt`: Handles dos namespaces PID, MNT e NET.
