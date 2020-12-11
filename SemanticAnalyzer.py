from Token import*
from AST import*
from SymbolTable import*

class SemanticAnalyzer():
    def __init__(self,ast,log):
        self.ast = ast
        self.log = log
        self.scope = SymbolTable('outer', 0, None)
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

    def error(self,msg):
        raise Exception(msg)

    def run(self):
        self.visit(self.ast)

    def visit(self,node):
        return self.visiter[type(node).__name__](node)

    def visit_Program(self,node):
        for function in node.function_list:
            self.visit(function)

    def visit_Function(self,node):
        function_name = node.name
        function_type = node.type
        params = node.params
        functionSymbol = FunctionSymbol(function_name, function_type)
        function_scope = SymbolTable(function_name, self.scope.scope_level + 1, self.scope)
        self.scope.insert(functionSymbol)
        self.scope = function_scope
        for param in params:
            param_name = param.var_node.value
            param_type = self.scope.lookup(param.type_node.value)
            varSymbol = VarSymbol(param_name, param_type)
            functionSymbol.params.append(varSymbol)
            self.scope.insert(varSymbol)
        self.visit(node.body)
        self.scope = self.scope.enclosing_scope

    def visit_Param(self,node):
        pass

    def visit_Code_Block(self,node):
        for declaration in node.declarations:
            self.visit(declaration)
        for statement in node.compound_statement:
            self.visit(statement)

    def visit_Type(self,node):
        pass

    def visit_Var(self,node):
        var_name = node.vat_node.value
        # if(self.scope.lookup(var_name) == None):
        #     self.error("Var not found")

    def visit_Var_decl(self,node):
        var_name = node.var_node.value
        # if(self.scope.lookup(var_name) != None):
        #     self.error('Duplicate identifier')
        var_type = self.scope.lookup(node.type_node.value)
        var_symbol = VarSymbol(var_name,var_type)
        self.scope.insert(var_symbol)

    def visit_Assign(self,node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Function_call(self,node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        pass

    def visit_Num(self, node):
        pass

    def visit_Return(self,node):
        pass

    def visit_IF(self,node):
        pass

    def visit_WHILE(self,node):
        pass

    def visit_FOR(self,node):
        pass