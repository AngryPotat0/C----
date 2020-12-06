from Lexer import*
from Parser import*
from Interpreter import*
from Token import*
from test import*
def main():
    # reserved_keywords()
    text = ""
    file = open('program.txt')
    while(True):
        line = file.readline()
        text += line
        if(not line):
            break
    file.close()
    lex = Lexer(text)
    parser = Parser(lex)
    # interpreter = Interpreter(parser.parser())
    # print(interpreter.run())
    test = Test(parser.parser())
    test.run()

main()