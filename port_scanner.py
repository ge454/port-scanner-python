import tkinter as tk
from tkinter import ttk, messagebox
import socket
import concurrent.futures
from datetime import datetime
import threading
import sys
import subprocess

# --- INSTALADOR AUTOMÁTICO DO FPDF ---
try:
    from fpdf import FPDF
except ImportError:
    print("[!] Biblioteca 'fpdf' não encontrada. Instalando automaticamente...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf", "--user"])
        from fpdf import FPDF
        print("[+] Instalação concluída com sucesso! Abrindo o programa...\n")
    except Exception as e:
        print(f"Erro ao tentar instalar automaticamente: {e}")
        messagebox.showerror("Erro de Dependência", "Não foi possível instalar a biblioteca fpdf. Instale manualmente.")
        sys.exit(1)

# --- DICIONÁRIO E FUNÇÕES AUXILIARES ---
PORTAS_CONHECIDAS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
    53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS", 
    3306: "MySQL", 3389: "RDP"
}

def limpar_texto(texto):
    if not texto:
        return ""
    return str(texto).encode('latin-1', 'replace').decode('latin-1')

# --- CLASSE DO PDF ---
class RelatorioCorporativoPDF(FPDF):
    def __init__(self, ip_alvo, tempo_total, total_abertas, total_fechadas):
        super().__init__()
        self.ip_alvo = ip_alvo
        self.tempo_total = tempo_total
        self.total_abertas = total_abertas
        self.total_fechadas = total_fechadas

    def header(self):
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.8)
        self.line(15, 15, 195, 15)
        
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(60, 60, 60)
        self.ln(12)
        self.cell(0, 10, limpar_texto('RELATÓRIO DE PROGRESSO'), 0, 1, 'L')
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, limpar_texto('Enumeração de Rede & Segurança Cibernética | Faculdade SENAI'), 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.2)
        self.line(15, self.get_y(), 195, self.get_y())
        
        self.ln(2)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(100, 10, limpar_texto('SENAI Port Scanner - Sprint 3'), 0, 0, 'L')
        self.cell(0, 10, limpar_texto(f'Página {self.page_no()}'), 0, 0, 'R')

