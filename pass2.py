class AssemblerPass2:
    def __init__(self):
        self.opcode_table={
            "ADD" : "1",
            "SUB" : "2",
            "MUL" : "3",
            "DIV":"4",
            "LOAD": "5",
            "STORE" : "6",
            "START" : "00",
            "END" : "FF"
        }
        
        self.symbol_table = {}
        self.literal= []
        self.current_add = 0
        self.pool_table = []
        
        
    def pass_two(self, intermediate_code):
        machine_code =[]
        
        for address, instruction in intermediate_code:
            if instruction in self.opcode_table:
                machine_code.append((address,self.opcode_table[instruction]))
                
            elif instruction == "END":
                machine_code.append((address,"FF"))
                
            elif instruction in self.symbol_table:
                symbol_add = self.symbol_table[instruction]
                machine_code.append((address,str(symbol_add)))
                
            elif instruction in self.literal:
                machine_code.append((address,instruction))
                
            
        for index in self.pool_table:
            literal = self.literal[index]
            machine_code.append((self.current_add,literal))
            self.current_add+=1
            
        return machine_code
        
    def display_machinecode(self,machine_code):
        for address,code in machine_code:
            print(f"{address}:{code}")
            
symbol_table={
    "A" :103,
    "B":104,
    "RESULT":105
}
literal = ["5","10"]
pool_table =[0,1]

intermediate_code = [
    (100,"LOAD"),
    (101,"ADD"),
    (102,"STORE"),
    (103,"A"),
    (104,"B"),
    (105,"RESULT"),
    (106,"END")
    ]

ass=AssemblerPass2()
ass.symbol_table = symbol_table
ass.literal = literal
ass.pool_table = pool_table

machine_code = ass.pass_two(intermediate_code)

ass.display_machinecode(machine_code)