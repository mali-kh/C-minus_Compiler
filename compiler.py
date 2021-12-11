import FileManager.file_writer as fw
import scanner
import emperor_parser
# from parser import Parser

token_writer = fw.TokenWriter()
scanner = scanner.Scanner()
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
    parser.run()
