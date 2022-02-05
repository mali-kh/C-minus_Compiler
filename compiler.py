# Seyyed Mohammad Sadegh Tabaian - 98105868
# Mohammad Ali Khodabandelou - 98101482

import FileManager.file_writer as fw
import emperor_parser
import scanner
import codegen
import semantic_checker

token_writer = fw.TokenWriter()
scanner = scanner.Scanner()
codegen = codegen.Codegen()
semanticer = semantic_checker.SemanticChecker()
parser = emperor_parser.Parser()
# PAY ATTENTION TO THIS!!!
do_scanner_only = False

if do_scanner_only:
    while True:
        next_token = scanner.get_next_token()
        if next_token is None:
            break
        token_writer.write_token(scanner.get_lineno(), next_token)
else:
    parser.set_scanner(scanner)
    parser.set_codegen_and_semantic_checker(codegen, semanticer)
    parser.run()
