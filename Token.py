from enum import Enum
class TokenType(Enum):
    PLUS =              '+'
    MINUS =             '-'
    MULIT =             '*'
    DIVES =             '/'
    MOD =               '%'
    LPAREN =            '('
    RPAREN =            ')'
    LBRACE =            '{'
    RBRACE =            '}'
    EQUAL =             '='
    GREATE =            '>'
    LESS =              '<'
    COMMA =             ','
    SEMI =              ';'
    BEQUAL =            '=='
    GE =                '>='
    LE =                '<='
    INTEGER_CONST =     'INTEGER_CONST'
    REAL_CONST =        'REAL_CONST'
    ID =                'ID'
    #MAIN =              'main'#FIXME:
    INT =               'int'
    REAL =              'real'
    CHAR =              'char'
    BOOL =              'bool'
    VOID =              'void'
    IF =                'if'
    FOR =               'for'
    WHILE =             'while'
    RETURN =            'return'
    EOF =               'EOF'

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'Token type:{type},value:{value}'.format(type=self.type, value=self.value)

def reserved_keywords():
        token_list = list(TokenType)
        start = token_list.index(TokenType.INT)
        end = token_list.index(TokenType.EOF)
        reserved_keywords = {
            token_type.value : token_type
            for token_type in token_list[start:end]
        }
        return reserved_keywords