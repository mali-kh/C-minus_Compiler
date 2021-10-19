import FileManager.file_reader as fr
import FileManager.file_writer as fw
import re


class Scanner:
    state = ['start', 'num', 'word', 'equal', 'twoequal', 'symbol', 'slash', 'bcmt', 'bcmt*', 'lcmt', 'wspace', 'star']
    valid_tokens = '[a-zA-Z0-9;:,\[\]\(\)\{\}\+\-\*=< \n\r\t\v\f]'
    digit = '[0-9]'
    letter = '[a-zA-Z]'
    symbol = '[;:,\[\]\(\)\{\}\+\-<]'
    wspace = '[ \n\r\t\v\f]'

    keyword_reference_list = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']

    type_by_state_name = {'num': 'NUM', 'equal': 'SYMBOL', 'twoequal': 'SYMBOL', 'symbol': 'SYMBOL', 'bcmt*': 'COMMENT',
                          'lcmt': 'COMMENT', 'wspace': 'WHITESPACE', 'star': 'SYMBOL'}

    def __init__(self):
        self.token_found_return = False
        self.finished = False
        self.read_again = False
        self.skip_one_char = False
        self.go_to_next_line = False
        self.lineno = 1
        self.temporary_lineno = 1
        self.current_index = 0
        self.current_char = ''
        self.current_state = 'start'
        self.state_to_return = ''
        self.current_token_lexeme = ''
        self.reader = fr.Reader()
        self.error_writer = fw.ErrorWriter()
        self.symbol_writer = fw.SymbolWriter()
        self.id_list = []

    def update_start_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'num'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'symbol'
            self.current_token_lexeme += self.current_char
        elif re.search('=', self.current_char):
            self.current_state = 'equal'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.current_state = 'star'
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.current_state = 'slash'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'wspace'
            if self.current_char == '\n':
                self.lineno += 1
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_num_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'num'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid number)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_word_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'word'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_equal_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.current_state = 'twoequal'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_two_equal_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_symbol_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_slash_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search('=', self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        elif re.search('\*', self.current_char):
            self.current_state = 'bcmt'
            print('asb')
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.current_state = 'lcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_bcmt_with_char(self):
        self.current_token_lexeme += self.current_char
        if self.current_char == '\n':
            self.lineno += 1
        if re.search('\*', self.current_char):
            self.current_state = 'bcmt*'

    def update_bcmt_star_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.letter, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search(Scanner.symbol, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search('=', self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        elif re.search('\*', self.current_char):
            self.current_state = 'bcmt*'
            self.current_token_lexeme += self.current_char
        elif re.search('/', self.current_char):
            self.reset_state_return()
            self.skip_one_char = True
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'bcmt'
            self.current_token_lexeme += self.current_char

    def update_lcmt_with_char(self):
        if re.search('\n', self.current_char):
            self.reset_state_return()
        else:
            self.current_token_lexeme += self.current_char

    def update_white_space_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.wspace, self.current_char):
            self.current_state = 'wspace'
            if self.current_char == '\n':
                self.lineno += 1
            self.current_token_lexeme += self.current_char
        else:
            self.current_state = 'start'
            self.error_writer.write_error(self.lineno, '(' + self.current_char + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_star_with_char(self):
        if re.search(Scanner.digit, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.letter, self.current_char):
            self.reset_state_return()
        elif re.search(Scanner.symbol, self.current_char):
            self.reset_state_return()
        elif re.search('=', self.current_char):
            self.reset_state_return()
        elif re.search('\*', self.current_char):
            self.reset_state_return()
        elif re.search('/', self.current_char):
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Unmatched comment)')
            self.current_token_lexeme = ''
        elif re.search(Scanner.wspace, self.current_char):
            self.reset_state_return()
        else:
            self.current_state = 'start'
            self.current_token_lexeme += self.current_char
            self.error_writer.write_error(self.lineno, '(' + self.current_token_lexeme + ', Invalid input)')
            self.current_token_lexeme = ''

    def update_state(self):
        if self.current_state == 'start':
            self.update_start_with_char()
        elif self.current_state == 'num':
            self.update_num_with_char()
        elif self.current_state == 'word':
            self.update_word_with_char()
        elif self.current_state == 'equal':
            self.update_equal_with_char()
        elif self.current_state == 'twoequal':
            self.update_two_equal_with_char()
        elif self.current_state == 'symbol':
            self.update_symbol_with_char()
        elif self.current_state == 'slash':
            self.update_slash_with_char()
        elif self.current_state == 'bcmt':
            self.update_bcmt_with_char()
        elif self.current_state == 'bcmt*':
            self.update_bcmt_star_with_char()
        elif self.current_state == 'lcmt':
            self.update_lcmt_with_char()
        elif self.current_state == 'wspace':
            self.update_white_space_with_char()
        elif self.current_state == 'star':
            self.update_star_with_char()

    def reset_state_return(self):
        self.state_to_return = self.current_state
        self.current_state = 'start'
        self.token_found_return = True

    def generate_token_type(self, temp_lexeme):
        if self.state_to_return == 'word':
            if temp_lexeme in self.keyword_reference_list:
                return 'KEYWORD'
            else:
                if temp_lexeme not in self.id_list:
                    self.id_list.append(temp_lexeme)
                return 'ID'
        else:
            return self.type_by_state_name[self.state_to_return]

    def get_lineno(self):
        return self.temporary_lineno

    def get_next_token(self):
        if self.finished:
            return None
        else:
            while True:
                # Go to next line
                # if self.go_to_next_line:
                #     self.temporary_lineno += 1
                #     self.go_to_next_line = False
                # Read next character
                if not self.token_found_return:
                    if not self.read_again:
                        self.current_char = self.reader.read_next_char()
                    else:
                        self.read_again = False
                # Return the newly-found token
                else:
                    self.token_found_return = False
                    temp_lexeme = self.current_token_lexeme
                    self.temporary_lineno = self.lineno
                    self.current_token_lexeme = ''
                    if self.state_to_return not in ['bcmt', 'bcmt*', 'lcmt', 'wspace']:
                        self.read_again = True
                        return '(' + self.generate_token_type(temp_lexeme) + ', ' + temp_lexeme + ')'
                    elif self.state_to_return == 'bcmt*':
                        continue

                # Return none if the file has ended
                if len(self.current_char) == 0:
                    if self.current_state in ['bcmt', 'bcmt*']:
                        self.error_writer.write_error(self.temporary_lineno, '(' + self.current_token_lexeme[0:7] + '..., Unclosed comment)')
                    self.reader.close_file()
                    self.symbol_writer.write_symbols(self.keyword_reference_list + self.id_list)
                    self.finished = True
                    self.error_writer.close()
                    self.symbol_writer.close()
                    return None

                # Call the method to update the state and construct the token
                self.update_state()
