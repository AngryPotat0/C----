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
            functions_list.append(self.fuction_decl())
        # main_function = [fun for fun in functions_list if fun.name == 'main']
        # if(main_function == []):
        #     self.error()
        return Program(functions_list)

    def function_decl(self):
        func_type = self.type_spec()
        func_name = self.variable().var_name
        func_params = self.params()
        func_body = self.code_block()
        return Function(func_type, func_name, func_params, func_body)

    def params(self):
        self.eat(TokenType.LPAREN)
        result = []
        while(True):
            param_type = self.type_spec()
            param = self.currentToken.value
            self.eat(TokenType.ID)
            result.append(Param(param,param_type))
            if(self.currentToken.type == TokenType.RPAREN):
                break
            self.eat(TokenType.COMMA)
        return result

    def code_block(self):
        self.eat(TokenType.LBRACE)
        #FIXME: 然后呢？？？？？

    def declarations(self):
        result = []
        while(self.currentToken.type in (TokenType.INT, TokenType.REAL)):
            result.append(self.var_decl())
            self.eat(TokenType.SEMI)

    def var_decl(self):
        var_type = self.type_spec()
        val = self.variable()
        self.eat(TokenType.EQUAL)
        expr = self.expr()
        self.eat(TokenType.SEMI)
        return Var_decl(var, var_type, expr)

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

    def combound_statement(self):
        pass

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
        node = self.paren()
        while(self.currentToken.type in (TokenType.MULIT, TokenType.DIVES, TokenType.MOD)):
            op = self.currentToken
            if(op.type == TokenType.MULIT):
                self.eat(TokenType.MULIT)
            elif(op.type == TokenType.DIVES):
                self.eat(TokenType.DIVES)
            else:
                self.eat(TokenType.MOD)
            node = BinOp(node,self.paren(),op)
        return node

    def paren(self):
        node = None
        if(self.currentToken.type == TokenType.LPAREN):
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
        elif(self.currentToken.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.currentToken
            if(op.type == TokenType.PLUS):
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            expr = self.expr()
            node = UnaryOp(expr, op)
        else:
            node = Num(self.currentToken)
            if(self.currentToken.type == TokenType.INTEGER_CONST):
                self.eat(TokenType.INTEGER_CONST)
            else:
                self.eat(TokenType.REAL_CONST)
        return node