class SimpleMemory:
    def __init__(self):
        self.chat_history = []

    def load_memory(self):
        return self.chat_history

    def save(self, user_input, output):
        self.chat_history.append({"user": user_input, "assistant": output})


memory = SimpleMemory()


def get_memory():
    return memory
