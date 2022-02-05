class SemanticChecker:
    def __init__(self):
        self.codegen = None
        self.error_list = []

    def set_codegen(self, codegen):
        self.codegen = codegen

    def check(self, action_symbol, token, lineno):
        action_symbol = action_symbol[1:]
        if action_symbol == 'pid':
            for symbol in reversed(self.codegen.masmal_symbol_table):
                if symbol.lexeme == token:
                    break
            else:
                self.error_list.append(f'#{lineno} : Semantic Error! \'{token}\' is not defined')
