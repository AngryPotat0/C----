from Lexer import*
from Parser import*
from Interpreter import*

def main():
    text = input('Please input:')
    lex = Lexer(text)
    parser = Parser(lex)
    interpreter = Interpreter(parser.parser())
    print(interpreter.run())

main()