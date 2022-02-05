import anytree
import FileManager.file_writer as fw

class Parser:
    PRODUCTIONS = {'Program': [['Declaration-list', '$']],
                   'Declaration-list': [['Declaration', 'Declaration-list'], ['EPSILON']],
                   'Declaration': [['Declaration-initial', 'Declaration-prime']],
                   'Declaration-initial': [['Type-specifier', '#declare_pid', 'ID']],
                   'Declaration-prime': [['#label', '#declare_func', '#increase_scope', 'Fun-declaration-prime', '#decrease_scope'], ['Var-declaration-prime']],
                   'Var-declaration-prime': [['#declare_var', ';'], ['[', '#parr_size', 'NUM', ']', '#declare_array', ';']],
                   'Fun-declaration-prime': [['(', 'Params', ')', 'Compound-stmt', '#implicit_return']],
                   'Type-specifier': [['#ptype_int', 'int'], ['#ptype_void', 'void']],
                   'Params': [['#ptype_int', 'int', '#declare_pid', 'ID', 'Param-prime', 'Param-list'], ['void']],
                   'Param-list': [[',', 'Param', 'Param-list'], ['EPSILON']],
                   'Param': [['Declaration-initial', 'Param-prime']],
                   'Param-prime': [['[', ']', '#declare_pointer_param'], ['EPSILON', '#declare_var_param']],
                   'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
                   'Statement-list': [['Statement', 'Statement-list'], ['EPSILON']],
                   'Statement': [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt'], ['Return-stmt']],
                   'Expression-stmt': [['Expression', '#pop', ';'], ['break', '#break_jump', ';'], [';']],
                   'Selection-stmt': [['if', '(', 'Expression', ')', '#save', '#increase_scope', 'Statement', '#decrease_scope', 'Else-stmt']],
                   'Else-stmt': [['#jpf', 'endif'], ['else', '#jpf_with_else', '#save', '#increase_scope', 'Statement', '#decrease_scope', '#jp', 'endif']],
                   'Iteration-stmt': [['repeat', '#repeat_count_plus', '#label', '#increase_scope', 'Statement', '#decrease_scope', 'until', '#repeat_count_minus', '(', 'Expression', '#until', ')']],
                   'Return-stmt': [['return', 'Return-stmt-prime']],
                   'Return-stmt-prime': [['#return_empty', ';'], ['Expression', '#return_from_stack', ';']],
                   'Expression': [['Simple-expression-zegond'], ['#pid', 'ID', 'B']],
                   'B': [['=', 'Expression', '#relnum_op', '#assign'], ['[', 'Expression', ']', '#get_array_element', 'H'], ['Simple-expression-prime']],
                   'H': [['=', 'Expression', '#relnum_op', '#assign'], ['G', 'D', 'C']],
                   'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
                   'Simple-expression-prime': [['Additive-expression-prime', 'C']],
                   'C': [['Relop', 'Additive-expression', '#relnum_op', '#calculate_relation'], ['EPSILON']],
                   'Relop': [['#psmaller_than', '<'], ['#pequals', '==']],
                   'Additive-expression': [['Term', 'D']],
                   'Additive-expression-prime': [['Term-prime', 'D']],
                   'Additive-expression-zegond': [['Term-zegond', 'D']],
                   'D': [['Addop', 'Term', '#relnum_op', '#calculate_addition', 'D'], ['EPSILON']],
                   'Addop': [['#pplus', '+'], ['#pminus', '-']],
                   'Term': [['Factor', 'G']],
                   'Term-prime': [['Factor-prime', 'G']],
                   'Term-zegond': [['Factor-zegond', 'G']],
                   'G': [['*', 'Factor', '#relnum_op', '#calculate_multiplication', 'G'], ['EPSILON']],
                   'Factor': [['(', 'Expression', ')'], ['#pid', 'ID', 'Var-call-prime'], ['#pnum', 'NUM']],
                   'Var-call-prime': [['#get_function_ready', '(', 'Args', ')', '#function_call'], ['Var-prime']],
                   'Var-prime': [['[', 'Expression', ']', '#get_array_element'], ['EPSILON']],
                   'Factor-prime': [['#get_function_ready', '(', 'Args', ')', '#function_call'], ['EPSILON']],
                   'Factor-zegond': [['(', 'Expression', ')'], ['#pnum', 'NUM']],
                   'Args': [['Arg-list'], ['EPSILON']],
                   'Arg-list': [['Expression', '#arg_count_plus', 'Arg-list-prime']],
                   'Arg-list-prime': [[',', 'Expression', '#arg_count_plus', 'Arg-list-prime'], ['EPSILON']]
                   }

    PREDICTS = {'Program': [['int', 'void', '$']],
                'Declaration-list': [['int', 'void'],
                                     ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']],
                'Declaration': [['int', 'void']],
                'Declaration-initial': [['int', 'void']],
                'Declaration-prime': [['('], [';', '[']],
                'Var-declaration-prime': [[';'], ['[']],
                'Fun-declaration-prime': [['(']],
                'Type-specifier': [['int'], ['void']],
                'Params': [['int'], ['void']],
                'Param-list': [[','], [')']],
                'Param': [['int', 'void']],
                'Param-prime': [['['], [',', ')']],
                'Compound-stmt': [['{']],
                'Statement-list': [['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], ['}']],
                'Statement': [['break', ';', 'ID', '(', 'NUM'], ['{'], ['if'], ['repeat'], ['return']],
                'Expression-stmt': [['ID', '(', 'NUM'], ['break'], [';']],
                'Selection-stmt': [['if']],
                'Else-stmt': [['endif'], ['else']],
                'Iteration-stmt': [['repeat']],
                'Return-stmt': [['return']],
                'Return-stmt-prime': [[';'], ['ID', '(', 'NUM']],
                'Expression': [['(', 'NUM'], ['ID']],
                'B': [['='], ['['], ['(', '*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'H': [['='], ['*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'Simple-expression-zegond': [['(', 'NUM']],
                'Simple-expression-prime': [['(', '*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'C': [['<', '=='], [';', ')', ']', ',']],
                'Relop': [['<'], ['==']],
                'Additive-expression': [['(', 'ID', 'NUM']],
                'Additive-expression-prime': [['(', '*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'Additive-expression-zegond': [['(', 'NUM']],
                'D': [['+', '-'], ['<', '==', ';', ')', ']', ',']],
                'Addop': [['+'], ['-']],
                'Term': [['(', 'ID', 'NUM']],
                'Term-prime': [['(', '*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'Term-zegond': [['(', 'NUM']],
                'G': [['*'], ['+', '-', '<', '==', ';', ')', ']', ',']],
                'Factor': [['('], ['ID'], ['NUM']],
                'Var-call-prime': [['('], ['[', '*', '+', '-', ';', ')', '<', '==', ']', ',']],
                'Var-prime': [['['], ['*', '+', '-', ';', ')', '<', '==', ']', ',']],
                'Factor-prime': [['('], ['*', '+', '-', '<', '==', ';', ')', ']', ',']],
                'Factor-zegond': [['('], ['NUM']],
                'Args': [['ID', '(', 'NUM'], [')']],
                'Arg-list': [['ID', '(', 'NUM']],
                'Arg-list-prime': [[','], [')']]
                }

    FOLLOWS = {'Program': [],
               'Declaration-list': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
               'Declaration': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
               'Declaration-initial': ['(', ';', '[', ',', ')'],
               'Declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM',
                                     '}'],
               'Var-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
                                         'NUM', '}'],
               'Fun-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
                                         'NUM', '}'],
               'Type-specifier': ['ID'],
               'Params': [')'],
               'Param-list': [')'],
               'Param': [',', ')'],
               'Param-prime': [',', ')'],
               'Compound-stmt': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
                                 'endif', 'else', 'until'],
               'Statement-list': ['}'],
               'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                             'until'],
               'Expression-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                   'until'],
               'Selection-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                  'until'],
               'Else-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                             'until'],
               'Iteration-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                                  'until'],
               'Return-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
                               'until'],
               'Return-stmt-prime': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif',
                                     'else', 'until'],
               'Expression': [';', ')', ']', ','],
               'B': [';', ')', ']', ','],
               'H': [';', ')', ']', ','],
               'Simple-expression-zegond': [';', ')', ']', ','],
               'Simple-expression-prime': [';', ')', ']', ','],
               'C': [';', ')', ']', ','],
               'Relop': ['(', 'ID', 'NUM'],
               'Additive-expression': [';', ')', ']', ','],
               'Additive-expression-prime': ['<', '==', ';', ')', ']', ','],
               'Additive-expression-zegond': ['<', '==', ';', ')', ']', ','],
               'D': ['<', '==', ';', ')', ']', ','],
               'Addop': ['(', 'ID', 'NUM'],
               'Term': ['+', '-', ';', ')', '<', '==', ']', ','],
               'Term-prime': ['+', '-', '<', '==', ';', ')', ']', ','],
               'Term-zegond': ['+', '-', '<', '==', ';', ')', ']', ','],
               'G': ['+', '-', '<', '==', ';', ')', ']', ','],
               'Factor': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
               'Var-call-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
               'Var-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
               'Factor-prime': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
               'Factor-zegond': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
               'Args': [')'],
               'Arg-list': [')'],
               'Arg-list-prime': [')'],
               }

    FIRSTS = {'Program': ['$', 'int', 'void'],
              'Declaration-list': ['EPSILON', 'int', 'void'],
              'Declaration': ['int', 'void'],
              'Declaration-initial': ['int', 'void'],
              'Declaration-prime': ['(', ';', '['],
              'Var-declaration-prime': [';', '['],
              'Fun-declaration-prime': ['('],
              'Type-specifier': ['int', 'void'],
              'Params': ['int', 'void'],
              'Param-list': [',', 'EPSILON'],
              'Param': ['int', 'void'],
              'Param-prime': ['[', 'EPSILON'],
              'Compound-stmt': ['{'],
              'Statement-list': ['EPSILON', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
              'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
              'Expression-stmt': ['break', ';', 'ID', '(', 'NUM'],
              'Selection-stmt': ['if'],
              'Else-stmt': ['endif', 'else'],
              'Iteration-stmt': ['repeat'],
              'Return-stmt': ['return'],
              'Return-stmt-prime': [';', 'ID', '(', 'NUM'],
              'Expression': ['ID', '(', 'NUM'],
              'B': ['=', '[', '(', '*', '+', '-', '<', '==', 'EPSILON'],
              'H': ['=', '*', 'EPSILON', '+', '-', '<', '=='],
              'Simple-expression-zegond': ['(', 'NUM'],
              'Simple-expression-prime': ['(', '*', '+', '-', '<', '==', 'EPSILON'],
              'C': ['EPSILON', '<', '=='],
              'Relop': ['<', '=='],
              'Additive-expression': ['(', 'ID', 'NUM'],
              'Additive-expression-prime': ['(', '*', '+', '-', 'EPSILON'],
              'Additive-expression-zegond': ['(', 'NUM'],
              'D': ['EPSILON', '+', '-'],
              'Addop': ['+', '-'],
              'Term': ['(', 'ID', 'NUM'],
              'Term-prime': ['(', '*', 'EPSILON'],
              'Term-zegond': ['(', 'NUM'],
              'G': ['*', 'EPSILON'],
              'Factor': ['(', 'ID', 'NUM'],
              'Var-call-prime': ['(', '[', 'EPSILON'],
              'Var-prime': ['[', 'EPSILON'],
              'Factor-prime': ['(', 'EPSILON'],
              'Factor-zegond': ['(', 'NUM'],
              'Args': ['EPSILON', 'ID', '(', 'NUM'],
              'Arg-list': ['ID', '(', 'NUM'],
              'Arg-list-prime': [',', 'EPSILON']
              }
    NON_TERMINALS = ['Program', 'Declaration-list', 'Declaration', 'Declaration-initial', 'Declaration-prime',
                     'Var-declaration-prime', 'Fun-declaration-prime', 'Type-specifier', 'Params', 'Param-list',
                     'Param', 'Param-prime', 'Compound-stmt', 'Statement-list', 'Statement', 'Expression-stmt',
                     'Selection-stmt', 'Else-stmt', 'Iteration-stmt', 'Return-stmt', 'Return-stmt-prime',
                     'Expression', 'B', 'H', 'Simple-expression-zegond', 'Simple-expression-prime', 'C', 'Relop',
                     'Additive-expression', 'Additive-expression-prime', 'Additive-expression-zegond', 'D', 'Addop',
                     'Term', 'Term-prime', 'Term-zegond', 'G', 'Factor', 'Var-call-prime', 'Var-prime',
                     'Factor-prime', 'Factor-zegond', 'Args', 'Arg-list', 'Arg-list-prime']

    scany = None
    codegeny = None
    semantic_checkerie = None
    next_token = None
    next_token_symbol = None
    reached_EOF = False


    def __init__(self):
        self.syntax_error_writer = fw.SyntaxErrorWriter()
        self.parse_tree_writer = fw.ParseTreeWriter()
        self.scany = None
        self.codegeny = None
        self.semantic_checkerie = None

    def set_scanner(self, scanner_instance):
        self.scany = scanner_instance

    def set_codegen_and_semantic_checker(self, codegen_instance, semantic_checker_instance):
        self.codegeny = codegen_instance
        self.semantic_checkerie = semantic_checker_instance
        self.semantic_checkerie.set_codegen(self.codegeny)

    def get_next_token(self):
        self.next_token = self.scany.get_next_token()
        typie = self.next_token.split(' ')[0][1:-1]
        if typie == 'SYMBOL' or typie == 'KEYWORD':
            self.next_token_symbol = self.next_token.split(' ')[1][0:-1]
        else:
            self.next_token_symbol = typie

    def parsie(self, non_term: str):
        predict_set = self.PREDICTS[non_term]

        continue_searching = True
        i = 0
        while continue_searching:
            i = 0
            continue_searching = False
            for i in range(len(predict_set)):
                if self.next_token_symbol in predict_set[i]:
                    break
            else:
                if self.next_token_symbol in self.FOLLOWS[non_term]:
                    self.syntax_error_writer.write_syntax_error(self.scany.get_lineno(), "missing " + non_term)
                    return None
                else:
                    if self.next_token_symbol == '$':
                        self.syntax_error_writer.write_syntax_error(self.scany.get_lineno(), "Unexpected EOF")
                        self.reached_EOF = True
                        return None
                    self.syntax_error_writer.write_syntax_error(self.scany.get_lineno(), "illegal " + self.next_token_symbol)
                    self.get_next_token()
                    continue_searching = True

        production_set = self.PRODUCTIONS[non_term][i]
        root_node = anytree.Node(non_term)
        for term in production_set:
            if term.startswith('#'):
                token = self.next_token.split(', ')[1][0:-1]
                self.semantic_checkerie.check(term, token, self.scany.get_lineno())
                self.codegeny.generate_code(term, token)
            elif term in self.NON_TERMINALS:
                child_node = self.parsie(term)
                if child_node is not None:
                    child_node.parent = root_node
                if self.reached_EOF:
                    return root_node
            elif term == 'EPSILON':
                child_node = anytree.Node('epsilon')
                child_node.parent = root_node
            else:
                if term == self.next_token_symbol:
                    if self.next_token_symbol != '$':
                        child_node = anytree.Node(self.next_token)
                        child_node.parent = root_node
                        self.get_next_token()
                    else:
                        child_node = anytree.Node('$')
                        child_node.parent = root_node
                else:
                    self.syntax_error_writer.write_syntax_error(self.scany.get_lineno(), "missing " + term)
                    pass
        return root_node

    def run(self):
        non_term = 'Program'
        self.get_next_token()
        self.reached_EOF = False
        parsed_code = self.parsie(non_term)
        self.parse_tree_writer.write_parse_tree(parsed_code)
        self.syntax_error_writer.close()
        self.parse_tree_writer.close()
        self.codegeny.pop_three_useless_codes()
        self.codegeny.write_generated_code()
        self.semantic_checkerie.write_errors()
