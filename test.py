from Token import*
from AST import*
from SymbolTable import*

class Test():
    def __init__(self,ast):
        self.ast = ast
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
            'Return':       self.visit_Return,
            'IF':           self.visit_IF,
            'WHILE':        self.visit_WHILE,
            'FOR':          self.visit_FOR,
        }
    
    def run(self):
        self.visit(self.ast)

    def visit(self,node):
        return self.visiter[type(node).__name__](node)

    def visit_Program(self,node):
        print("Program:")
        for function in node.function_list:
            print("function:{name}, type :{type}".format(name = function.name, type = function.type))
        print("-----------------------------")
        for function in node.function_list:
            self.visit(function)

    def visit_Function(self,node):
        print("function: {name}".format(name = node.name))
        for param in node.params:
            self.visit(param)
        self.visit(node.body)
        print("-----------------------------")

    def visit_Param(self,node):
        print("param: {name},type: {type}".format(name = node.var_node.value,type = node.type_node.value))

    def visit_Code_Block(self,node):
        for decl in node.declarations:
            self.visit(decl)
        for statement in node.compound_statement:
            self.visit(statement)

    def visit_Type(self,node):
        pass

    def visit_Var(self,node):
        return node.value

    def visit_Var_decl(self,node):
        print("Var_decl: name: {name},type: {type}".format(name = node.var_node.value, type = node.type_node.value))

    def visit_Assign(self,node):
        expr = self.visit(node.right)
        print("Assign: {left}={right}".format(left=node.left.value,right=expr))

    def visit_Function_call(self,node):
        print('Call function:{name}'.format(name=node.function_name))
        return 'Call function:{name}'.format(name=node.function_name)

    def visit_BinOp(self, node):
        return '{left}{op}{right}'.format(
            left=self.visit(node.left),op = node.op.value,right=self.visit(node.right)
            )

    def visit_UnaryOp(self, node):
        pass

    def visit_Num(self, node):
        return node.value

    def visit_Return(self,node):
        pass

    def visit_IF(self,node):
        pass

    def visit_WHILE(self,node):
        pass

    def visit_FOR(self,node):
        pass