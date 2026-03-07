class MemoryManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def store(self, state):
        # save query, hypothesis, scores

    def retrieve_similar(self, query):
        # return past similar cases