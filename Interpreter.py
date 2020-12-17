from Token import*
from AST import*
from Memory import*

class Interpreter():
    def __init__(self,ast):
        self.ast = ast
        self.memory = CallStack()
        self.calcu = {
            '+':    lambda a,b: a + b,
            '-':    lambda a,b: a - b,
            '*':    lambda a,b: a * b,
            '/':    lambda a,b: a / b,
            '%':    lambda a,b: a % b,
            '&':    lambda a,b: a & b,
            '|':    lambda a,b: a | b,
            '^':    lambda a,b: a ^ b,
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
            'Return':       self.visit_Return,
            'If':           self.visit_If,
            'While':        self.visit_While,
            'For':          self.visit_For,
            'Block':        self.visit_Block,
        }
    
    def calculate(self,a,b,op):
        return self.calcu[op](a,b)

    def visit_print(self,actual_params):
        for param in actual_params:
            print(self.visit(param))

    def visit_input(self):#FIXME:
        temp = input()
        return int(temp)
    
    def visit(self,node):
        return self.visiter[type(node).__name__](node)

    def visit_Program(self, node):
        main_function = [function for function in node.function_list if function.name == 'main']
        if(main_function != []):
            main_function = main_function[0]
        else:
            raise Exception('Main function cannot found')
        status = self.visit_Function(main_function,[])
        return status

    def visit_Function(self, node, actual_params):
        self.memory.push(Frame(node.name,2))
        current_frame = self.memory.peek()
        for name, value in zip(node.params, actual_params):
            current_frame.set_value(name.var_node.value, self.visit(value))
        return_value = self.visit(node.body)#FIXME:
        self.memory.pop()
        return return_value

    def visit_Param(self, node):
        pass

    def visit_Code_Block(self, node):
        current_frame = self.memory.peek()
        for decl in node.declarations:
            current_frame.set_value(decl.var_node.value,0)
        for statement in node.compound_statement:
            if(isinstance(statement,Return)):
                return self.visit_Return(statement)
            self.visit(statement)
            

    def visit_Type(self, node):
        pass

    def visit_Var(self, node):
        return self.memory.peek().get_value(node.value)

    def visit_Var_decl(self, node):
        pass

    def visit_Assign(self, node):
        left = node.left.value
        right = self.visit(node.right)
        self.memory.peek().set_value(left,right)

    def visit_Function_call(self, node):
        actual_params = [param for param in node.real_params]
        if(node.function_name == 'print'):
            self.visit_print(actual_params)
        elif(node.function_name == 'input'):
            return self.visit_input()
        else:
            return self.visit_function(func, actual_params)#FIXME:

    def visit_BinOp(self, node):
        op = node.op.value
        if(op == '=='):
            return self.visit(node.left) == self.visit(node.right)
        elif(op == '!='):
            return self.visit(node.left) != self.visit(node.right)
        elif(op == '>'):
            return self.visit(node.left) > self.visit(node.right)
        elif(op == '<'):
            return self.visit(node.left) < self.visit(node.right)
        elif(op == '>='):
            return self.visit(node.left) >= self.visit(node.right)
        elif(op == '<='):
            return self.visit(node.left) <= self.visit(node.right)
        elif(op == '&&'):
            return self.visit(node.left) and self.visit(node.right)
        elif(op == '||'):
            return self.visit(node.left) or self.visit(node.right)
        return self.calcu[node.op.value](self.visit(node.left),self.visit(node.right))

    def visit_UnaryOp(self, node):
        if(node.op.value == '-'):
            return -(self.visit(node.expr))
        elif(node.op.value == '+'):
            return +(self.visit(node.expr))
        elif(node.op.value == '!'):
           return not(self.visit(node.expr))
        elif(node.op.value == '~'):
            return ~(self.visit(node.expr))

    def visit_Num(self, node):
        return node.value

    def visit_Return(self, node):
        return self.visit(node.return_expr)

    def visit_If(self, node):
        if(self.visit(node.expr)):
            self.visit(node.block)

    def visit_While(self, node):#TODO: break, continue
        while(self.visit(node.expr)):
            self.visit(node.block)

    def visit_For(self, node):
        pass

    def visit_Block(self, node):
        for statement in node.compound_statement:
            self.visit(statement)
    
    def run(self):
        status = self.visit(self.ast)
        if(status != 0):
            raise Exception('Program Error')