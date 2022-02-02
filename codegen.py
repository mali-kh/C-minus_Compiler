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
            entry = SymbolTableEntry(self.semantic_stack[-1], 'func', )
        elif action_symbol == 'declare_var':
            entry = SymbolTableEntry(self.semantic_stack[-1], 'var', )
        elif action_symbol == 'declare_array':
            entry = SymbolTableEntry(self.semantic_stack[-1], 'array', )

