class AST():
    pass

class Program(AST):
    def __init__(self):
        pass

class Function(AST):
    def __init__(self):
        pass

class Code_Block(AST):
    pass

class Var(AST):
    def __init__(self,token):
        self.name = token.value

class Assign(AST):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class BinOp(AST):
    def __init__(self,left,right,op):
        self.left = left
        self.right = right
        self.op = op

class Num(AST):
    def __init__(self,token):
        self.type = token.type
        self.value = token.value

class UnaryOp(AST):
    def __init__(self,expr, op):
        self.op = op
        self.expr = expr