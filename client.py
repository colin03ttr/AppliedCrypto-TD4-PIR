from paillier import Paillier

class Client:
    def __init__(self, bits=1024):
        self.phe = Paillier(bits)
        self.pk = (self.phe.n, self.phe.g)

    def request(self, db_size, index):
        query = []
        for i in range(db_size):
            if i == index:
                query.append(self.phe.encrypt(1))
            else:
                query.append(self.phe.encrypt(0))
        return query

    def decrypt_answer(self, encrypted_answer):
        return self.phe.decrypt(encrypted_answer)