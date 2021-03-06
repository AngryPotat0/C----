class AST():
    pass

class Program(AST):
    def __init__(self,function_list):
        self.function_list = function_list

class Function(AST):
    def __init__(self,type, name, params, body):
        self.type = type
        self.name = name
        self.params = params
        self.body = body

class Return(AST):
    def __init__(self,return_expr):
        self.return_expr = return_expr

class Param(AST):
    def __init__(self,var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Code_Block(AST):
    def __init__(self,declarations,compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement#FIXME:Do we need to create a Compound node for AST?

class Type(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Array(AST):
    def __init__(self, var_node,index):
        self.var_node = var_node
        self.index = index

class Var_decl(AST):
    def __init__(self,var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Array_decl(AST):
    def __init__(self,var_node, type_node, length):
        self.var_node = var_node
        self.type_node = type_node
        self.length = length

class Assign(AST):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Function_call(AST):
    def __init__(self,function_name,real_params):
        self.function_name = function_name
        self.real_params = real_params#each param is a expr
        self.params = None
        self.body = None

class If(AST):
    def __init__(self,expr,block,else_block):
        self.expr = expr
        self.block = block
        self.else_block = else_block

class While(AST):
    def __init__(self,expr,block):
        self.expr = expr
        self.block = block

class For(AST):
    def __init__(self,assign1,expr,assign2,block):
        self.assign1 = assign1
        self.expr = expr
        self.assign2 = assign2
        self.block = block

class Break(AST):
    def __init__(self):
        pass

class Continue(AST):
    def __init__(self):
        pass

class Block(AST):
    def __init__(self,compound_statement):
        self.compound_statement = compound_statement

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