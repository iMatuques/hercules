import asyncio
import websockets
import socket
import time

async def handle_websocket(websocket, path):
    # Recebe a primeira mensagem do cliente WebSocket
    data = await websocket.recv()
    options = data.split(",")
    print(options)
    if len(options) != 4:
        print("Mensagem inválida. Fechando conexão.")
        await websocket.close()
        return

    ip, port, protocol, message_type = options
    print(f"IP: {ip}, Porta: {port}, Protocolo: {protocol}, Tipo de Mensagem: {message_type}")

    # Função para criar uma conexão TCP
    def create_tcp_connection():
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((ip, int(port)))
        return tcp_client

    # Função para criar uma conexão UDP
    def create_udp_connection():
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.connect((ip, int(port)))
        return udp_client

    # Cria a conexão inicial com base no protocolo recebido
    if protocol == "tcp":
        client = create_tcp_connection()
        client.setblocking(False)  # Configura o socket como não bloqueante
    elif protocol == "udp":
        client = create_udp_connection()
        client.setblocking(False)
    else:
        print("Protocolo inválido. Fechando conexão.")
        await websocket.close()
        return

    await websocket.send("nhe")
    try:
        while True:
            # Recebe mensagem do cliente WebSocket
            message = await websocket.recv()
            print(f"Mensagem recebida do WebSocket: {message}")

            # Envia mensagem para o servidor TCP ou UDP
            try:
                if message_type == "hex":
                    message = bytes.fromhex(message)
                    #message = message.encode('utf-8')
                    print(message)
                else:
                    message.encode()
                client.sendall(message)
            except (ConnectionResetError, BrokenPipeError):
                print(f"Conexão {protocol.upper()} perdida. Tentando reconectar...")
                client.close()
                while True:
                    try:
                        if protocol == "tcp":
                            client = create_tcp_connection()
                            client.setblocking(False)  # Configura o socket como não bloqueante
                        elif protocol == "udp":
                            client = create_udp_connection()
                            client.setblocking(False)
                        print(f"Reconexão {protocol.upper()} bem-sucedida.")
                        break
                    except ConnectionRefusedError:
                        print(f"Tentativa de reconexão {protocol.upper()} falhou. Tentando novamente em 1 segundo...")
                        time.sleep(1)

            # Espera um curto período de tempo para a resposta do servidor TCP
            await asyncio.sleep(0.1)

            # Tenta receber a resposta do servidor TCP
            try:
                response = client.recv(1024)
                if message_type == "hex":
                    response = response.hex()
                print(f"Resposta do servidor {protocol.upper()}: {response}")
                await websocket.send(response.decode())
            except BlockingIOError:
                # Não há resposta disponível, continuar para a próxima iteração do loop
                pass
            except (ConnectionResetError, BrokenPipeError):
                print(f"Conexão {protocol.upper()} perdida. Tentando reconectar...")
                client.close()
                while True:
                    try:
                        if protocol == "tcp":
                            client = create_tcp_connection()
                            client.setblocking(False)  # Configura o socket como não bloqueante
                        elif protocol == "udp":
                            client = create_udp_connection()
                        print(f"Reconexão {protocol.upper()} bem-sucedida.")
                        break
                    except ConnectionRefusedError:
                        print(f"Tentativa de reconexão {protocol.upper()} falhou. Tentando novamente em 1 segundo...")
                        time.sleep(1)

    finally:
        client.close()


