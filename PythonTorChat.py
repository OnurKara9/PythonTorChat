import stem.process
import socket
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(9050),
    'ControlPort': str(9051)
  },
  init_msg_handler = print,
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 9051))
sock.connect(("3g2upl4pq6kufc4m.onion", 80))


def send_message(message):
  encrypted_message = cipher_suite.encrypt(message.encode())
  sock.send(encrypted_message)

def receive_message():
  encrypted_message = sock.recv(4096)
  decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
  return decrypted_message

while True:
  message = input("You: ")
  send_message(message)
  response = receive_message()
  print("Server: " + response)