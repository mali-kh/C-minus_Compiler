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
        self.next_empty_temp_address = 1000
        self.next_empty_var_address = 500
        self.scope_stack = []

    def get_temp(self):
        address = self.next_empty_temp_address
        self.next_empty_temp_address += 4
        return address

    def get_var(self, length):
        address = self.next_empty_var_address
        self.next_empty_var_address += length * 4
        return address

    def find_addr(self, lexeme):
        pass

    def generate_code(self, action_symbol, token):
        action_symbol = action_symbol[1:]
        if action_symbol == 'pid':
            self.semantic_stack.append(token)
        elif action_symbol == 'ptype':
            self.semantic_stack.append(token)
        elif action_symbol == 'pnum':
            self.semantic_stack.append(token)
        elif action_symbol == 'label':
            self.semantic_stack.append(len(self.program_block))
        elif action_symbol == 'declare_func':
            entry = SymbolTableEntry(self.semantic_stack[-2], 'func', self.semantic_stack[-1], 0, self.semantic_stack[-3], len(self.scope_stack))
        elif action_symbol == 'declare_var':
            address = self.get_var(1)
            entry = SymbolTableEntry(self.semantic_stack[-1], 'var', address, 0, self.semantic_stack[-2], len(self.scope_stack))
        elif action_symbol == 'declare_array':
            address = self.get_var(self.semantic_stack[-1])
            entry = SymbolTableEntry(self.semantic_stack[-2], 'array', address, self.semantic_stack[-1], self.semantic_stack[-3], len(self.scope_stack))
        elif action_symbol == 'declare_pointer':
            pass
        elif action_symbol == 'increase_scope':
            pass
        elif action_symbol == 'decrease_scope':
            pass

