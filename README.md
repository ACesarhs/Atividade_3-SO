# 🐧 Atividade 3: Isolamento e Limitação de Recursos em Contêineres Linux

![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)
![Disciplina](https://img.shields.io/badge/Disciplina-Sistemas%20Operacionais-blue)
![Ambiente](https://img.shields.io/badge/Ambiente-Ubuntu%2024.04-orange)

Este repositório contém o laboratório prático desenvolvido para a **Atividade 3** da disciplina de Sistemas Operacionais (UFS - 2026.2). O objetivo principal foi observar empiricamente como os **Namespaces** alteram a visão de processos, mounts e rede, e como os **Cgroups v2** limitam recursos de hardware (CPU, RAM e PIDs) sem transformar um contêiner em uma Máquina Virtual independente.

---

## 📋 Sumário
1. [Ambiente e Infraestrutura](#-ambiente-e-infraestrutura)
2. [Evidências de Namespaces](#-evidências-de-namespaces)
3. [Experimento de Cgroups (CPU e Throttling)](#-experimento-de-cgroups-cpu-e-throttling)
4. [Segurança e Menor Privilégio](#-segurança-e-menor-privilégio)
5. [Estrutura do Repositório](#-estrutura-do-repositório)
6. [Como Reproduzir](#-como-reproduzir)

---

## 🖥️ Ambiente e Infraestrutura

O experimento foi conduzido em uma Máquina Virtual (VirtualBox) para isolar o ambiente de testes do hardware físico.

| Recurso | Especificação |
| :--- | :--- |
| **Sistema Operacional** | Ubuntu 24.04 LTS |
| **Kernel Linux** | Compartilhado entre Host e Contêineres |
| **Docker Engine** | v29.1.3 (Systemd Cgroup Driver) |
| **Cgroup** | v2 (Unificado) |
| **Imagem Base** | `python:3.12-slim` |
| **Digest da Imagem** | `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b` |

---

## 🏗️ Evidências de Namespaces (Parte B)

Para provar o isolamento de visão, subimos dois contêineres independentes (`ns-a` e `ns-b`). Os handles do Kernel foram extraídos via `/proc/1/ns/`.

| Recurso | Handle `ns-a` | Handle `ns-b` | Interpretação |
| :--- | :--- | :--- | :--- |
| **PID** | `pid:[4026532275]` | `pid:[4026532345]` | Árvores de processos isoladas. O PID 1 do contêiner é uma ilusão de visão. |
| **Mount** | `mnt:[4026532266]` | `mnt:[4026532342]` | Visões de sistema de arquivos independentes. |
| **Network** | `net:[4026532277]` | `net:[4026532347]` | Pilhas de rede isoladas (interfaces e rotas). |

*(Dados brutos disponíveis em `evidencias/namespaces.txt`)*

---

## ⚙️ Experimento de Cgroups (CPU e Throttling) (Parte C)

A carga de trabalho consistiu em um script Python determinístico (`carga_cpu.py`) executando 10.000.000 de iterações. Foram realizadas 3 repetições para cada condição:
*   **C1:** `--cpus=0.5`, `--memory=256m`, `--pids-limit=64`.
*   **C2:** `--cpus=1.0`, `--memory=256m`, `--pids-limit=64`.

### Resultados de Desempenho
*   **Tempo Médio C1:** ~32.6 segundos
*   **Tempo Médio C2:** ~20.2 segundos
> *Nota: O ganho não foi exatamente o dobro (2x) devido ao overhead de inicialização e ao ruído do host.*

### Prova do Throttling (Intervenção do Kernel)
A análise do arquivo `cpu.stat` durante a execução provou o estrangulamento (throttling) imposto pelo Completely Fair Scheduler (CFS):
*   **C1 (0.5 CPU):** `nr_throttled` = **69** | `throttled_usec` = **4.989.906**
*   **C2 (1.0 CPU):** `nr_throttled` = **24** | `throttled_usec` = **2.714.041**

*(Gráficos gerados: `grafico_tempo.png` e `grafico_throttling.png`)*

---

## 🔒 Segurança e Menor Privilégio (Parte D)

1.  **Mount Read-Only:** Um diretório sintético foi montado com a flag `:ro`. O contêiner rodou com usuário não-root (`1000:1000`), `--cap-drop=ALL` e `--security-opt no-new-privileges`. A leitura foi permitida, mas a tentativa de escrita retornou `Read-only file system`.
2.  **OOM Killer:** Em testes de estresse, ao tentar alocar mais de 256 MiB de RAM, o Kernel interveio ativamente (`Memory cgroup out of memory`) e matou o processo do contêiner, protegendo a integridade da VM host.

---

## 📂 Estrutura do Repositório

```text
atividade3/
├── README.md
├── ambiente.txt               # Saída do uname, docker info, etc.
├── carga_cpu.py               # Script de carga determinística
├── grafico_tempo.png          # Gráfico comparativo de tempo (C1 vs C2)
├── grafico_throttling.png     # Gráfico comparativo de throttling
├── resultados/
│   └── resultados.csv         # Dados brutos das 6 execuções
└── evidencias/
    ├── namespaces.txt         # Handles de PID, MNT e NET
    ├── throttling_final.txt   # Dados do cpu.stat
    ├── oom_killer.txt         # Log do OOM Killer
    └── readonly.txt           # Registro de negação de escrita
```
---

## 🚀 Como Reproduzir

---

### Baixe a imagem oficial do Python:
docker pull python:3.12-slim

---

### Execute os experimentos de carga (exemplo C1):
docker run --rm --cpus=0.5 --memory=256m --memory-swap=256m --pids-limit=64 -v "$HOME/carga_cpu.py:/carga_cpu.py:ro" python:3.12-slim python /carga_cpu.py 10000000

---

### Para verificar o Throttling, execute a carga em background e leia o cgroup:
docker run -d --name test_c1 --cpus=0.5 -v "$HOME/carga_cpu.py:/carga_cpu.py:ro" python:3.12-slim python /carga_cpu.py 10000000
docker exec test_c1 cat /sys/fs/cgroup/cpu.stat

---

## 📄 Entregáveis

*   **Relatório em PDF:** Disponível na pasta [`/relatorio`](./relatorio).
*   **Vídeo de Apresentação:** O link para o vídeo está disponível no arquivo [`/video/link_video.txt`](./video/link_video.txt). 
    *   *Link direto:* [Assistir no Google Drive](https://drive.google.com/drive/folders/1a3MHNHYxrozXPKFu2K0VzJWTPxJBUYuv?usp=sharing)
