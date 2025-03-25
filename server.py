import random

class Server:
    def __init__(self, db_size):
        self.db_size = db_size
        self.T = [random.randint(1, 2**16) for _ in range(db_size)]
    
    def answerRequest(self, request, pk): 
        v = request
        n, g = pk
        n_square = n ** 2
        t = 1
        for j, c in enumerate(v):
            t = (t * pow(c, self.T[j], n_square)) % n_square
        return t

if __name__ == "__main__":
    server = Server(10)
    print("Table T générée par le serveur :", server.T)