import os
import platform
import subprocess
import time
from datetime import datetime

# Lista de hosts para monitorar (Rede local, Gateways, DNS públicos)
HOSTS_PARA_MONITORAR = [
    {"nome": "DNS Google", "host": "8.8.8.8"},
    {"nome": "DNS Cloudflare", "host": "1.1.1.1"},
    {"nome": "Gateway Local (Exemplo)", "host": "127.0.0.1"}
]

def ping_host(host):
    """
    Executa o comando de ping no sistema operacional (Windows/Linux)
    e retorna o status e a latência aproximada.
    """
    parametro = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", parametro, "1", host]
    
    inicio = time.time()
    processo = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fim = time.time()
    
    latencia_ms = round((fim - inicio) * 1000, 2)
    
    if processo.returncode == 0:
        return "ONLINE", latencia_ms
    else:
        return "OFFLINE", 0.0

def executar_monitoramento():
    print("=" * 50)
    print(f"📡 NETWORK MONITOR - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
    
    with open("log_rede.txt", "a", encoding="utf-8") as log_file:
        for item in HOSTS_PARA_MONITORAR:
            status, latencia = ping_host(item["host"])
            mensagem = f"[{datetime.now().strftime('%H:%M:%S')}] {item['nome']} ({item['host']}): {status} | Latência: {latencia}ms"
            
            print(mensagem)
            log_file.write(mensagem + "\n")
            
    print("-" * 50)

if __name__ == "__main__":
    try:
        while True:
            executar_monitoramento()
            time.sleep(1)  # <--- ALTERE AQUI
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoramento encerrado pelo usuário.")