class SemanticChecker:
    def __init__(self):
        self.codegen = None
        self.error_list = []

        self.declaration_name = ''
        self.arg_count = []
        self.repeat_count = 0

    def set_codegen(self, codegen):
        self.codegen = codegen

    def check(self, action_symbol, token, lineno):
        action_symbol = action_symbol[1:]
        if action_symbol == 'pid':
            for symbol in reversed(self.codegen.masmal_symbol_table):
                if symbol.lexeme == token:
                    break
            else:
                self.error_list.append(f'#{lineno} : Semantic Error! \'{token}\' is not defined.')
        elif action_symbol == 'declare_pid':
            self.declaration_name = token
        elif action_symbol == 'declare_var':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{self.declaration_name}\'.')
        elif action_symbol == 'declare_array':
            if self.codegen.semantic_stack[-3] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{self.declaration_name}\'.')
        elif action_symbol == 'declare_var_param':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{self.declaration_name}\'.')
        elif action_symbol == 'declare_pointer_param':
            if self.codegen.semantic_stack[-2] == 'void':
                self.error_list.append(f'#{lineno} : Semantic Error! Illegal type of void for \'{self.declaration_name}\'.')
        elif action_symbol == 'arg_count_plus':
            self.arg_count[-1] += 1
        elif action_symbol == 'get_function_ready':
            self.arg_count.append(0)
        elif action_symbol == 'function_call':
            if self.arg_count[-1] != len(self.codegen.ready_function_param_list[-1]):
                self.error_list.append(f'#{lineno} : Semantic Error! Mismatch in numbers of arguments of \'{self.codegen.ready_function_lexeme_for_checker[-1]}\'.')
            self.arg_count.pop()
        elif action_symbol == 'repeat_count_plus':
            self.repeat_count += 1
        elif action_symbol == 'repeat_count_minus':
            self.repeat_count -= 1
        elif action_symbol == 'break_jump':
            if self.repeat_count == 0:
                self.error_list.append(f'#{lineno} : Semantic Error!  No \'repeat ... until\' found for \'break\'.')



    def write_errors(self):
        pass # FIXME
