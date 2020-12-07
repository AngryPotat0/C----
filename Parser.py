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
        functions_list = []
        while(self.currentToken.type != TokenType.EOF):
            functions_list.append(self.function_decl())
        # main_function = [fun for fun in functions_list if fun.name == 'main']
        # if(main_function == []):
        #     self.error()
        return Program(functions_list)

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
        while(self.currentToken.type in (TokenType.INT, TokenType.REAL)):
            result.extend(self.var_decl())
            self.eat(TokenType.SEMI)
        return result

    def var_decl(self):#FIXME:
        var_type = self.type_spec()
        var_name_list = []
        while(True):
            var_name_list.append(self.variable())
            if(self.currentToken.type == TokenType.SEMI):
                break
            self.eat(TokenType.COMMA)
        var_list = []
        for var_name in var_name_list:
            var_list.append(Var_decl(var_name,var_type))
        return var_list

    def type_spec(self):
        if(self.currentToken.type == TokenType.INT):
            result = Type(self.currentToken)
            self.eat(TokenType.INT)
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
        while(self.currentToken.type in (TokenType.ID, TokenType.RETURN, TokenType.IF, TokenType.WHILE, TokenType.FOR)):
            if(self.currentToken.type == TokenType.ID):
                if(self.lex.currentChar == '('):
                    statement_list.append(self.function_call())#????????????????????????????
                    self.eat(TokenType.SEMI)
                else:
                    statement_list.append(self.assign())
            elif(self.currentToken.type == TokenType.RETURN):
                statement_list.append(self.return_decl())
            elif(self.currentToken.type == TokenType.IF):
                statement_list.append(self.if_decl())
            elif(self.currentToken.type == TokenType.WHILE):
                statement_list.append(self.while_loop())
            elif(self.currentToken.type == TokenType.FOR):
                statement_list.append(self.for_loop())
        return statement_list

    def assign(self):
        left = self.variable()
        self.eat(TokenType.EQUAL)
        right = self.expr()
        self.eat(TokenType.SEMI)
        return Assign(left, right)

    def function_call(self):
        function_name = self.variable().value
        self.eat(TokenType.LPAREN)
        params = self.real_param_list()
        self.eat(TokenType.RPAREN)
        return Function_call(function_name,params)

    def real_param_list(self):
        params = [self.expr()]
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            params.append(self.expr())

    def if_decl(self):
        pass

    def for_loop(self):
        pass

    def while_loop(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        expr = self.expr()
        self.eat(TokenType.RPAREN)
        block = self.code_block()
        return While(expr,block)

    def expr(self):
        node = self.term()
        while(self.currentToken.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.currentToken
            if(op.type == TokenType.PLUS):
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinOp(node, self.term(), op)
        return node

    def term(self):
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
        elif(self.currentToken.type == TokenType.ID):
            if(self.lex.currentChar == '('):
                return self.function_call()#?????????????????????????
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