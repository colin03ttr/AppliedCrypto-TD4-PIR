from client import Client
from server import Server
import time
import matplotlib.pyplot as plt
import sys

# For measuring communication size
def bit_size(x):
    return x.bit_length()

db_sizes = list(range(10, 101, 10))
client_times = []
server_times = []
client_to_server_comm = []
server_to_client_comm = []

for db_size in db_sizes:
    client = Client(bits=1024)
    server = Server(db_size=db_size)

    # Time client request generation
    start = time.time()
    query = client.request(db_size=db_size, index=db_size // 2)
    client_time = time.time() - start
    client_times.append(client_time)

    # Communication size: client sends db_size ciphertexts
    # Each ciphertext ~ n^2, so we estimate bit size from one of them
    ct_size = bit_size(query[0])
    client_to_server_comm.append(ct_size * db_size)

    # Time server computation
    start = time.time()
    answer = server.answerRequest(query, client.pk)
    server_time = time.time() - start
    server_times.append(server_time)

    # Communication size: server sends one ciphertext
    server_to_client_comm.append(bit_size(answer))

# Plot execution time
plt.figure()
plt.plot(db_sizes, client_times, label='Client Time')
plt.plot(db_sizes, server_times, label='Server Time')
plt.xlabel('Database Size')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time vs. Database Size')
plt.legend()
plt.grid(True)
plt.savefig("execution_time_vs_db_size.png")
plt.show()

# Plot communication size
plt.figure()
plt.plot(db_sizes, client_to_server_comm, label='Client to Server')
plt.plot(db_sizes, server_to_client_comm, label='Server to Client')
plt.xlabel('Database Size')
plt.ylabel('Communication Size (bits)')
plt.title('Communication Size vs. Database Size')
plt.legend()
plt.grid(True)
plt.savefig("communication_size_vs_db_size.png")
plt.show()
