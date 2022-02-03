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
        self.next_empty_temp_address = 1500
        self.call_stack_head = 1000
        self.next_empty_var_address = 500
        self.RETURN_VALUE_ADDRESS = 2000
        self.scope_stack = []
        self.break_back_patch_list = []
        self.ready_function_param_list = []
        self.temp_symbol_table = []

        self.program_block.append('')  # Jump to main

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
            self.semantic_stack.append('#' + token)
        elif action_symbol == 'label':
            self.semantic_stack.append(len(self.program_block))
        elif action_symbol == 'declare_func':
            entry = SymbolTableFunction(self.semantic_stack[-2], 'func', self.semantic_stack[-1], 0, self.semantic_stack[-3], len(self.scope_stack))
            self.masmal_symbol_table.append(entry)
            if self.semantic_stack[-2] == 'main':
                self.program_block[0] = f'(JP, {len(self.program_block)}, , )'
            self.semantic_multi_pop(3)
        elif action_symbol == 'declare_var':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'var', address, 0, self.semantic_stack[-2], len(self.scope_stack))
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(2)
        elif action_symbol == 'declare_array':
            address = self.get_var(self.semantic_stack[-1])
            entry = SymbolTableEntry(self.semantic_stack[-2], 'array', address, self.semantic_stack[-1], self.semantic_stack[-3], len(self.scope_stack))
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
                if symbol.typie == 'func':
                    symbol.param_list.append(Param(self.semantic_stack[-2], address, 'pointer'))
                    break
            self.masmal_symbol_table.append(entry)
            self.semantic_multi_pop(2)
        elif action_symbol == 'increase_scope':
            self.scope_stack.append(len(self.masmal_symbol_table))
        elif action_symbol == 'decrease_scope':
            self.masmal_symbol_table = self.masmal_symbol_table[:self.scope_stack.pop()]
        elif action_symbol == 'pop':
            self.semantic_multi_pop(1)
        elif action_symbol == 'break_jump':
            self.break_back_patch_list.append(len(self.program_block))
            self.program_block.append([])
        elif action_symbol == 'save':
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append([])
        elif action_symbol == 'jpf':
            self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {len(self.program_block)}, )'
            self.semantic_multi_pop(2)
        elif action_symbol == 'jp':
            self.program_block[self.semantic_stack[-1]] = f'(JP, {len(self.program_block)}, , )'
            self.semantic_multi_pop(1)
        elif action_symbol == 'until':
            self.program_block.append(f'(JPF, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_multi_pop(2)
            for break_back_patch in self.break_back_patch_list:
                self.program_block[break_back_patch] = f'(JP, {len(self.program_block)}, , )'
        elif action_symbol == 'return_empty':
            self.program_block.append(f'(ASSIGN, 0, {self.RETURN_VALUE_ADDRESS}, )')  # Is this needed?
            self.semantic_stack.append(self.RETURN_VALUE_ADDRESS)
        elif action_symbol == 'return_from_stack':
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.RETURN_VALUE_ADDRESS}, )')
            self.semantic_multi_pop(1)
            self.semantic_stack.append(self.RETURN_VALUE_ADDRESS)
        elif action_symbol == 'assign':
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_multi_pop(1)  # We pop only one and leave the other one for later use
        elif action_symbol == 'get_array_element':
            new_address = self.semantic_stack[-2] + self.semantic_stack[-1] * 4
            self.semantic_multi_pop(2)
            self.semantic_stack.append(new_address)
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
            for symbol in reversed(self.masmal_symbol_table):
                if symbol.scope < len(self.scope_stack):
                    break
                self.program_block.append(f'(ASSIGN, {symbol.address}, {self.call_stack_head}, )')
                self.program_block.append(f'(ADD, #4, {self.call_stack_head}, {self.call_stack_head})')

            for symbol in reversed(self.temp_symbol_table):
                if symbol.scope < len(self.scope_stack):
                    break
                self.program_block.append(f'(ASSIGN, {symbol.address}, {self.call_stack_head}, )')
                self.program_block.append(f'(ADD, #4, {self.call_stack_head}, {self.call_stack_head})')
            new_temp_address = 0
            # Create jump for calling # TODO dodododododododododododododododododododododododododododododo
            self.semantic_multi_pop(2)
            self.semantic_stack.append(new_temp_address)
        elif action_symbol == 'get_function_ready':
            for symbol in self.masmal_symbol_table:
                if symbol.pvf == 'func' and symbol.lexeme == self.semantic_stack[-1]:
                    self.ready_function_param_list = symbol.param_list

