import scanner
import FileManager.file_writer as fw
import FileManager.file_reader as fr

scanner = scanner.Scanner()
token_writer = fw.TokenWriter()

while True:
    next_token = scanner.get_next_token()
    if next_token is None:
        break
    token_writer.write_token(scanner.lineno, next_token)
    print(scanner.lineno)

# reader = fr.Reader()
# while True:
#     print(reader.read_next_char(), end='')