# --- LÓGICA DO SCANNER ---
def verificar_porta(ip_alvo, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        resultado = s.connect_ex((ip_alvo, porta))
        
        if resultado == 0:
            servico = PORTAS_CONHECIDAS.get(porta, "Desconhecido")
            banner = "Sem resposta de banner"
            try:
                s.send(b"Oi\r\n") 
                resposta = s.recv(1024).decode('utf-8', errors='ignore').strip()
                if resposta:
                    banner = resposta[:50].replace('\n', ' ').replace('\r', '') 
            except:
                pass
            s.close()
            return porta, True, servico, banner
            
        s.close()
        return porta, False, "", ""
    except:
        return porta, False, "", ""

# --- TRUQUE DO GRADIENTE NO TKINTER ---
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")

# --- INTERFACE GRÁFICA FLUIDA ---
class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SENAI Port Scanner v3.0")
        self.root.geometry("520x660")
        self.root.resizable(False, False)
        
        # Fundo Gradient (Azul Escuro para Preto Noturno)
        self.bg_frame = GradientFrame(self.root, color1="#0A192F", color2="#000000", bd=0, highlightthickness=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Cor para camuflar os backgrounds das labels com o topo do gradient
        top_blend_color = "#07111F" 

        # Cabeçalho / Título (Flutuando no Canvas)
        self.lbl_titulo = tk.Label(self.bg_frame, text="⚡ SENAI PORT SCANNER", font=("Segoe UI", 18, "bold"), bg=top_blend_color, fg="#00FFC4")
        self.lbl_titulo.pack(pady=(25, 2))
        
        self.lbl_subtitulo = tk.Label(self.bg_frame, text="Advanced Network Enumeration", font=("Segoe UI", 9, "italic"), bg=top_blend_color, fg="#527A9B")
        self.lbl_subtitulo.pack(pady=(0, 25))

        # Estilo dos Entradas de Texto (Minimalistas, sem bordas)
        entry_options = {"bg": "#112240", "fg": "#FFFFFF", "insertbackground": "#00FFC4", "bd": 0, "font": ("Consolas", 12), "justify": "center"}

        # IP Alvo
        tk.Label(self.bg_frame, text="ENDEREÇO IP DO ALVO", font=("Segoe UI", 9, "bold"), bg=top_blend_color, fg="#8892B0").pack()
        self.entry_ip = tk.Entry(self.bg_frame, width=25, **entry_options)
        self.entry_ip.pack(ipady=6, pady=(5, 15))
        self.entry_ip.insert(0, "192.168.0.15")

        # Container Fluido para as Portas
        frame_portas = tk.Frame(self.bg_frame, bg=top_blend_color)
        frame_portas.pack(pady=5)

        # Porta Início
        frame_inicio = tk.Frame(frame_portas, bg=top_blend_color)
        frame_inicio.pack(side="left", padx=10)
        tk.Label(frame_inicio, text="PORTA INÍCIO", font=("Segoe UI", 8, "bold"), bg=top_blend_color, fg="#8892B0").pack()
        self.entry_inicio = tk.Entry(frame_inicio, width=10, **entry_options)
        self.entry_inicio.pack(ipady=6, pady=5)
        self.entry_inicio.insert(0, "1")

        # Divisor Visual
        tk.Label(frame_portas, text="—", font=("Segoe UI", 12), bg=top_blend_color, fg="#8892B0").pack(side="left", padx=5)

        # Porta Fim
        frame_fim = tk.Frame(frame_portas, bg=top_blend_color)
        frame_fim.pack(side="left", padx=10)
        tk.Label(frame_fim, text="PORTA FIM", font=("Segoe UI", 8, "bold"), bg=top_blend_color, fg="#8892B0").pack()
        self.entry_fim = tk.Entry(frame_fim, width=10, **entry_options)
        self.entry_fim.pack(ipady=6, pady=5)
        self.entry_fim.insert(0, "65535")

        # Botão customizado (Estilo Moderno Cyber)
        self.btn_scan = tk.Button(
            self.bg_frame, text="INICIAR VARREDURA", font=("Segoe UI", 10, "bold"),
            bg="#007ACC", fg="#FFFFFF", activebackground="#005999", activeforeground="#FFFFFF",
            bd=0, relief="flat", cursor="hand2", command=self.iniciar_scan
        )
        self.btn_scan.pack(fill="x", padx=40, pady=25, ipady=10)

        # Terminal Log (Design Glassmorphism)
        self.text_log = tk.Text(
            self.bg_frame, height=12, width=50, state="disabled", 
            bg="#020813", fg="#00FFC4", insertbackground="#FFFFFF",
            bd=0, font=("Consolas", 9), padx=15, pady=15
        )
        self.text_log.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
    def log(self, mensagem):
        self.text_log.config(state="normal")
        self.text_log.insert(tk.END, mensagem + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state="disabled")

    def iniciar_scan(self):
        ip = self.entry_ip.get().strip()
        try:
            inicio = int(self.entry_inicio.get().strip())
            fim = int(self.entry_fim.get().strip())
        except ValueError:
            messagebox.showerror("Erro de Sintaxe", "As portas inseridas precisam ser números inteiros válidos.")
            return

        if inicio > fim:
            messagebox.showerror("Erro de Escopo", "A porta inicial não pode ser superior à porta final.")
            return

        self.text_log.config(state="normal")
        self.text_log.delete(1.0, tk.END)
        self.text_log.config(state="disabled")
        
        self.btn_scan.config(state="disabled", bg="#203A43", text="⏳ ANALISANDO A REDE...")
        
        self.log(f"[*] INICIANDO AUDITORIA DE CONEXÃO")
        self.log(f"[*] Alvo: {ip}")
        self.log(f"[*] Escopo: TCP/{inicio} até TCP/{fim}\n")

        threading.Thread(target=self.processar_scan, args=(ip, inicio, fim), daemon=True).start()

    def processar_scan(self, ip, inicio, fim):
        tempo_inicio = datetime.now()
        portas_encontradas = []
        fechadas = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=800) as executor:
            futuros = [executor.submit(verificar_porta, ip, p) for p in range(inicio, fim + 1)]
            
            for futuro in concurrent.futures.as_completed(futuros):
                porta, aberta, servico, banner = futuro.result()
                if aberta:
                    self.log(f"[+] PORTA {porta}/TCP ABERTA ({servico})")
                    portas_encontradas.append({'porta': porta, 'servico': servico, 'banner': banner})
                else:
                    fechadas += 1

        tempo_total = str(datetime.now() - tempo_inicio).split('.')[0]
        total_abertas = len(portas_encontradas)
        
        self.log(f"\n[=] VARREDURA FINALIZADA [=]")
        self.log(f"Tempo Decorrido: {tempo_total}")
        self.log(f"Portas Abertas: {total_abertas}")
        self.log(f"Portas Ignoradas: {fechadas}")

        self.root.after(0, self.finalizar_interface)

        if portas_encontradas:
            self.gerar_pdf(ip, inicio, fim, tempo_total, total_abertas, fechadas, portas_encontradas)
        else:
            messagebox.showinfo("Resultado", "Análise concluída. Nenhuma porta aberta respondendo no host alvo.")

    def finalizar_interface(self):
        self.btn_scan.config(state="normal", bg="#007ACC", text="INICIAR NOVA VARREDURA")

    def gerar_pdf(self, ip, inicio, fim, tempo_total, total_abertas, fechadas, portas_encontradas):
        nome_arquivo = f"Relatorio_Progresso_{ip.replace('.', '_')}.pdf"
        
        try:
            pdf = RelatorioCorporativoPDF(ip, tempo_total, total_abertas, fechadas)
            pdf.set_margins(15, 15, 15)
            pdf.add_page()
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(70, 70, 70)
            pdf.cell(0, 10, limpar_texto("01. Resumo Executivo"), 0, 1, 'L')
            
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(100, 100, 100)
            texto_intro = f"Escaneamento direcionado ao endereco IP {ip}, analisando o intervalo de {inicio} a {fim} via conexoes TCP nativas."
            pdf.multi_cell(0, 6, limpar_texto(texto_intro))
            pdf.ln(5)
            
            pdf.set_fill_color(245, 245, 245)
            pdf.rect(15, pdf.get_y(), 180, 24, 'F')
            
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(120, 120, 120)
            pdf.set_xy(20, pdf.get_y() + 3)
            pdf.cell(60, 5, limpar_texto("ALVO"), 0, 0, 'C')
            pdf.cell(60, 5, limpar_texto("PORTAS ABERTAS"), 0, 0, 'C')
            pdf.cell(60, 5, limpar_texto("TEMPO"), 0, 1, 'C')
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(60, 60, 60)
            pdf.set_x(20)
            pdf.cell(60, 8, limpar_texto(ip), 0, 0, 'C')
            pdf.cell(60, 8, limpar_texto(str(total_abertas)), 0, 0, 'C')
            pdf.cell(60, 8, limpar_texto(tempo_total), 0, 1, 'C')
            pdf.ln(10)
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(70, 70, 70)
            pdf.cell(0, 10, limpar_texto("02. Mapeamento de Portas e Servicos"), 0, 1, 'L')
            
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(80, 80, 80)
            
            pdf.cell(30, 8, limpar_texto("Porta"), 0, 0, 'L', True)
            pdf.cell(45, 8, limpar_texto("Servico"), 0, 0, 'L', True)
            pdf.cell(105, 8, limpar_texto("Banner Detectado"), 0, 1, 'L', True)
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(100, 100, 100)
            pdf.set_draw_color(200, 200, 200)
            pdf.set_line_width(0.3)
            
            portas_encontradas = sorted(portas_encontradas, key=lambda x: x['porta'])
            alternar = False
            for p in portas_encontradas:
                pdf.set_fill_color(250, 250, 250) if alternar else pdf.set_fill_color(255, 255, 255)
                pdf.cell(30, 8, limpar_texto(f"TCP {p['porta']}"), 'B', 0, 'L', True)
                pdf.cell(45, 8, limpar_texto(p['servico']), 'B', 0, 'L', True)
                pdf.cell(105, 8, limpar_texto(p['banner']), 'B', 1, 'L', True)
                alternar = not alternar

            pdf.output(nome_arquivo)
            messagebox.showinfo("Sucesso!", f"Auditoria concluída!\n\nO documento '{nome_arquivo}' foi gerado e salvo com sucesso no diretório do programa.")
                
        except Exception as e:
            messagebox.showerror("Erro no PDF", f"Falha crítica ao compilar o PDF.\nErro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()