from Token import*
# import Token
class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.currentChar = self.text[self.pos]
        self.reserved_keywords = reserved_keywords()
    
    def advance(self):
        self.pos += 1
        if(self.pos >= len(self.text)):
            self.currentChar = None
            return
        self.currentChar = self.text[self.pos]
    
    def peek(self):
        idx = self.pos + 1
        if(idx >= len(self.text)):
            return None
        return self.text[idx]
    
    def skip_whitespace(self):
        while(self.currentChar != None and self.currentChar == ' '):
            self.advance()
        
    def number(self):
        res = ''
        while(self.currentChar != None and self.currentChar.isdigit()):
            res += self.currentChar
            self.advance()
        if(self.currentChar == '.'):
            res += '.'
            self.advance()
            while(self.currentChar != None and self.currentChar.isdigit()):
                res += self.currentChar
                self.advance()
            return Token(TokenType.REAL_CONST,float(res))
        return Token(TokenType.INTEGER_CONST,int(res))
    
    def _id(self):
        result = ''
        while(self.currentChar != None and self.currentChar.isalnum()):
            result += self.currentChar
            self.advance()
        if(result in self.reserved_keywords):
            return self.reserved_keywords[result]
        return Token(TokenType.ID, result)

    def error(self):
        raise Exception('Unexpectde char')
    
    def get_next_token(self):
        while(True):
            if(self.currentChar == None):
                return Token(TokenType.EOF,None)
            if(self.currentChar == ' '):
                self.skip_whitespace()
                continue
            if(self.currentChar == '=' and self.peek() == '='):
                self.advance()
                self.advance()
                return Token(TokenType.BEQULE, '==')
            if(self.currentChar == '>' and self.peek() == '='):
                self.advance()
                self.advance()
                return Token(TokenType.GE, '>=')
            if(self.currentChar == '<' and self.peek() == '='):
                self.advance()
                self.advance()
                return Token(TokenType.LE, '<=')
            if(self.currentChar.isdigit()):
                return self.number()
            if(self.currentChar.isalnum()):
                return self._id()

            try:
                token_type = TokenType(self.currentChar)
            except ValueError:
                self.error()
            token = Token(token_type,token_type.value)
            self.advance()
            return token