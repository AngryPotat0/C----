class TokenType(Enum):
    PLUS =              '+'
    MINUS =             '-'
    MULIT =             '*'
    DIVES =             '/'
    MOD =               '%'
    LPAREN =            '('
    RPAREN =            ')'
    INTEGER_CONST =     'INTEGER_CONST'
    REAL_CONST =        'REAL_CONST'
    EOF =               'EOF'

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'Token type:{type},value:{value}'.format(type=self.type, value=self.value)
