from enum import Enum

class TokenType(Enum):
    PLUS =      '+'
    MINUS =     '-'
    MULIT =     '*'
    DIVES =     '/'
    MOD =       '%'
    LPAREN =    '('
    RPAREN =    ')'
    Num =       'Num'

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'Token type:{type},value:{value}'.format(type=self.type, value=self.value)

class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.currentChar = self.text[self.pos]
    
    def advance(self):
        self.pos += 1
        if(self.pos >= len(self.text)):
            self.currentChar = None
            return
        self.currentChar = self.text[self.pos]
    
    def skip_whitespace(self):
        while(self.currentChar != None and self.currentChar == ' '):
            self.advance()
        
    def number(self):
        res = ''
        while(self.currentChar != None and self.currentChar.isdigit()):
            res += self.currentChar
            self.advance()
        if(self.currentChar == '.'):
            res += '.'
            while(self.currentChar != None and self.currentChar.isdigit()):
                res += self.currentChar
                self.advance()
            return float(res)
        return int(res)

    def error(self):
        raise Exception('Unexpectde char')
    
    def get_next_token(self):
        while(True):
            if(self.currentChar == None):
                return None
            if(self.currentChar == ' '):
                self.skip_whitespace()
                continue
            if(self.currentChar.isdigit()):
                value = self.number()
                token = Token(TokenType.Num,value)
                return token
            try:
                token_type = TokenType(self.currentChar)
            except ValueError:
                self.error()
            token = Token(token_type,token_type.value)
            self.advance()
            return token

class AST():
    pass

class BinOp(AST):
    def __init__(self,left,right,op):
        self.left = left
        self.right = right
        self.op = op

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Parser():
    def __init__(self,lex):
        self.lex = lex
        self.currentToken = self.lex.get_next_token()

    def eat(self,expect_type):
        if(self.currentToken.type != expect_type):
            self.error()
        self.currentToken = self.lex.get_next_token()
    
    def error(self):
        raise Exception('Unexpected Token')
    
    def parser(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while(self.currentToken.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.currentToken
            if(op.type == TokenType.PLUS):
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinOp(node, self.term(), op)
        return node

    def term(self):
        node = self.paren()
        while(self.currentToken.type in (TokenType.MULIT, TokenType.DIVES)):
            op = self.currentToken
            if(op.type == TokenType.MULIT):
                self.eat(TokenType.MULIT)
            else:
                self.eat(TokenType.DIVES)
            node = BinOp(node,self.paren(),op)
        return node

    def paren(self):
        node = None
        if(self.currentToken.type == TokenType.LPAREN):
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
        node = Num(self.currentToken)
        self.eat(TokenType.Num)
        return node

class Interpreter():
    def __init__(self,ast):
        self.ast = ast
        self.calcu = {
            '+':    lambda a,b: a + b,
            '-':    lambda a,b: a - b,
            '*':    lambda a,b: a * b,
            '/':    lambda a,b: a / b,
            '%':    lambda a,b: a % b
        }
    
    def caculate(self,a,b,op):
        return self.calcu[op](a,b)
    
    def visit(self,node):
        if(node.type == TokenType.Num):
            return node.value
        if(node.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULIT, TokenType.DIVES, TokenType.MOD)):
            return self.calculate(node.left,node.right,node.value)

def main():
    text = input('Please input:')
    lex = Lexer(text)
    parser = Parser(lex)
    interpreter = Interpreter(parser.parser())
    print(interpreter.visit())

main()