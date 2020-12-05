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
            'Program':      self.visit_Program,
            'Function':     self.visit_Function,
            'Param':        self.visit_Param,
            'Code_Block':   self.visit_Code_Block,
            'Type':         self.visit_Type,
            'Var':          self.visit_Var,
            'Var_decl':     self.visit_Var_decl,
            'Assign':       self.visit_Assign,
            'Function_call':self.visit_Function_call,
            'BinOp':        self.visit_BinOp,
            'UnaryOp':      self.visit_UnaryOp,
            'Num':          self.visit_Num,
        }
    
    def calculate(self,a,b,op):
        return self.calcu[op](a,b)
    
    def visit(self,node):
        return self.visiter[type(node).__name__](node)

    def visit_Program(self):
        pass

    def visit_Function(self):
        pass

    def visit_Param(self):
        pass

    def visit_Code_Block(self):
        pass

    def visit_Type(self):
        pass

    def visit_Var(self):
        pass

    def visit_Var_decl(self):
        pass

    def Assign(self):
        pass

    def visit_Function_call(self):
        pass

    def visit_BinOp(self, node):
        return self.calcu[node.op.value](self.visit(node.left),self.visit(node.right))

    def visit_UnaryOp(self, node):
        if(node.op.value == '-'):
            return -(self.visit(node.expr))
        elif(node.op.value == '+'):
            return +(self.visit(node.expr))

    def visit_Num(self, node):
        return node.value
    
    def run(self):
        return self.visit(self.ast)