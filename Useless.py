from Token import*
from AST import*
from Memory import*

class ToAsm():
    def __init__(self,ast):
        self.ast = ast
        self.function_list = {}
        self.table = {}
        self.addreess = 0
        self.asm = []
        self.visiter = {
            'Program':      self.visit_Program,
            'Function':     self.visit_Function,
            # 'Param':        self.visit_Param,
            'Code_Block':   self.visit_Code_Block,
            # 'Type':         self.visit_Type,
            'Var':          self.visit_Var,
            # 'Array':        self.visit_Array,
            'Var_decl':     self.visit_Var_decl,
            # 'Array_decl':   self.visit_Array_decl,
            'Assign':       self.visit_Assign,
            # 'Function_call':self.visit_Function_call,
            'BinOp':        self.visit_BinOp,
            # 'UnaryOp':      self.visit_UnaryOp,
            'Num':          self.visit_Num,
            'Return':       self.visit_Return,
            'Break':        self.visit_Break,
            'Continue':     self.visit_Continue,
            'If':           self.visit_If,
            'While':        self.visit_While,
            'For':          self.visit_For,
            'Block':        self.visit_Block,
        }

    def run(self):
        self.visit(self.ast)
        self.asm.append('HALT')
        for command in self.asm:
            print(command)

    
    def visit(self,node):
        return self.visiter[type(node).__name__](node)

    def visit_Program(self, node):
        for function in node.function_list:
            self.function_list[function.name] = function
        if('main' in self.function_list):
            status = self.visit_Function(self.function_list['main'],[])
            return status
        else:
            raise Exception('Main function cannot found')

    def visit_Function(self, node, actual_params):#only have main function
        self.visit(node.body)

    def visit_Code_Block(self, node):
        for decl in node.declarations:
            self.visit(decl)
        for statement in node.compound_statement:
            self.visit(statement)

    def visit_Var(self, node):
        addreess = hex(self.table[node.value])
        self.asm.append('LDA {addr}'.format(addr=addreess))

    def visit_Var_decl(self, node):#语义分析阶段已经确定了变量合法性的问题
        self.table[node.var_node.value] = self.addreess
        self.addreess += 1

    def visit_Assign(self, node):
        address = hex(self.table[node.left.value])
        self.visit(node.right)
        self.asm.append('STA {addr}'.format(addr=address))

    def visit_BinOp(self, node):
        OP = 'ADD' if node.op.value == '+' else 'SUB'
        self.visit(node.right)
        self.asm.append('MOV R0 A')
        self.visit(node.left)
        self.asm.append('{op} A R0'.format(op = OP))

    def visit_Num(self, node):
        self.asm.append('MOV A #{data}'.format(data=node.value))

    def visit_Break(self, node):
        pass

    def visit_Continue(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_While(self, node):#TODO: break, continue
        pass

    def visit_For(self, node):
        pass

    def visit_Block(self, node):
        pass
