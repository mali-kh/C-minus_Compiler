import scanner


class Parser:
    scany = None

    def set_scanner(self, scanner_instance):
        self.scany = scanner_instance

    def run(self):
        while True:
            next_token = self.scany.get_next_token()
            if next_token is None:
                break
