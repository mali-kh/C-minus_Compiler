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
        elif action_symbol == 'declare_var':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{token}\'')
        elif action_symbol == 'declare_array':
            if self.codegen.semantic_stack[-3] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{token}\'')
        elif action_symbol == 'declare_var_param':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{token}\'')
        elif action_symbol == 'declare_pointer_param':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{token}\'')

    def write_errors(self):
        pass # FIXME
