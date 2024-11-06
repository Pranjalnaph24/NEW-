class AssemblerPassOne:
    def __init__(self):
        self.symbol_table = {}       # For storing labels and variables (symbols)
        self.intermediate_code = []  # For storing intermediate code
        self.opcode_table = {
            "ADD": "01",
            "SUB": "02",
            "MUL": "03",
            "DIV": "04",
            "LOAD": "05",
            "STORE": "06",
            "START": "00",
            "END": "FF",
            "ORIGIN": "A0",  # Just a placeholder for ORIGIN directive opcode
            "LTORG": "B0",   # Placeholder for LTORG directive opcode
            "DECLARE": "C0", # Placeholder for DECLARE directive
        }
        self.literal_table = []      # For storing literals
        self.pool_table = []         # For storing literal pool indexes
        self.current_address = 0     # Tracks the current memory address
        self.literal_index = 0       # Index for literals
     
    def pass_one(self, source_code):
        for line in source_code:
            parts = line.strip().split()
            if not parts:
                continue

            # Handle ORIGIN directive (sets starting address)
            if parts[0] == "START":
                self.current_address =int( parts[1]) if len(parts)>0 else self.current_address
                continue
            if parts[0] == "ORIGIN":
                self.current_address = int(parts[1]) if len(parts) > 1 else self.current_address
                continue

            # Handle LTORG directive (process literals)
            if parts[0] == "LTORG":
                self.process_literals()
                continue

            # Handle END directive
            if parts[0] == "END":
                self.intermediate_code.append((self.current_address, "END"))  # Using FF for END opcode
                break

            # Handle labels (symbol table)
            if parts[0].endswith(":"):
                label = parts[0][:-1]  # Remove the colon from the label
                self.symbol_table[label] = self.current_address
                
                parts = parts[1:]  # Remove the label part from the instruction
           
            # Handle DECLARE statements (constant and storage declarations)
            if parts[0] == "DECLARE":
                if len(parts) >= 2:
                    declaration_type = parts[1]
                    if declaration_type == "CONSTANT":
                        value = parts[2] if len(parts) > 2 else "0"
                        
                        self.symbol_table[parts[2]] = self.current_address
                        
                        self.intermediate_code.append((self.current_address,value))
                    elif declaration_type == "STORAGE":
                        variable = parts[2] if len(parts) > 2 else "UNKNOWN"
                      
                        self.symbol_table[variable] = self.current_address
                        self.intermediate_code.append((self.current_address,variable))
                    self.current_address += 1
                continue

            # Handle opcodes and add to intermediate code
            if parts[0] in self.opcode_table:
              
                self.intermediate_code.append((self.current_address, parts[0]))
                self.current_address += 1

            # Handle literals (e.g., =5, =A)
            for part in parts:
                if part.startswith('='):
                    literal = part[1:]
                    if literal not in self.literal_table:
                        self.literal_table.append(literal)
                        if not self.pool_table or self.pool_table[-1] != self.literal_index:
                            self.pool_table.append(self.literal_index)
                        self.literal_index += 1

    def process_literals(self):
        # This method processes literals when LTORG is encountered
        for literal in self.literal_table:
            self.intermediate_code.append((self.current_address, f"= {literal}"))
            self.current_address += 1
      # Clear literal table after processing

    def display_tables(self):
        print("Symbol Table:")
        for label, address in self.symbol_table.items():
            print(f"{label}: {address}")

        print("\nLiteral Table:")
        for i, literal in enumerate(self.literal_table):
            print(f"Literal {i + 1}: {literal}")

        print("\nPool Table:")
        for i, index in enumerate(self.pool_table):
            print(f"Pool {i + 1}: Index {index}")

        print("\nIntermediate Code:")
        for code in self.intermediate_code:
            print(f" ({code[1]} ,{code[0]})")

        # Constants and Storage Declarations are omitted from final output

# To run pass one
if __name__ == "__main__":
    source_code = [
       "START 100",
"LOAD A",
"ADD =5", 
"SUB =10",  
"STORE B",
"ORIGIN 200",
"DECLARE STORAGE A",
"DECLARE STORAGE B",
"LTORG",
"END"
    ]

    assembler = AssemblerPassOne()
    assembler.pass_one(source_code)
    assembler.display_tables()

    print("\n=== Code Execution Successful ===")
