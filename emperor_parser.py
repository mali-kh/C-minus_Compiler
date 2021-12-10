class Parser:
    PRODUCTIONS = {'Program': [['Declaration_list', '$']],
                   'Declaration_list': [['Declaration', 'Declaration_list'], ['EPSILON']],
                   'Declaration': [['Declaration_initial', 'Declaration_prime']],
                   'Declaration_initial': [['Type_specifier', 'ID']],
                   'Declaration_prime': [['Fun_declaration_prime'], ['Var_declaration_prime']],
                   'Var_declaration_prime': [[';'], ['[', 'NUM', ']', ';']],
                   'Fun_declaration_prime': [['(', 'Params', ')', 'Compound_stmt']],
                   'Type_specifier': [['int'], ['void']],
                   'Params': [['int', 'ID', 'Param_prime', 'Param_list'], ['void']],
                   'Param_list': [[',', 'Param', 'Param_list'], ['EPSILON']],
                   'Param': [['Declaration_initial', 'Param_prime']],
                   'Param_prime': [['[', ']'], ['EPSILON']],
                   'Compound_stmt': [['{', 'Declaration_list', 'Statement_list', '}']],
                   'Statement_list': [['Statement', 'Statement_list'], ['EPSILON']],
                   'Statement': [['Expression_stmt'], ['Compound_stmt'], ['Selection_stmt'], ['Iteration_stmt'],
                                 ['Return_stmt']],
                   'Expression_stmt': [['Expression', ';'], ['break', ';'], [';']],
                   'Selection_stmt': [['if', '(', 'Expression', ')', 'Statement', 'Else_stmt']],
                   'Else_stmt': [['endif'], ['else', 'Statement', 'endif']],
                   'Iteration_stmt': [['repeat', 'Statement', 'until', '(', 'Expression', ')']],
                   'Return_stmt': [['return', 'Return_stmt_prime']],
                   'Return_stmt_prime': [[';'], ['Expression', ';']],
                   'Expression': [['Simple_expression_zegond'], ['ID', 'B']],
                   'B': [['=', 'Expression'], ['[', 'Expression', ']', 'H'], ['Simple_expression_prime']],
                   'H': [['=', 'Expression'], ['G', 'D', 'C']],
                   'Simple_expression_zegond': [['Additive_expression_zegond', 'C']],
                   'Simple_expression_prime': [['Additive_expression_prime', 'C']],
                   'C': [['Relop', 'Additive_expression'], ['EPSILON']],
                   'Relop': [['<'], ['==']],
                   'Additive_expression': [['Term', 'D']],
                   'Additive_expression_prime': [['Term_prime', 'D']],
                   'Additive_expression_zegond': [['Term_zegond', 'D']],
                   'D': [['Addop', 'Term', 'D'], ['EPSILON']],
                   'Addop': [['+'], ['-']],
                   'Term': [['Factor', 'G']],
                   'Term_prime': [['Factor_prime', 'G']],
                   'Term_zegond': [['Factor_zegond', 'G']],
                   'G': [['*', 'Factor', 'G'], ['EPSILON']],
                   'Factor': [['(', 'Expression', ')'], ['ID', 'Var_call_prime'], ['NUM']],
                   'Var_call_prime': [['(', 'Args', ')'], ['Var_prime']],
                   'Var_prime': [['[', 'Expression', ']'], ['EPSILON']],
                   'Factor_prime': [['(', 'Args', ')'], ['EPSILON']],
                   'Factor_zegond': [['(', 'Expression', ')'], ['NUM']],
                   'Args': [['Arg_list'], ['EPSILON']],
                   'Arg_list': [['Expression', 'Arg_list_prime']],
                   'Arg_list_prime': [[',', 'Expression', 'Arg_list_prime'], ['EPSILON']]
                   }

    scany = None

    def __init__(self):
        self.scany = None

    def set_scanner(self, scanner_instance):
        self.scany = scanner_instance

    def run(self):
        stack = ['Program']
        while True:
            next_token = self.scany.get_next_token()

            if next_token is '(KEYWORD, $)':
                break
