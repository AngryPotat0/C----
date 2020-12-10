class Frame():
    def __init__(self,name,level,type = 'Function'):
        self.name = name
        self.level = level
        self.type = type
        self.memory = dict()

    def set_value(self,name,value):
        self.memory[name] = value

    def get_value(self,name):
        return self.memory[name] if name in self.memory else None

    def __setitem__(self,name,value):
        self.memory[name] = value

    def __getitem__(self,name):
        return self.memory[name]

class CallStack():
    def __init__(self):
        self.stack = []

    def pop(self):
        self.stack.pop()

    def push(self,frame):
        self.stack.append(frame)

    def peek(self):
        return self.stack[-1]