import FileManager.file_writer as fw


class SymbolTableEntry:
    def __init__(self, lexeme, pvf, address, size, typie, scope):
        self.lexeme = lexeme
        self.address = address
        self.pvf = pvf
        self.size = size
        self.typie = typie
        self.scope = scope


class Codegen:
    def __init__(self):
        self.code_writer = fw.IntermediateCodeWriter()
        self.semantic_stack = []
        self.masmal_symbol_table = []
        self.program_block = []
        self.next_empty_temp_address = 1500
        self.call_stack_head = 1000
        self.next_empty_var_address = 500
        self.scope_stack = []
        self.break_back_patch_list = []

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
        if action_symbol == 'pid':
            self.semantic_stack.append(token)
        elif action_symbol == 'ptype_int':
            self.semantic_stack.append(token)
        elif action_symbol == 'ptype_void':
            self.semantic_stack.append(token)
        elif action_symbol == 'pnum':
            self.semantic_stack.append(token)
        elif action_symbol == 'label':
            self.semantic_stack.append(len(self.program_block))
        elif action_symbol == 'declare_func':
            entry = SymbolTableEntry(self.semantic_stack[-2], 'func', self.semantic_stack[-1], 0, self.semantic_stack[-3], len(self.scope_stack))
            self.masmal_symbol_table.append(entry)
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
        elif action_symbol == 'declare_pointer':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'pointer', address, 0, self.semantic_stack[-2], len(self.scope_stack))
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


