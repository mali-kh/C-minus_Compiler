import anytree


class Writer:
    def __init__(self, file_name):
        self.file = open(file_name, 'w', encoding="utf-8")

    def close(self):
        self.file.close()


class ErrorWriter(Writer):
    def __init__(self):
        super().__init__('lexical_errors.txt')
        self.error_exists = False
        self.lineno = 0

    def write_error(self, lineno, error_string):
        if self.lineno != lineno:
            if self.lineno != 0:
                self.file.write('\n')
            self.lineno = lineno
            self.file.write(str(self.lineno) + '.\t')
        self.error_exists = True
        self.file.write(error_string + ' ')

    def close(self):
        if not self.error_exists:
            self.file.write('There is no lexical error.')
        super().close()


class TokenWriter(Writer):
    def __init__(self):
        super().__init__('tokens.txt')
        self.lineno = 0

    def write_token(self, lineno, token_string):
        if self.lineno != lineno:
            if self.lineno != 0:
                self.file.write('\n')
            self.lineno = lineno
            self.file.write(str(self.lineno) + '.\t')
        self.file.write(token_string + ' ')


class SymbolWriter(Writer):
    def __init__(self):
        super().__init__('symbol_table.txt')

    def write_symbols(self, symbol_list):
        for index in range(len(symbol_list)):
            self.file.write(str(index + 1) + '.\t' + symbol_list[index] + '\n')


class SyntaxErrorWriter(Writer):
    def __init__(self):
        super().__init__('syntax_errors.txt')
        self.error_exists = False

    def write_syntax_error(self, lineno, error_string):
        self.error_exists = True
        self.file.write('#' + str(lineno) + ' : syntax error, ' + error_string + '\n')

    def close(self):
        if not self.error_exists:
            self.file.write('There is no syntax error.')
        super().close()


class ParseTreeWriter(Writer):
    def __init__(self):
        super().__init__('parse_tree.txt')

    def write_parse_tree(self, parse_tree):
        stringy = ''
        for pre, fill, node in anytree.RenderTree(parse_tree):
            stringy += (str("%s%s" % (pre, node.name)) + '\n')
        self.file.write(stringy)


class IntermediateCodeWriter:
    def __init__(self):
        self.lineno = 0
        pass

    def write_code(self, code):
        pass
