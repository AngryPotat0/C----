from Token import*
from AST import*
from Memory import*

class ToAsm():
    def __init__(self,ast):
        self.ast = ast
        self.function_list = {}
        self.table = {}
        self.address = 0
        self.rsp = 0
        self.asm = []
        self.visiter = {
            'Program':      self.visit_Program,
            'Function':     self.visit_Function,
            # 'Param':        self.visit_Param,
            'Code_Block':   self.visit_Code_Block,
            # 'Type':         self.visit_Type,
            'Var':          self.visit_Var,
            'Array':        self.visit_Array,
            'Var_decl':     self.visit_Var_decl,
            'Array_decl':   self.visit_Array_decl,
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
        i = 0
        for command in self.asm:
            print(self.hex(i) ,command)
            i += 1

    
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
        self.rsp = self.address
        for statement in node.compound_statement:
            self.visit(statement)

    def visit_Var(self, node):
        address = self.hex(self.table[node.value])
        self.asm.append('LDA {addr}'.format(addr=address))

    def visit_Var_decl(self, node):#语义分析阶段已经确定了变量合法性的问题
        self.table[node.var_node.value] = self.address
        self.address += 1

    def visit_Assign(self, node):
        address = self.hex(self.table[node.left.value])
        self.visit(node.right)
        self.asm.append('STA {addr}'.format(addr=address))

    def visit_BinOp(self, node):#关于逻辑运算，0为True，非0为False
        if(node.op.value in ('+', '-')):
            OP = 'ADD' if node.op.value == '+' else 'SUB'
            self.visit(node.left)
            self.push('A')
            self.visit(node.right)
            self.asm.append('MOV R0 A')
            self.pop('A')
            self.asm.append('{op} A R0'.format(op=OP))
        elif(node.op.value == '=='):
            self.visit(node.left)
            self.asm.append('MOV R1 A')
            self.visit(node.right)
            self.asm.append('SUB A R1')
        elif(node.op.value == '!='):
            self.visit(node.right)
            self.asm.append('MOV R1 A')
            self.visit(node.left)
            self.asm.append('SUB A R1')
            self.asm.append('JZ {addr}'.format(addr=self.hex(len(self.asm) + 3)))
            self.asm.append('MOV A #0')
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('MOV A #01')
        elif(node.op.value == '>='):
            self.visit(node.right)
            self.asm.append('MOV R1 A')
            self.visit(node.left)
            self.asm.append('SUB A R1')
            self.asm.append('JC {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 3)))
            self.asm.append('MOV A #01')
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('MOV A #0')
        elif(node.op.value == '<='):
            self.visit(node.left)
            self.asm.append('MOV R1 A')
            self.visit(node.right)
            self.asm.append('SUB A R1')
            self.asm.append('JC {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 3)))
            self.asm.append('MOV A #01')
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('MOV A #0')
        elif(node.op.value == '<'):
            self.visit(node.right)
            self.asm.append('MOV R1 A')
            self.visit(node.left)
            self.asm.append('SUB A R1')
            self.asm.append('JC {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 3)))
            self.asm.append('MOV A #00')
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('MOV A #01')
        elif(node.op.value == '>'):
            self.visit(node.left)
            self.asm.append('MOV R1 A')
            self.visit(node.right)
            self.asm.append('SUB A R1')
            self.asm.append('JC {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 3)))
            self.asm.append('MOV A #00')
            self.asm.append('JMP {addr}'.format(addr=self.hex(len(self.asm) + 2)))
            self.asm.append('MOV A #01')


    def push(self, distance):
        # self.asm.append('PUSH {dist}'.format(dist=distance))
        if(distance != 'A'):
            self.asm.append('MOV A {dist}'.format(dist=distance))
        self.asm.append('STA {addr}'.format(addr=self.hex(self.rsp)))
        self.rsp += 1

    def pop(self, distance):
        # self.asm.append('POP {dist}'.format(dist=distance))
        self.rsp -= 1
        self.asm.append('LDA {addr}'.format(addr=self.hex(self.rsp)))
        if(distance != 'A'):
            self.asm.append('MOV {dist} A'.format(dist=distance))

    def visit_Num(self, node):
        self.asm.append('MOV A #{data}'.format(data=node.value))

    def visit_Break(self, node):
        pass

    def visit_Continue(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_If(self, node):#TODO:也许可以优化一下else_block为None的情况
        expr = node.expr
        block1 = node.block
        block2 = node.else_block
        L = len(self.asm)
        self.visit(expr)
        self.asm.append('JZ {dist}'.format(dist=self.hex(len(self.asm) + 2)))
        self.asm.append('JMP BLK2')
        BLK = len(self.asm)
        self.visit(block1)
        self.asm.append('JMP END')
        BLK2 = len(self.asm)
        if(block2 != None):
            self.visit(block2)
        END = len(self.asm)
        self.asm[BLK - 1] = 'JMP {dist}'.format(dist=self.hex(BLK2))
        self.asm[BLK2 - 1] = 'JMP {dist}'.format(dist=self.hex(END))

    def visit_While(self, node):#FIXME:
        expr = node.expr
        block = node.block
        LOOP = len(self.asm)
        self.visit(expr)
        self.asm.append('JZ {dist}'.format(dist = self.hex(len(self.asm) + 2)))
        self.asm.append('JMP END')
        BLK = len(self.asm)
        self.visit(block)
        self.asm.append('JMP {dist}'.format(dist = self.hex(LOOP)))
        END = len(self.asm)
        self.asm[BLK - 1] = 'JMP {dist}'.format(dist = self.hex(END))


    def visit_For(self, node):
        pass

    def visit_Block(self, node):
        for statement in node.compound_statement:
            self.visit(statement)

    def hex(self, value):
        if(value == 0):
            return '0H'
        lis = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        res = ''
        while(value != 0):
            res = (lis[value % 16]) + res
            value = value // 16
        return res + 'H'