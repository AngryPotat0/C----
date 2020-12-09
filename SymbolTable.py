class Symbol():
    def __init__(self,name,type=None):
        self.name = name
        self.type = type

class BuildInSymbol(Symbol):
    def __init__(self,name):
        super().__init__(name)

    def __str__(self):
        return '<{class_name}(name={name})>'.format(
            class_name=self.__class__.__name__,
            name=self.name
        )

    __repr__ = __str__

class VarSymbol(object):
    def __init__(self,name,type):
        super().__init__(name,type)

    def __str__(self):
        return '<{class_name}(name={name}, type={type})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            type = self.type.name
        )

    __repr__ = __str__

class FunctionSymbol(Symbol):
    def __init__(self,name,type,params=None):
        super().__init__(name,type)
        self.params = params if params != None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )
    __repr__ = __str__

class SymbolTable():
    def __init__(self,scope_name,scope_level,enclosing_scope):
        self.scope = dict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.__init__builtins()

    def __init__builtins(self):
        self.insert(BuildInSymbol('INT'))
        self.insert(BuildInSymbol('REAL'))
    
    def error(self, msg):
        raise Exception(msg)

    def insert(self,symbol):
        name = symbol.name
        if(name in self.scope):
            self.error('Duplicate identifier is found')
        self.scope[name] = symbol

    def lookup(self,symbol_name):
        # return self.scope[symbol_name] if symbol_name in self.scope else None
        if(symbol_name in self.scope):
            return self.scope[symbol_name]
        self.error('Symbol not found')

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope', self.enclosing_scope.scope_name if self.enclosing_scope != None else None)
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__