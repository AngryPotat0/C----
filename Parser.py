from Token import*
from AST import*


class Parser():
    def __init__(self,lex):
        self.lex = lex
        self.currentToken = self.lex.get_next_token()

    def eat(self,expect_type):
        if(self.currentToken.type != expect_type):
            self.error()
        self.currentToken = self.lex.get_next_token()
    
    def error(self):
        raise Exception('Unexpected Token{token}'.format(token = self.currentToken))
    
    def parser(self):
        return self.program()
    
    def program(self):
        function_list = []
        while(self.currentToken.type != TokenType.EOF):
            function_list.append(self.function_decl())
            # function = function_list[-1]
            # print("function:{name}, type :{type}".format(name = function.name, type = function.type))
        # main_function = [fun for fun in functions_list if fun.name == 'main']
        # if(main_function == []):
        #     self.error()
        return Program(function_list)

    def function_decl(self):
        func_type = self.type_spec().value
        func_name = self.variable().value
        func_params = self.params()
        func_body = self.code_block()
        return Function(func_type, func_name, func_params, func_body)

    def return_decl(self):
        self.eat(TokenType.RETURN)
        expr = self.expr()
        self.eat(TokenType.SEMI)
        return Return(expr)

    def params(self):
        result = []
        self.eat(TokenType.LPAREN)
        if(self.currentToken.type == TokenType.RPAREN):
            self.eat(TokenType.RPAREN)
            return result
        while(True):
            param_type = self.type_spec()
            param = self.variable()
            result.append(Param(param,param_type))
            if(self.currentToken.type == TokenType.RPAREN):
                break
            self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        return result

    def code_block(self):
        self.eat(TokenType.LBRACE)
        #FIXME: 然后呢？？？？？
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        self.eat(TokenType.RBRACE)
        return Code_Block(declarations,compound_statement)

    def declarations(self):
        result = []
        while(self.currentToken.type in (TokenType.INT, TokenType.REAL, TokenType.CHAR, TokenType.BOOL)):
            result.extend(self.var_decl())
            self.eat(TokenType.SEMI)
        return result

    def var_decl(self):#FIXME:
        var_type = self.type_spec()
        decl_list = []
        while(True):
            name = self.variable()
            if(self.currentToken.type == TokenType.LBRACKET):
                self.eat(TokenType.LBRACKET)
                expr = self.expr()
                self.eat(TokenType.RBRACKET)
                decl_list.append(Array_decl(name,var_type,expr))
            else:
                decl_list.append(Var_decl(name,var_type))
            if(self.currentToken.type == TokenType.SEMI):
                break
            self.eat(TokenType.COMMA)
        return decl_list

    def array(self):
        name = self.variable()
        self.eat(TokenType.LBRACKET)
        index = self.expr()
        self.eat(TokenType.RBRACKET)
        return Array(name,index)

    def type_spec(self):
        if(self.currentToken.type == TokenType.INT):
            result = Type(self.currentToken)
            self.eat(TokenType.INT)
            return result
        elif(self.currentToken.type == TokenType.CHAR):
            result = Type(self.currentToken)
            self.eat(TokenType.CHAR)
            return result
        elif(self.currentToken.type == TokenType.VOID):
            result = Type(self.currentToken)
            self.eat(TokenType.VOID)
            return result
        elif(self.currentToken.type == TokenType.BOOL):
            result = Type(self.currentToken)
            self.eat(TokenType.BOOL)
            return result
        else:
            result = Type(self.currentToken)
            self.eat(TokenType.REAL)
            return result

    def variable(self):
        var = self.currentToken
        self.eat(TokenType.ID)
        res = Var(var)
        return res

    def compound_statement(self):#FIXME:
        statement_list = []
        while(self.currentToken.type in (
            TokenType.ID, TokenType.RETURN, TokenType.IF, TokenType.WHILE, TokenType.FOR,TokenType.BREAK, TokenType.CONTINUE)):
            statement_list.append(self.statement())
        return statement_list

    def statement(self):
        result = None
        if(self.currentToken.type == TokenType.ID):
            if(self.lex.currentChar == '('):
                result = self.function_call()
                self.eat(TokenType.SEMI)
            else:
                result = self.assign()
                self.eat(TokenType.SEMI)
        elif(self.currentToken.type == TokenType.RETURN):
            result = self.return_decl()
        elif(self.currentToken.type == TokenType.IF):
            result = self.if_decl()
        elif(self.currentToken.type == TokenType.WHILE):
            result = self.while_loop()
        elif(self.currentToken.type == TokenType.FOR):
            result = self.for_loop()
        return result

    def assign(self):
        left = None
        if(self.lex.currentChar == '['):
            left = self.array()
        else:
            left = self.variable()
        self.eat(TokenType.EQUAL)
        right = self.expr()
        # self.eat(TokenType.SEMI)
        return Assign(left, right)

    def function_call(self):
        function_name = self.variable().value
        params = []
        self.eat(TokenType.LPAREN)
        if(self.currentToken.type != TokenType.RPAREN):
            params = self.real_param_list()
        self.eat(TokenType.RPAREN)
        return Function_call(function_name,params)

    def real_param_list(self):
        params = [self.expr()]
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            params.append(self.expr())
        return params

    def if_decl(self):#FIXME:
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        expr = self.expr()
        self.eat(TokenType.RPAREN)
        block = else_block = None

        if(self.currentToken.type == TokenType.LBRACE):
            block = self.block()
        else:
            block = self.statement()
            self.eat(TokenType.SEMI)

        if(self.currentToken.type == TokenType.ELSE):
            self.eat(TokenType.ELSE)
            if(self.currentToken.type == TokenType.LBRACE):
                else_block = self.block()
            else:
                else_block = self.statement()
                self.eat(TokenType.SEMI)
                
        return If(expr,block,else_block)
            

    def for_loop(self):#FIXME:
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        assign1 = expr = assign2 = None
        if(self.currentToken.type != TokenType.SEMI):
            assign1 = self.assign()
        self.eat(TokenType.SEMI)
        if(self.currentToken.type != TokenType.SEMI):
            expr = self.expr()
        self.eat(TokenType.SEMI)
        if(self.currentToken.type != TokenType.SEMI):
            assign2 = self.assign()
        self.eat(TokenType.RPAREN)
        block = self.block()
        return For(assign1,expr,assign2,block)

    def while_loop(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        expr = self.expr()
        self.eat(TokenType.RPAREN)
        block = self.block()
        return While(expr,block)

    def block(self):#FIXME:
        self.eat(TokenType.LBRACE)
        statement_list = []
        while(self.currentToken.type in (
                TokenType.ID, TokenType.RETURN, TokenType.IF, TokenType.WHILE, TokenType.FOR,
                TokenType.BREAK, TokenType.CONTINUE
            )):
            if(self.currentToken.type == TokenType.BREAK):
                statement_list.append(Break())
                self.eat(TokenType.BREAK)
                self.eat(TokenType.SEMI)
            elif(self.currentToken.type == TokenType.CONTINUE):
                statement_list.append(Continue())
                self.eat(TokenType.CONTINUE)
                self.eat(TokenType.SEMI)
            else:
                statement_list.append(self.statement())
        self.eat(TokenType.RBRACE)
        return Block(statement_list)
        # self.eat(TokenType.LBRACE)
        # compound_statement = self.compound_statement()
        # self.eat(TokenType.RBRACE)
        # return Block(compound_statement)

    def expr(self):
        node = self.level_2()
        while(self.currentToken.type == TokenType.BOR):
            op = self.currentToken
            self.eat(TokenType.BOR)
            node = BinOp(node, self.level_2(), op)
        return node

    def level_2(self):
        node = self.level_3()
        while(self.currentToken.type == TokenType.BAND):
            op = self.currentToken
            self.eat(TokenType.BAND)
            node = BinOp(node, self.level_3(), op)
        return node
    
    def level_3(self):
        node = self.level_4()
        while(self.currentToken.type == TokenType.OR):
            op = self.currentToken
            self.eat(TokenType.OR)
            node = BinOp(node, self.level_4(), op)
        return node

    def level_4(self):
        node = self.level_5()
        while(self.currentToken.type == TokenType.XOR):
            op = self.currentToken
            self.eat(TokenType.XOR)
            node = BinOp(node, self.level_5(), op)
        return node

    def level_5(self):
        node = self.level_6()
        while(self.currentToken.type == TokenType.AND):
            op = self.currentToken
            self.eat(TokenType.AND)
            node = BinOp(node, self.level_6(), op)
        return node

    def level_6(self):
        node = self.level_7()
        op_list = [
            TokenType.BEQUAL,TokenType.NEQUAL,TokenType.GREATE,TokenType.GE,TokenType.LESS,TokenType.LE
        ]
        if(self.currentToken.type in op_list):
            op = self.currentToken
            self.eat(op.type)#FIXME:
            node = BinOp(node, self.level_7(), op)
        return node

    def level_7(self):
        node = self.level_8()
        while(self.currentToken.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.currentToken
            if(op.type == TokenType.PLUS):
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinOp(node, self.level_8(), op)
        return node

    def level_8(self):
        node = self.factor()
        while(self.currentToken.type in (TokenType.MULIT, TokenType.DIVES, TokenType.MOD)):
            op = self.currentToken
            if(op.type == TokenType.MULIT):
                self.eat(TokenType.MULIT)
            elif(op.type == TokenType.DIVES):
                self.eat(TokenType.DIVES)
            else:
                self.eat(TokenType.MOD)
            node = BinOp(node,self.factor(),op)
        return node

    # def level_9(self):
    #     node = self.factor()
    #     while(self.currentToken.type in (TokenType.NOT, TokenType.BNOT)):
    #         op = self.currentToken
    #         if(op.type == TokenType.NOT):
    #             self.eat(TokenType.NOT)
    #         else:
    #             self.eat(TokenType.BNOT)
    #         node = BinOp(node, self.factor(), op)
    #     return node

    def factor(self):
        if(self.currentToken.type == TokenType.LPAREN):
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif(self.currentToken.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.currentToken
            if(op.type == TokenType.PLUS):
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            expr = self.expr()
            node = UnaryOp(expr, op)
            return node
        elif(self.currentToken.type in (TokenType.NOT, TokenType.BNOT)):
            op = self.currentToken
            if(op.type == TokenType.NOT):
                self.eat(TokenType.NOT)
            else:
                self.eat(TokenType.BNOT)
            expr = self.expr()
            node = UnaryOp(expr, op)
            return node
        elif(self.currentToken.type == TokenType.ID):
            if(self.lex.currentChar == '('):
                return self.function_call()#?????????????????????????
            if(self.lex.currentChar == '['):
                node = self.array()
            else:
                node = self.variable()
            return node
        else:
            node = Num(self.currentToken)
            if(self.currentToken.type == TokenType.INTEGER_CONST):
                self.eat(TokenType.INTEGER_CONST)
            else:
                self.eat(TokenType.REAL_CONST)
            return node
        self.error()