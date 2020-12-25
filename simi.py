class Simi():
    def __init__(self,code):
        self.code = code
        self.pc = 0
        self.memory = [0] * 100
        self.registers = {
            'A':  0,
            'R0': 0,
            'R1': 0,
            'R2': 0,
            'R3': 0,
            'Z':  0,
            'C':  0,
        }
        self.table = {
            '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15
        }
    
    def run(self):
        while(True):
            cmd = self.code[self.pc]
            self.pc += 1
            lis = cmd.split()
            if(lis[0] == 'MOV'):
                self.mov(lis[1], lis[2])
            elif(lis[0] == 'ADD'):
                self.add(lis[2])
            elif(lis[0] == 'SUB'):
                self.sub(lis[2])
            elif(lis[0] == 'JZ'):
                self.jz(lis[1])
            elif(lis[0] == 'JC'):
                self.jc(lis[1])
            elif(lis[0] == 'JMP'):
                self.jmp(lis[1])
            elif(lis[0] == 'STA'):
                self.sta(lis[1])
            elif(lis[0] == 'LDA'):
                self.lda(lis[1])
            elif(lis[0] == 'HALT'):
                break
            else:
                raise Exception('Unexpectde code')
        for i in range(0,20):
            print(i,self.memory[i])

    def add(self,register):
        self.registers['A'] += self.registers[register]
        if(self.registers['A'] > 255):
            self.registers['A'] = self.registers['A'] & 0xff
            self.registers['C'] = 1
        else:
            self.registers['C'] = 0
        if(self.registers['A'] == 0):
            self.registers['Z'] = 1
        else:
            self.registers['Z'] = 0

    def sub(self,registers):
        self.registers['A'] -= self.registers[registers]
        if(self.registers['A'] >= 0):
            self.registers['C'] = 0
        else:
            self.registers['A'] = self.registers['A'] & 0xff
            self.registers['C'] = 1
        if(self.registers['A'] == 0):
            self.registers['Z'] = 1
        else:
            self.registers['Z'] = 0
    
    def mov(self, distance, source):
        if(source[0] == '#'):
            self.registers[distance] = int(source[1:])
            # print('*********')
            # print(self.registers[distance])
            # print('*********')
        else:
            self.registers[distance] = self.registers[source]

    def jz(self, distance):
        if(self.registers['Z'] == 1 or self.registers['A'] == 0):
            self.pc = self.toTen(distance)

    def jc(self, distance):
        if(self.registers['C'] == 1):
            self.pc = self.toTen(distance)

    def jmp(self, distance):
        self.pc = self.toTen(distance)

    def lda(self, address):
        address = self.toTen(address)
        self.registers['A'] = self.memory[address]

    def sta(self, address):
        address = self.toTen(address)
        self.memory[address] = self.registers['A']

    def halt(self):
        print('Over')

    def toTen(self, value):
        value = value[0:-1]
        res = 0
        t = 0
        for i in range(len(value) - 1, -1, -1):
            res += self.table[value[i]] * 16 ** t
            t += 1
        return res


# text = ""
# file = open('code.txt')
# while(True):
#     line = file.readline()
#     text += line
#     if(not line):
#         break
# file.close()
# s = Simi(text.split('\n'))
# s.run()