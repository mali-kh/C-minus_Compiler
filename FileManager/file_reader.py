class Reader:
    def __init__(self):
        self.file = open('input.txt', 'r')
        self.current_index = -1

    def read_next_char(self):
        char = self.file.read(1)
        self.current_index += 1
        return char

    def close_file(self):
        self.file.close()
