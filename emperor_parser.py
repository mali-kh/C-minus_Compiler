import scanner
import anytree


class Parser:
    PRODUCTIONS = {'Program': [['Declaration-list', '$']],
                   'Declaration-list': [['Declaration', 'Declaration-list'], ['EPSILON']],
                   'Declaration': [['Declaration-initial', 'Declaration-prime']],
                   'Declaration-initial': [['Type-specifier', 'ID']],
                   'Declaration-prime': [['Fun-declaration-prime'], ['Var-declaration-prime']],
                   'Var-declaration-prime': [[';'], ['[', 'NUM', ']', ';']],
                   'Fun-declaration-prime': [['(', 'Params', ')', 'Compound-stmt']],
                   'Type-specifier': [['int'], ['void']],
                   'Params': [['int', 'ID', 'Param-prime', 'Param-list'], ['void']],
                   'Param-list': [[',', 'Param', 'Param-list'], ['EPSILON']],
                   'Param': [['Declaration-initial', 'Param-prime']],
                   'Param-prime': [['[', ']'], ['EPSILON']],
                   'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
                   'Statement-list': [['Statement', 'Statement-list'], ['EPSILON']],
                   'Statement': [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt'],
                                 ['Return-stmt']],
                   'Expression-stmt': [['Expression', ';'], ['break', ';'], [';']],
                   'Selection-stmt': [['if', '(', 'Expression', ')', 'Statement', 'Else-stmt']],
                   'Else-stmt': [['endif'], ['else', 'Statement', 'endif']],
                   'Iteration-stmt': [['repeat', 'Statement', 'until', '(', 'Expression', ')']],
                   'Return-stmt': [['return', 'Return-stmt-prime']],
                   'Return-stmt-prime': [[';'], ['Expression', ';']],
                   'Expression': [['Simple-expression-zegond'], ['ID', 'B']],
                   'B': [['=', 'Expression'], ['[', 'Expression', ']', 'H'], ['Simple-expression-prime']],
                   'H': [['=', 'Expression'], ['G', 'D', 'C']],
                   'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
                   'Simple-expression-prime': [['Additive-expression-prime', 'C']],
                   'C': [['Relop', 'Additive-expression'], ['EPSILON']],
                   'Relop': [['<'], ['==']],
                   'Additive-expression': [['Term', 'D']],
                   'Additive-expression-prime': [['Term-prime', 'D']],
                   'Additive-expression-zegond': [['Term-zegond', 'D']],
                   'D': [['Addop', 'Term', 'D'], ['EPSILON']],
                   'Addop': [['+'], ['-']],
                   'Term': [['Factor', 'G']],
                   'Term-prime': [['Factor-prime', 'G']],
                   'Term-zegond': [['Factor-zegond', 'G']],
                   'G': [['*', 'Factor', 'G'], ['EPSILON']],
                   'Factor': [['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
                   'Var-call-prime': [['(', 'Args', ')'], ['Var-prime']],
                   'Var-prime': [['[', 'Expression', ']'], ['EPSILON']],
                   'Factor-prime': [['(', 'Args', ')'], ['EPSILON']],
                   'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
                   'Args': [['Arg-list'], ['EPSILON']],
                   'Arg-list': [['Expression', 'Arg-list-prime']],
                   'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'], ['EPSILON']]
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

    FOLLOWS = {'Declaration-list': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
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
    next_token = None
    next_token_symbol = None

    def __init__(self):
        self.scany = None

    def set_scanner(self, scanner_instance):
        self.scany = scanner_instance

    def get_next_token(self):
        if self.next_token_symbol != '$':
            self.next_token = self.scany.get_next_token()
            typie = self.next_token.split(' ')[0][1:-1]
            if typie == 'SYMBOL' or typie == 'KEYWORD':
                self.next_token_symbol = self.next_token.split(' ')[1][0:-1]
            else:
                self.next_token_symbol = typie

    def parsie(self, non_term: str):
        predict_set = self.PREDICTS[non_term]
        i = 0
        for i in range(len(predict_set)):
            if self.next_token_symbol in predict_set[i]:
                break
        else:
            # TODO: Error
            pass
        production_set = self.PRODUCTIONS[non_term][i]
        root_node = anytree.Node(non_term)
        for term in production_set:
            if term in self.NON_TERMINALS:
                child_node = self.parsie(term)
                child_node.parent = root_node
            elif term == 'EPSILON':
                child_node = anytree.Node('epsilon')
                child_node.parent = root_node
            else:
                if term == self.next_token_symbol:
                    child_node = anytree.Node(self.next_token)
                    child_node.parent = root_node
                    self.get_next_token()
                else:
                    pass
                    # TODO: Do some error or something idk
        return root_node

    def run(self):
        non_term = 'Program'
        self.get_next_token()
        parsed_code = self.parsie(non_term)
        for pre, fill, node in anytree.RenderTree(parsed_code):
            print("%s%s" % (pre, node.name))

    # if next_token == '(KEYWORD, $)':
    #     break
