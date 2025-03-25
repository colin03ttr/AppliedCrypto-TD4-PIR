from client import Client
from server import Server
import time

client = Client(bits=1024)
server = Server(db_size=100)

index_to_retrieve = 41
query = client.request(db_size=100, index=index_to_retrieve)

encrypted_answer = server.answer_request(query, client.pk)

decrypted_answer = client.decrypt_answer(encrypted_answer)

assert decrypted_answer == server.db[index_to_retrieve], "PIR protocol failed!"
print(f"Retrieved value: {decrypted_answer} (Correct: {server.db[index_to_retrieve]})")

def measure_performance(db_sizes):
    for size in db_sizes:
        server = Server(size)
        client = Client()

        # Measure server time
        start = time.time()
        query = client.request(size, index=size//2)  # Query middle element
        encrypted_answer = server.answer_request(query, client.pk)
        server_time = time.time() - start

        # Measure client time
        start = time.time()
        decrypted_answer = client.decrypt_answer(encrypted_answer)
        client_time = time.time() - start

        print(f"DB Size: {size} | Server Time: {server_time:.4f}s | Client Time: {client_time:.4f}s")

def measure_communication(db_sizes, bits=1024):
    for size in db_sizes:
        client = Client(bits)
        query = client.request(size, index=0)
        
        client_to_server_bits = size * 2 * bits
        server_to_client_bits = 2 * bits
        
        print(f"DB Size: {size} | Client→Server: {client_to_server_bits} bits | Server→Client: {server_to_client_bits} bits")