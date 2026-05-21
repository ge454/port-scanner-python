import socket
import sys

def verificar_porta(ip_alvo, porta_alvo):
    """
    Tenta estabelecer uma conexão TCP com o IP e porta especificados.
    Retorna True se a porta estiver aberta (sucesso na conexão) e False caso contrário.
    """
    try:
        # Cria o socket: AF_INET para IPv4 e SOCK_STREAM para protocolo TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Define o timeout de 2 segundos, essencial para não travar em portas filtradas
        s.settimeout(2)
        
        # connect_ex tenta conectar e retorna 0 se a conexão for bem-sucedida
        resultado = s.connect_ex((ip_alvo, porta_alvo))
        
        # Fecha o socket para liberar os recursos do sistema
        s.close()
        
        # Retorna True apenas se o resultado for 0 (porta aberta)
        if resultado == 0:
            return True
        else:
            return False
            
    except socket.error as erro:
        # Tratamento de erro caso ocorra alguma falha na rede ou no socket
        print(f"Erro de conexão: {erro}")
        return False

# Bloco principal de execução
if __name__ == "__main__":
    # Verifica se o usuário passou os argumentos corretamente (IP e Porta)
    if len(sys.argv) != 3:
        print("Uso correto: python port_scanner.py <IP_ALVO> <PORTA>")
        print("Exemplo: python port_scanner.py 192.168.1.1 80")
        sys.exit(1)

    # Captura os argumentos passados via linha de comando
    ip = sys.argv[1]
    
    # Converte a porta para número inteiro (int), pois vem como texto (string) do terminal
    try:
        porta = int(sys.argv[2])
    except ValueError:
        print("Erro: A porta deve ser um número inteiro.")
        sys.exit(1)

    print(f"Iniciando varredura no IP {ip} na porta {porta}...")

    # Chama a função de verificação
    if verificar_porta(ip, porta):
        print(f"[+] SUCESSO: A porta {porta} está ABERTA em {ip}")
    else:
        print(f"[-] A porta {porta} está FECHADA ou FILTRADA em {ip}")