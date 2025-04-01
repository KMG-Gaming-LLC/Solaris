import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('67.220.85.146', 6459))  # Change 'localhost' to your server's IP if needed

try:
    while True:
        message = input("Send a message to the server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client.send(message.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        print(f"Server response: {response}")
finally:
    client.close()