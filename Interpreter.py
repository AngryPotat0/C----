from Token import*
from AST import*

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
    
    def calculate(self,a,b,op):
        return self.calcu[op](a,b)
    
    def visit(self,node):
        if(isinstance(node,Num)):
            return node.value
        if(node.op.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULIT, TokenType.DIVES, TokenType.MOD)):
            return self.calculate(self.visit(node.left),self.visit(node.right),node.op.value)
    
    def run(self):
        return self.visit(self.ast)