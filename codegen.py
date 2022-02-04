import FileManager.file_writer as fw


class SymbolTableEntry:
    def __init__(self, lexeme, pvf, address, size, typie, scope):
        self.lexeme = lexeme
        self.address = address
        self.pvf = pvf
        self.size = size
        self.typie = typie
        self.scope = scope


class TempSymbolTableEntry:
    def __init__(self, address, scope):
        self.address = address
        self.scope = scope


class Param:
    def __init__(self, typie, address, pvf):
        self.address = address
        self.pvf = pvf
        self.typie = typie


class SymbolTableFunction(SymbolTableEntry):
    def __init__(self, lexeme, pvf, address, size, typie, scope):
        super().__init__(lexeme, pvf, address, size, typie, scope)
        self.param_list = []


class Codegen:
    def __init__(self):
        self.code_writer = fw.IntermediateCodeWriter()
        self.semantic_stack = []
        self.masmal_symbol_table = []
        self.program_block = []
        self.next_empty_temp_address = 2000
        self.CALL_STACK_JUMP_TEMP = 996  # Put jump address in here before return jump
        self.CALL_STACK_HEAD = 1000  # This is a pointer to call stack head
        self.PRINT_PARAMETER = 500
        self.next_empty_var_address = 504
        self.RETURN_VALUE_ADDRESS = 2500
        self.scope_stack = []
        self.temp_scope_stack = []
        self.break_back_patch_list = []
        self.ready_function_param_list = []
        self.ready_function_address = 0
        self.temp_symbol_table = []
        self.compile_time_address_call_stack = []
        self.compile_time_address_call_stack_counter = []

        self.program_block.append(f'(ASSIGN, #1004, {self.CALL_STACK_HEAD}, )')

        self.program_block.append('')  # Jump to main

        output_func_symbol = SymbolTableFunction('output', 'func', 2, 0, 'void', 0)
        output_func_symbol.param_list.append(Param('int', 500, 'var'))
        self.masmal_symbol_table.append(output_func_symbol)

        self.program_block.append(f'(PRINT, {self.PRINT_PARAMETER}, , )')
        self.program_block.append(f'(ASSIGN, #0, {self.RETURN_VALUE_ADDRESS}, )')  # Is this needed?
        self.program_block.append(f'(SUB, {self.CALL_STACK_HEAD}, #4, {self.CALL_STACK_HEAD})')
        self.program_block.append(f'(ASSIGN, @{self.CALL_STACK_HEAD}, {self.CALL_STACK_JUMP_TEMP}, )')
        self.program_block.append(f'(JP, @{self.CALL_STACK_JUMP_TEMP}, , )')

    def print_program(self):
        print(self.semantic_stack)
        for item in self.masmal_symbol_table:
            print(f'{item.lexeme}\t{item.address}')
        for i in range(len(self.program_block)):
            print(f'{i}\t{self.program_block[i]}')
        print("////////////////////////////////////")

    def get_temp(self):
        address = self.next_empty_temp_address
        self.next_empty_temp_address += 4
        return address

    def get_var(self, length):
        address = self.next_empty_var_address
        self.next_empty_var_address += length * 4
        return address

    def find_addr(self, lexeme):
        for symbol in reversed(self.masmal_symbol_table):
            if symbol.lexeme == lexeme:
                return symbol.address

    def semantic_multi_pop(self, pop_count):
        for i in range(pop_count):
            self.semantic_stack.pop()

    def generate_code(self, action_symbol, token):
        # print(f'{action_symbol} {token}\n///////////////')
        # self.print_program()
        action_symbol = action_symbol[1:]
        if action_symbol == 'declare_pid':  # Push ID itself
            self.semantic_stack.append(token)
        elif action_symbol == 'pid':  # Push address
            self.semantic_stack.append(self.find_addr(token))
        elif action_symbol == 'ptype_int':
            self.semantic_stack.append(token)
        elif action_symbol == 'ptype_void':
            self.semantic_stack.append(token)
        elif action_symbol == 'parr_size':
            self.semantic_stack.append(token)
        elif action_symbol == 'label':
            self.semantic_stack.append(len(self.program_block))
        elif action_symbol == 'declare_func':
            entry = SymbolTableFunction(self.semantic_stack[-2], 'func', self.semantic_stack[-1], 0, self.semantic_stack[-3], len(self.scope_stack))
            self.masmal_symbol_table.append(entry)
            if self.semantic_stack[-2] == 'main':
                self.program_block[1] = f'(JP, {len(self.program_block)}, , )'
            self.semantic_multi_pop(3)
        elif action_symbol == 'declare_var':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'var', address, 0, self.semantic_stack[-2], len(self.scope_stack))
            self.program_block.append(f'(ASSIGN, #0, {address}, )')
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(2)
        elif action_symbol == 'declare_array':
            address = self.get_var(int(self.semantic_stack[-1]))
            entry = SymbolTableEntry(self.semantic_stack[-2], 'array', address, int(self.semantic_stack[-1]), self.semantic_stack[-3], len(self.scope_stack))
            for i in range(int(self.semantic_stack[-1])):
                self.program_block.append(f'(ASSIGN, #0, {address + 4 * i}, )')
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(3)
        elif action_symbol == 'declare_var_param':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'var', address, 0, self.semantic_stack[-2], len(self.scope_stack))
            for symbol in reversed(self.masmal_symbol_table):
                if symbol.pvf == 'func':
                    symbol.param_list.append(Param(self.semantic_stack[-2], address, 'var'))
                    break
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(2)
        elif action_symbol == 'declare_pointer_param':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'pointer', address, 0, self.semantic_stack[-2], len(self.scope_stack))
            for symbol in reversed(self.masmal_symbol_table):
                if symbol.pvf == 'func':
                    symbol.param_list.append(Param(self.semantic_stack[-2], address, 'pointer'))
                    break
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(2)
        elif action_symbol == 'increase_scope':
            self.scope_stack.append(len(self.masmal_symbol_table))
            self.temp_scope_stack.append(len(self.temp_symbol_table))
        elif action_symbol == 'decrease_scope':
            self.masmal_symbol_table = self.masmal_symbol_table[:self.scope_stack.pop()]
            self.temp_symbol_table = self.masmal_symbol_table[:self.temp_scope_stack.pop()]
        elif action_symbol == 'pop':
            self.semantic_multi_pop(1)
        elif action_symbol == 'break_jump':
            self.break_back_patch_list.append(len(self.program_block))
            self.program_block.append('')
        elif action_symbol == 'save':
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append('empty')
        elif action_symbol == 'jpf':
            self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {len(self.program_block)}, )'
            self.semantic_multi_pop(2)
        elif action_symbol == 'jpf_with_else':
            self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {len(self.program_block)+1}, )'
            self.semantic_multi_pop(2)
        elif action_symbol == 'jp':
            self.program_block[self.semantic_stack[-1]] = f'(JP, {len(self.program_block)}, , )'
            self.semantic_multi_pop(1)
        elif action_symbol == 'until':
            self.program_block.append(f'(JPF, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_multi_pop(2)
            for break_back_patch in self.break_back_patch_list:
                self.program_block[break_back_patch] = f'(JP, {len(self.program_block)}, , )'
            self.break_back_patch_list = []
        elif action_symbol == 'return_empty':
            self.program_block.append(f'(ASSIGN, #0, {self.RETURN_VALUE_ADDRESS}, )')  # Is this needed?
            self.program_block.append(f'(SUB, {self.CALL_STACK_HEAD}, #4, {self.CALL_STACK_HEAD})')
            self.program_block.append(f'(ASSIGN, @{self.CALL_STACK_HEAD}, {self.CALL_STACK_JUMP_TEMP}, )')
            self.program_block.append(f'(JP, @{self.CALL_STACK_JUMP_TEMP}, , )')
        elif action_symbol == 'return_from_stack':
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.RETURN_VALUE_ADDRESS}, )')
            self.program_block.append(f'(SUB, {self.CALL_STACK_HEAD}, #4, {self.CALL_STACK_HEAD})')
            self.program_block.append(f'(ASSIGN, @{self.CALL_STACK_HEAD}, {self.CALL_STACK_JUMP_TEMP}, )')
            self.program_block.append(f'(JP, @{self.CALL_STACK_JUMP_TEMP}, , )')
            self.semantic_multi_pop(1)
        elif action_symbol == 'implicit_return':
            self.program_block.append(f'(ASSIGN, #0, {self.RETURN_VALUE_ADDRESS}, )')  # Is this needed?
            self.program_block.append(f'(SUB, {self.CALL_STACK_HEAD}, #4, {self.CALL_STACK_HEAD})')
            self.program_block.append(f'(ASSIGN, @{self.CALL_STACK_HEAD}, {self.CALL_STACK_JUMP_TEMP}, )')
            self.program_block.append(f'(JP, @{self.CALL_STACK_JUMP_TEMP}, , )')
        elif action_symbol == 'assign':
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_multi_pop(1)  # We pop only one and leave the other one for later use
        elif action_symbol == 'get_array_element':
            very_new_address = ''
            the_pvf = ''
            for symbol in reversed(self.masmal_symbol_table):
                if symbol.address == self.semantic_stack[-2]:
                    the_pvf = symbol.pvf
                    break
            if str(self.semantic_stack[-1])[0] == '#':
                if the_pvf == 'pointer':
                    very_new_address = self.get_temp()
                    self.program_block.append(f'(ADD, {int(self.semantic_stack[-1][1:])*4}, {self.semantic_stack[-2]}, {very_new_address})')
                else:
                    very_new_address = self.semantic_stack[-2] + int(self.semantic_stack[-1][1:]) * 4
            else:
                very_new_address = self.get_temp()
                self.program_block.append(f'(MULT, {self.semantic_stack[-1]}, #4, {very_new_address})')
                if the_pvf == 'pointer':
                    self.program_block.append(f'(ADD, {very_new_address}, {self.semantic_stack[-2]}, {very_new_address})')
                else:
                    self.program_block.append(f'(ADD, {very_new_address}, #{self.semantic_stack[-2]}, {very_new_address})')
                very_new_address = '@' + str(very_new_address)
            self.semantic_multi_pop(2)
            self.semantic_stack.append(very_new_address)
        elif action_symbol == 'calculate_relation':
            operator = ''
            if self.semantic_stack[-2] == '<':
                operator = 'LT'
            elif self.semantic_stack[-2] == '==':
                operator = 'EQ'
            new_temp_address = self.get_temp()
            entry = TempSymbolTableEntry(new_temp_address, len(self.scope_stack))
            self.temp_symbol_table.append(entry)
            self.program_block.append(f'({operator}, {self.semantic_stack[-3]}, {self.semantic_stack[-1]}, {new_temp_address})')
            self.semantic_multi_pop(3)
            self.semantic_stack.append(new_temp_address)
        elif action_symbol == 'psmaller_than':
            self.semantic_stack.append(token)
        elif action_symbol == 'pequals':
            self.semantic_stack.append(token)
        elif action_symbol == 'pplus':
            self.semantic_stack.append(token)
        elif action_symbol == 'pminus':
            self.semantic_stack.append(token)
        elif action_symbol == 'calculate_addition':
            operator = ''
            if self.semantic_stack[-2] == '-':
                operator = 'SUB'
            elif self.semantic_stack[-2] == '+':
                operator = 'ADD'
            new_temp_address = self.get_temp()
            entry = TempSymbolTableEntry(new_temp_address, len(self.scope_stack))
            self.temp_symbol_table.append(entry)
            self.program_block.append(f'({operator}, {self.semantic_stack[-3]}, {self.semantic_stack[-1]}, {new_temp_address})')
            self.semantic_multi_pop(3)
            self.semantic_stack.append(new_temp_address)
        elif action_symbol == 'calculate_multiplication':
            new_temp_address = self.get_temp()
            entry = TempSymbolTableEntry(new_temp_address, len(self.scope_stack))
            self.temp_symbol_table.append(entry)
            self.program_block.append(f'(MULT, {self.semantic_stack[-2]}, {self.semantic_stack[-1]}, {new_temp_address})')
            self.semantic_multi_pop(2)
            self.semantic_stack.append(new_temp_address)
        elif action_symbol == 'pnum':
            self.semantic_stack.append('#' + token)
        elif action_symbol == 'function_call':
            self.compile_time_address_call_stack_counter.append(0)
            for symbol in reversed(self.masmal_symbol_table):
                if symbol.scope < len(self.scope_stack):
                    break
                self.program_block.append(f'(ASSIGN, {symbol.address}, @{self.CALL_STACK_HEAD}, )')
                self.program_block.append(f'(ADD, #4, {self.CALL_STACK_HEAD}, {self.CALL_STACK_HEAD})')
                self.compile_time_address_call_stack.append(symbol.address)
                self.compile_time_address_call_stack_counter[-1] += 1
                if symbol.pvf == 'array':
                    for i in range(1, symbol.size):
                        self.program_block.append(f'(ASSIGN, {symbol.address + 4 * i}, @{self.CALL_STACK_HEAD}, )')
                        self.program_block.append(f'(ADD, #4, {self.CALL_STACK_HEAD}, {self.CALL_STACK_HEAD})')
                        self.compile_time_address_call_stack.append(symbol.address + 4 * i)
                        self.compile_time_address_call_stack_counter[-1] += 1
            for symbol in reversed(self.temp_symbol_table):
                if symbol.scope < len(self.scope_stack):
                    break
                self.program_block.append(f'(ASSIGN, {symbol.address}, @{self.CALL_STACK_HEAD}, )')
                self.program_block.append(f'(ADD, #4, {self.CALL_STACK_HEAD}, {self.CALL_STACK_HEAD})')
                self.compile_time_address_call_stack.append(symbol.address)
                self.compile_time_address_call_stack_counter[-1] += 1
            # Put Arguments
            for paramie in reversed(self.ready_function_param_list):
                if paramie.pvf == 'pointer':
                    self.program_block.append(f'(ASSIGN, #{self.semantic_stack.pop()}, {paramie.address}, )')
                else:
                    self.program_block.append(f'(ASSIGN, {self.semantic_stack.pop()}, {paramie.address}, )')
            self.semantic_stack.pop()  # Accidentally didn't use the function name so I'll just pop it and never think about it again
            # Jump to function body
            self.program_block.append(f'(ASSIGN, #{len(self.program_block)+3}, @{self.CALL_STACK_HEAD}, )')
            self.program_block.append(f'(ADD, #4, {self.CALL_STACK_HEAD}, {self.CALL_STACK_HEAD})')
            self.program_block.append(f'(JP, {self.ready_function_address}, , )')
            for i in range(self.compile_time_address_call_stack_counter[-1]):
                address = self.compile_time_address_call_stack.pop()
                self.program_block.append(f'(SUB, {self.CALL_STACK_HEAD}, #4, {self.CALL_STACK_HEAD})')
                self.program_block.append(f'(ASSIGN, @{self.CALL_STACK_HEAD}, {address}, )')
            self.compile_time_address_call_stack_counter.pop()
            new_temp_address = self.get_temp()
            self.program_block.append(f'(ASSIGN, {self.RETURN_VALUE_ADDRESS}, {new_temp_address}, )')
            self.semantic_stack.append(new_temp_address)
        elif action_symbol == 'get_function_ready':
            self.ready_function_address = self.semantic_stack[-1]
            for symbol in self.masmal_symbol_table:
                if symbol.pvf == 'func' and symbol.address == self.semantic_stack[-1]:
                    self.ready_function_param_list = symbol.param_list
                    # for i in range(len(symbol.param_list)):
                    #     print(f'{symbol.param_list[i].address} from {symbol.lexeme} in {symbol.address} or {self.semantic_stack[-1]}')
                    break

    def write_generated_code(self):
        code_string = ''
        for i in range(len(self.program_block)):
            code_string += f'{i}\t{self.program_block[i]}\n'
        self.code_writer.write_code(code_string)
        self.code_writer.close()

    def pop_three_useless_codes(self):
        self.program_block.pop()
        self.program_block.pop()
        self.program_block.pop()
        self.program_block.pop()
