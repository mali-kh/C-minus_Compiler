import scanner
import parser
import FileManager.file_writer as fw

parser = parser.Parser()
scanner = scanner.Scanner()
token_writer = fw.TokenWriter()
# PAY ATTENTION TO THIS!!!
do_scanner_only = True

if do_scanner_only:
    while True:
        next_token = scanner.get_next_token()
        if next_token is None:
            break
        token_writer.write_token(scanner.get_lineno(), next_token)
else:
    parser.set_scanner(scanner)
    parser.run()