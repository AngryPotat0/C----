from enum import Enum
class TokenType(Enum):
    PLUS =              '+'
    MINUS =             '-'
    MULIT =             '*'
    DIVES =             '/'
    MOD =               '%'
    LPAREN =            '('
    RPAREN =            ')'
    EQUAL =             '='
    GREATE =            '>'
    LESS =              '<'
    BEQUAL =            '=='
    GE =               '>='
    LE =               '<='
    INTEGER_CONST =     'INTEGER_CONST'
    REAL_CONST =        'REAL_CONST'
    ID =                'ID'
    MAIN =              'MAIN'
    INT =               'INT'
    REAL =              'REAL'
    IF =                'IF'
    FOR =               'FOR'
    WHILE =             'WHILE'
    EOF =               'EOF'

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'Token type:{type},value:{value}'.format(type=self.type, value=self.value)

def reserved_keywords():
        token_list = list(TokenType)
        print(token_list)
        start = token_list.index(TokenType.MAIN)
        end = token_list.index(TokenType.EOF)
        reserved_keywords = {
            token_type.value : token_type
            for token_type in token_list[start:end]
        }
        print(reserved_keywords)
        return reserved_keywords