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
        self.params = params

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )
    __repr__ = __str__

class SymbolTable():
    pass