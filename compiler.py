import scanner
import FileManager.file_writer as fw

scanner = scanner.Scanner()
token_writer = fw.TokenWriter()

while True:
    next_token = scanner.get_next_token()
    if next_token is None:
        break
    token_writer.write_token(next_token)
