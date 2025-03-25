import random

class Server:
    def __init__(self, db_size):
        self.db = [random.randint(1, 2**16) for _ in range(db_size)]  # random entries

    def answer_request(self, query, pk):
        # homomorphic dot product of the query and database
        n, g = pk
        encrypted_answer = 1
        for c_i, db_item in zip(query, self.db):
            encrypted_answer *= pow(c_i, db_item, n**2)
            encrypted_answer %= n**2
        return encrypted_answer