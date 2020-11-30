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
        self.visiter = {
            'BinOp':    self.BinOp,
            'UnaryOp':  self.UnaryOp,
            'Num':      self.Num,
        }
    
    def calculate(self,a,b,op):
        return self.calcu[op](a,b)
    
    def visit(self,node):
        return self.visiter[type(node).__name__](node)
    def BinOp(self, node):
        return self.calcu[node.op.value](self.visit(node.left),self.visit(node.right))

    def UnaryOp(self, node):
        if(node.op.value == '-'):
            return -(self.visit(node.expr))
        elif(node.op.value == '+'):
            return +(self.visit(node.expr))

    def Num(self, node):
        return node.value
    
    def run(self):
        return self.visit(self.ast)