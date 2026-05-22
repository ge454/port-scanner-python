# SENAI Port Scanner v3.0

Uma ferramenta que faz a varredura de portas desenvolvida em phyton. Esse projeto tem o objetivo de enumerar portas TCP, identificar serviços no alvo e capturar banners de conexão e no final em uma interface gráfica e ao final gerar um relatório em PDF.
## 🚀 Funcionalidades

* **Varredura Multithreading:** Utiliza de threads simultâneas para fazer um escaneamento mais rápido.
* **Interface Gráfica (GUI):** Uma interface voltada gráfica tematizada para "cyber-segurança".
* **Detecção de Serviços:** Identifica automaticamente os serviços das portas mapeadas.
* **Banner Grabbing:** Tenta capturar a resposta (banner) do serviço rodando na porta aberta.
* **Geração Automática de Relatórios:** Faz relatórios com os resultados do escaneamento em um documento PDF 
* **Auto-Instalação de Dependências:** O código verifica e instala a biblioteca para pfds no python ('fpdf') caso o usuário não tenha.
## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter:** Interface Gráfica e animações (Canvas Gradient).
* **Socket:** Conexões de rede e auditoria de portas TCP.
* **Concurrent.futures:** Processamento paralelo (Multithreading).
* **FPDF:** Geração de relatórios PDF.

## 💻 Como Utilizar

1. Faça o clone deste repositório:
   ```bash
   git clone [https://github.com/ge454/port-scanner-python] https://github.com/ge454/port-scanner-python
