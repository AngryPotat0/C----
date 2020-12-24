from Lexer import*
from Parser import*
from Interpreter import*
from Token import*
from test import*
from SemanticAnalyzer import*
from Useless import*
from simi import*
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
    ast = parser.parser()
    seman = SemanticAnalyzer(ast,1)
    seman.run()
    asm = ToAsm(ast)
    asm.run()
    s = Simi(asm.asm)
    s.run()

    # interpreter = Interpreter(ast)
    # interpreter.run()
    # test = Test(ast)
    # test.run()

main()