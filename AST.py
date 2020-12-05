class AST():
    pass

class Program(AST):
    def __init__(self,functions_list):
        self.functions_list = functions_list

class Function(AST):
    def __init__(self,type, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Param(AST):
    def __init__(self,var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Code_Block(AST):
    def __init__(self,declarations,compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class Type(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Var_decl(AST):
    def __init__(self,var_name, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Assign(AST):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Function_call(AST):
    def __init__(self,function_name,real_params):
        self.function_name = function_name
        self.real_params = real_params

class If(AST):
    pass

class While(AST):
    pass

class For(AST):
    pass

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