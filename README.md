# Atividade 3 - SO 2026.2

## Integrantes
- Augusto Cesar (ACesarhs)

## Ambiente e Infraestrutura
- **Ambiente:** Máquina Virtual (VirtualBox) rodando Ubuntu 24.04 LTS.
- **Kernel Linux:** Compartilhado entre VM e contêineres.
- **Docker:** Versão 29.1.3
- **Cgroup:** v2
- **Imagem Utilizada:** `python:3.12-slim`
- **Digest:** `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`

## Metodologia e Resultados
- **Namespaces:** Coleta de handles de PID, MNT e NET em dois contêineres.
- **Carga de Trabalho:** Script Python com 10.000.000 de iterações (checksum validado).
- **C1 (0.5 CPU):** Tempo médio ~32.6s. `nr_throttled` = 69 (Kernel interveio 69 vezes).
- **C2 (1.0 CPU):** Tempo médio ~20.2s. `nr_throttled` = 24.
- **Segurança:** Teste de mount Read-Only (negação de escrita com erro `Read-only file system`) e Teste de OOM Killer (Kernel matou processo que tentou exceder 256 MiB).

## Estrutura de Arquivos
- `grafico_tempo.png`: Comparação do tempo médio de execução (C1 vs C2).
- `grafico_throttling.png`: Prova visual do estrangulamento do Kernel.
- `evidencias/namespaces.txt`: Handles dos namespaces.
- `evidencias/throttling_final.txt`: Contadores do `cpu.stat`.
- `evidencias/oom_killer.txt`: Log da intervenção do Kernel (OOM).
- `evidencias/readonly.txt`: Registro do teste de negação de escrita.
