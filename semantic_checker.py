import FileManager.file_writer as fw


class SemanticChecker:
    def __init__(self):
        self.codegen = None
        self.error_list = []
        self.writer = fw.SemanticErrorWriter()

        self.declaration_name = ''
        self.arg_count = []
        self.repeat_count = 0

    def set_codegen(self, codegen):
        self.codegen = codegen

    def check(self, action_symbol, token, lineno):
        # for err in self.error_list:
        #     print(err)
        # print('100101010101001001010101')
        action_symbol = action_symbol[1:]
        if action_symbol == 'pid':
            for symbol in reversed(self.codegen.masmal_symbol_table):
                if symbol.lexeme == token:
                    break
            else:
                self.error_list.append(f'#{lineno} : Semantic Error! \'{token}\' is not defined.')
        elif action_symbol == 'relnum_op':
            if self.codegen.id_pvfs[-2] == 'arr' or self.codegen.id_pvfs[-1] == 'arr':
                self.error_list.append(f'#{lineno} : Semantic Error! Type mismatch in operands, Got array instead of int.')
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
            min_len = min(len(self.codegen.ready_function_param_list[-1]), self.arg_count[-1])
            for i in range(min_len):
                param_type = self.codegen.ready_function_param_list[-1][i].pvf
                arg_type = self.codegen.id_pvfs[i - self.arg_count[-1]]
                if param_type == 'pointer' and arg_type != 'arr':
                    self.error_list.append(
                        f'#{lineno} : Semantic Error! Mismatch in type of argument {i + 1} of \'{self.codegen.ready_function_lexeme_for_checker[-1]}\'. Expected \'array\' but got \'int\' instead.')
                if param_type == 'var' and arg_type != 'num':
                    self.error_list.append(
                        f'#{lineno} : Semantic Error! Mismatch in type of argument {i + 1} of \'{self.codegen.ready_function_lexeme_for_checker[-1]}\'. Expected \'int\' but got \'array\' instead.')
            if len(self.codegen.ready_function_param_list[-1]) != self.arg_count[-1]:
                self.error_list.append(f'#{lineno} : Semantic Error! Mismatch in numbers of arguments of \'{self.codegen.ready_function_lexeme_for_checker[-1]}\'.')
            self.arg_count.pop()
        elif action_symbol == 'repeat_count_plus':
            self.repeat_count += 1
        elif action_symbol == 'repeat_count_minus':
            self.repeat_count -= 1
        elif action_symbol == 'break_jump':
            if self.repeat_count == 0:
                self.error_list.append(f'#{lineno} : Semantic Error! No \'repeat ... until\' found for \'break\'.')

    def write_errors(self):
        if len(self.error_list) == 0:
            self.writer.write_errors('The input program is semantically correct')
        else:
            error_string = ''
            for err in self.error_list:
                error_string += err + '\n'
            self.writer.write_errors(error_string)
        self.writer.close()
